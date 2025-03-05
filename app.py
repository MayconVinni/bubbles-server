import database
import os
from flask import Flask, send_from_directory
from api import api

app = Flask(__name__)
app.register_blueprint(api)

paths = (
    'db/',
    'uploads/avatar/',
    'uploads/guild_icon/',
    'uploads/group_icon/',
)

for path in paths:
    os.makedirs(path, exist_ok=True)

database.init()


@app.route('/')
def index():
    return send_from_directory('static/html', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
