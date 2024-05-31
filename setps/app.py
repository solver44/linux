import requests
import json
import pika  # for RabbitMQ
from kafka import KafkaProducer  # for Kafka
from requests_toolbelt.multipart.encoder import MultipartEncoder
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import logging
import time
import redis
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration variables
api_name = "your_api_name"
api_url = "your_api_url"
headers_dict = {"your": "headers"}
params_dict = {"your": "params"}
http_method = "GET"  # or POST, PUT, DELETE
request_type = "json"  # or form-data
request_data_dict = {"your": "data"}
cron_schedule = "*/5 * * * *"  # Cron format for every 5 minutes
redis_host = "localhost"  # Replace with your Redis host
redis_port = 6379
redis_db = 0

# Unique identifier for this instance
instance_id = str(uuid.uuid4())

# Initialize Redis client
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)

def log_history(stage, message, detail):
    type = "info"
    if "error" in stage:
        type = "error" 
        
    log_entry = {
        "instance_id": instance_id,
        "stage": stage,
        "message": message,
        "detail": detail,
        "type": type,
        "timestamp": datetime.now().isoformat()
    }
    try:
        redis_client.lpush(f'process_history:{instance_id}', json.dumps(log_entry))
        logger.info(f"{stage}: {message}")
    except Exception as e:
        logger.error(f"Failed to log history to Redis: {e}")

def notify_server(stage, message, detail = None):
    log_history(stage, message, detail)
    # Removed direct server notification to follow the new requirement

def send_to_rabbitmq(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=f'{api_name}_queue')
        channel.basic_publish(exchange='', routing_key=f'{api_name}_queue', body=message)
        connection.close()
        notify_server("send_to_rabbitmq", "Message sent to RabbitMQ")
    except Exception as e:
        notify_server("send_to_rabbitmq_error", str(e))
        logger.error(f"Failed to send to RabbitMQ: {e}")

def send_to_kafka(message):
    try:
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        producer.send(f'{api_name}_topic', message.encode('utf-8'))
        producer.flush()
        producer.close()
        notify_server("send_to_kafka", "Message sent to Kafka")
    except Exception as e:
        notify_server("send_to_kafka_error", str(e))
        logger.error(f"Failed to send to Kafka: {e}")

def fetch_data():
    url = api_url
    headers = headers_dict
    params = params_dict
    request_data = request_data_dict

    try:
        if http_method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif http_method == 'POST':
            if request_type == 'json':
                response = requests.post(url, headers=headers, params=params, json=request_data)
            else:
                m = MultipartEncoder(fields=request_data)
                headers['Content-Type'] = m.content_type
                response = requests.post(url, headers=headers, params=params, data=m)
        else:
            raise ValueError('Unsupported HTTP method')
    except Exception as e:
        notify_server("fetch_data_error", str(e))
        logger.error(f"Failed to fetch data: {e}")
        raise

    try:
        data = response.json()
        notify_server("fetch_data", "Data fetched successfully", data)
    except ValueError:
        data = {'response': response.text}

    return data

def process_data(data):
    # Add any data processing logic here if needed
    processed_data = json.dumps(data, indent=4)
    notify_server("process_data", "Data processed successfully")
    return processed_data

def send_data():
    logger.info(f"Starting data fetch at {datetime.now()}")
    notify_server("send_data_start", "Data fetch started")
    try:
        data = fetch_data()
        processed_data = process_data(data)
        send_to_rabbitmq(processed_data)  # try if not responding send to kafka
        # send_to_kafka(processed_data)
        logger.info(f"Data processing and sending completed at {datetime.now()}")
        notify_server("send_data_complete", "Data processing and sending completed")
    except Exception as e:
        notify_server("send_data_error", str(e))
        logger.error(f"Error in send_data: {e}")

def main():
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }

    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }

    scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
    scheduler.add_job(send_data, 'cron', **{'minute': cron_schedule.split()[0], 'hour': cron_schedule.split()[1], 'day': cron_schedule.split()[2], 'month': cron_schedule.split()[3], 'day_of_week': cron_schedule.split()[4]})
    scheduler.start()
    logger.info("Scheduler started")
    notify_server("scheduler_start", "Scheduler started")

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler shut down")
        notify_server("scheduler_shutdown", "Scheduler shut down")

if __name__ == "__main__":
    main()