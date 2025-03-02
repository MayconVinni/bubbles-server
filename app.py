import database
import os
from flask import Flask, send_from_directory
from api import api

app = Flask(__name__)
app.register_blueprint(api)

os.makedirs('db/', exist_ok=True)
database.init_users()

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static/pages', 'index.html')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000
    )
