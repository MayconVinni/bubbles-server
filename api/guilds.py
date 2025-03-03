import database
from flask import Blueprint, request, jsonify
from sqlite3 import Error as Sqlite3Error

guilds = Blueprint('guilds', __name__, url_prefix='/guilds')


@guilds.route('/create', methods=['POST'])
def create():
    REQUIRED_PARAMS = []
    
    if not request.is_json:
        return jsonify({'error': 'mimetype not supported'}), 415
    
    data = request.get_json()
    
    if not all(key in data for key in REQUIRED_PARAMS):
        return jsonify({'error': 'missing required fields'}), 400
