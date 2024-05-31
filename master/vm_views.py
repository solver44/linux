from flask import Flask, jsonify, request
import redis
import json

app = Flask(__name__)
redis_host = "localhost"
redis_port = 6379
redis_db = 0

redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)

@app.route('/logs/<instance_id>', methods=['GET'])
def get_logs(instance_id):
    try:
        logs = redis_client.lrange(f'process_history:{instance_id}', 0, -1)
        logs = [json.loads(log) for log in logs]
        return jsonify(logs), 200
    except Exception as e:
        return str(e), 500
    
# [
#     {
#         "instance_id": "123e4567-e89b-12d3-a456-426614174000",
#         "stage": "fetch_data",
#         "message": "Data fetched successfully",
#         "timestamp": "2023-05-30T12:34:56.789Z"
#     },
#     {
#         "instance_id": "123e4567-e89b-12d3-a456-426614174000",
#         "stage": "process_data",
#         "message": "Data processed successfully",
#         "timestamp": "2023-05-30T12:35:56.789Z"
#     },
#     {
#         "instance_id": "123e4567-e89b-12d3-a456-426614174000",
#         "stage": "send_to_rabbitmq",
#         "message": "Message sent to RabbitMQ",
#         "timestamp": "2023-05-30T12:36:56.789Z"
#     }
# ]


@app.route('/instances', methods=['GET'])
def get_instances():
    try:
        keys = redis_client.keys('process_history:*')
        instances = [key.split(':')[1] for key in keys]
        return jsonify(instances), 200
    except Exception as e:
        return str(e), 500  
# [
#     "123e4567-e89b-12d3-a456-426614174000",
#     "987e6543-e21b-12d3-a456-426614174111",
#     "abcde123-45f6-7890-ab12-34567890cdef"
# ]