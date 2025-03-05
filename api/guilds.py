import database
from flask import Blueprint, request, jsonify
from sqlite3 import Error as Sqlite3Error
from constants import MAX_LENGTH, MIN_LENGTH

guilds = Blueprint('guilds', __name__, url_prefix='/guilds')


@guilds.route('/create', methods=['POST'])
def create():
    REQUIRED_PARAMS = ['master_key', 'name']
    
    if not request.is_json:
        return jsonify({'error': 'mimetype not supported'}), 415
    
    data = request.get_json()
    
    if not all(key in data for key in REQUIRED_PARAMS):
        return jsonify({'error': 'missing required fields'}), 400
    
    
    master_key = data['master_key'].strip()
    name = data['name'].strip()
    description = data.get('description')
    invite = data.get('invite')
    invite_only = data.get('only_invite', True)
    
    if len(name) > MAX_LENGTH['GUILD_NAME'] or len(name) < 1:
        return jsonify({'error': f'name too big or small (max: {MAX_LENGTH["GUILD_NAME"]})'}), 400
    
    if description is not None:
        description = description.strip()
        
        if len(description) > MAX_LENGTH['GUILD_DESCRIPTION'] or len(description) < 1:
            return jsonify({'error': f'description too big or small (max: {MAX_LENGTH["GUILD_DESCRIPTION"]})'}), 400
    
    if invite is not None:
        invite = invite.strip()
        
        if len(invite) > MAX_LENGTH['GUILD_INVITE'] or len(invite) < 1:
            return jsonify({'error': f'invite too big or small (max: {MAX_LENGTH["GUILD_INVITE"]})'}), 400
    
    if not isinstance(invite_only, bool):
        return jsonify({'error': 'only_invite is not a boolean'}), 400
    
    
    try:
        guild_data = database.create_guild(master_key, name, description, invite, invite_only)
        
        return jsonify(guild_data), 201
    
    except Sqlite3Error as e:
        e_status = e.args[1] if len(e.args) > 1 else 500
        e_msg = e.args[0]
        
        return jsonify({'error': f'database error: {str(e_msg)}'}), e_status
