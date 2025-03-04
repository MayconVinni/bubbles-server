import database
from flask import Blueprint, request, jsonify
from sqlite3 import Error as Sqlite3Error

guilds = Blueprint('guilds', __name__, url_prefix='/guilds')


@guilds.route('/create', methods=['POST'])
def create():
    REQUIRED_PARAMS = ['name']
    
    if not request.is_json:
        return jsonify({'error': 'mimetype not supported'}), 415
    
    data = request.get_json()
    
    if not all(key in data for key in REQUIRED_PARAMS):
        return jsonify({'error': 'missing required fields'}), 400
    
    
    guild_name = data['name'].strip()
    guild_desc = data.get('description')
    
    if guild_desc is not None:
        guild_desc = guild_desc.strip()
    
    # TODO: call database to create guild using:
    # master_key (header), name, description (optional)
