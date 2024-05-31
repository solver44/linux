from fastapi import FastAPI, HTTPException, Request, Depends
from sqlalchemy.orm import Session
import pika
from kafka import KafkaProducer
import json
from database import SessionLocal, Config
from pydantic import BaseModel
import redis
import uuid

app = FastAPI()

# Application ID
APP_ID = str(uuid.uuid4())

class ConfigUpdate(BaseModel):
    rabbitmq_host: str
    rabbitmq_queue: str
    kafka_bootstrap_servers: str
    kafka_topic: str
    redis_host: str
    redis_port: int
    app_name: str
    app_type: str

class LogEntry(BaseModel):
    log_type: str
    message: str
    detail: str
    source_id: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_config(db: Session):
    return db.query(Config).first()

def log_to_redis(redis_client, log_entry: LogEntry):
    log_id = str(uuid.uuid4())
    redis_client.hset(f"log:{log_id}", mapping=log_entry.model_dump())
    redis_client.lpush(f"logs:{log_entry.source_id}", log_id)

def register_source(redis_client, app_id, app_name, app_type):
    redis_client.hset(f"source:{app_id}", mapping={"id": app_id, "name": app_name, "app_type": app_type})

def send_to_rabbitmq(config: Config, message: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=config.rabbitmq_queue, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=config.rabbitmq_queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()

def send_to_kafka(config: Config, message: dict):
    producer = KafkaProducer(
        bootstrap_servers=config.kafka_bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    producer.send(config.kafka_topic, message)
    producer.flush()
    producer.close()

@app.post("/push")
async def send_message(request: Request, db: Session = Depends(get_db)):
    if not request.headers.get("Content-Type") == "application/json":
        raise HTTPException(status_code=400, detail="Content type must be application/json")

    message = await request.json()
    config = get_config(db)

    if not config:
        raise HTTPException(status_code=500, detail="Server side error")

    redis_client = redis.Redis(host=config.redis_host, port=config.redis_port, db=0)

    try:
        send_to_rabbitmq(config, message)
        log_to_redis(redis_client, LogEntry(log_type="message_sent", source_id=APP_ID, message="Message sent to RabbitMQ", detail=json.dumps(message)))
    except Exception as e:
        log_to_redis(redis_client, LogEntry(log_type="error", source_id=APP_ID, message="RabbitMQ error", detail=str(e)))
        try:
            send_to_kafka(config, message)
            log_to_redis(redis_client, LogEntry(log_type="message_sent", source_id=APP_ID, message="Message sent to Kafka", detail=json.dumps(message)))
        except Exception as kafka_e:
            log_to_redis(redis_client, LogEntry(log_type="error", source_id=APP_ID, message="Kafka error", detail=str(kafka_e)))
            raise HTTPException(status_code=500, detail="Server side error")

    return {"status": "Successfully sent"}

@app.post("/update-config")
async def update_config(config_update: ConfigUpdate, db: Session = Depends(get_db)):
    config = get_config(db)
    if config:
        config.rabbitmq_host = config_update.rabbitmq_host
        config.rabbitmq_queue = config_update.rabbitmq_queue
        config.kafka_bootstrap_servers = config_update.kafka_bootstrap_servers
        config.kafka_topic = config_update.kafka_topic
        config.redis_host = config_update.redis_host
        config.redis_port = config_update.redis_port
        config.app_name = config_update.app_name
        config.app_type = config_update.app_type
    else:
        config = Config(**config_update.dict())
        db.add(config)
    
    db.commit()
    db.refresh(config)
    redis_client = redis.Redis(host=config.redis_host, port=config.redis_port, db=0)
    register_source(redis_client, APP_ID, config.app_name, config.app_type)
    log_to_redis(redis_client, LogEntry(log_type="config_update", source_id=APP_ID, message="Configuration updated", detail=json.dumps(config_update.dict())))
    return {"status": "Configuration updated successfully"}

if __name__ == "__main__":
    db = SessionLocal()
    config = get_config(db)
    if config:
        redis_client = redis.Redis(host=config.redis_host, port=config.redis_port, db=0)
        register_source(redis_client, APP_ID, config.app_name, config.app_type)
        startup_log = LogEntry(
            log_type="startup",
            source_id=APP_ID,
            message=f"Application {config.app_name} started",
            detail=f"Type: {config.app_type}"
        )
        log_to_redis(redis_client, startup_log)
    db.close()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
