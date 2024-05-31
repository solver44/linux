from flask import Flask, send_from_directory
from flask_basicauth import BasicAuth
from tinydb import TinyDB
from logging_config import configure_logging
from views import details, create_vm, delete_class
from vm_views import app as logging_app

app = Flask(__name__)
basic_auth = BasicAuth(app)
db = TinyDB("database/proxmox-class.json", indent=3)

app.config.from_object('config')

configure_logging()

# app.add_url_rule("/", view_func=index)
@app.route('/')
def serve():
    return send_from_directory('templates/build', 'index.html')

app.add_url_rule("/api/details", view_func=details)
app.add_url_rule("/create", view_func=create_vm, methods=["POST"])
app.add_url_rule("/delete", view_func=delete_class, methods=["PUT"])

# Register the logging server routes
app.register_blueprint(logging_app, url_prefix='/api/services')

if __name__ == "__main__":
    app.run(debug=True, port=8080)