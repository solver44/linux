from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sync@server#123!'
socketio = SocketIO(app)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    sources = get_all_sources()
    return render_template('index.html', sources=sources)

def get_all_sources():
    source_keys = redis_client.keys('source:*')
    sources = [redis_client.hgetall(key) for key in source_keys]
    return [{k.decode(): v.decode() for k, v in source.items()} for source in sources]

@app.route('/logs/<source_id>')
def logs(source_id):
    return render_template('logs.html', source_id=source_id)

@socketio.on('connect')
def handle_connect():
    emit('connected', {'data': 'Connected'})

@socketio.on('join')
def handle_join(data):
    source_id = data['source_id']
    emit_logs(source_id)

def emit_logs(source_id):
    log_keys = redis_client.lrange(f'logs:{source_id}', 0, -1)
    logs = [redis_client.hgetall(key) for key in log_keys]
    logs = [{k.decode(): v.decode() for k, v in log.items()} for log in logs]
    socketio.emit('logs', logs)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3333)
