import database
import re
from flask import Blueprint, jsonify, request
from sqlite3 import Error as Sqlite3Error

auth = Blueprint('auth', __name__, url_prefix='/auth')

def _check_username(username: str) -> bool:
    if not 3 <= len(username) <= 16:
        return False
    
    return bool(re.match(r'^[a-z0-9._-]+$', username))


@auth.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({'error': 'mimetype not supported'}), 415
    
    data = request.get_json()
    
    if not all(key in data for key in ['username', 'password']):
        return jsonify({'error': 'missing required fields'}), 400
    
    username = str(data['username']).strip()
    password = str(data['password']).strip()
    display_name = data.get('display_name')
    
    if display_name is not None:
        display_name = str(display_name).strip()
    
    if not _check_username(username):
        return jsonify({'error': 'invalid username (3-16 characters)'}), 400
    
    if len(password) < 4:
        return jsonify({'error': 'password too small (4 characters min)'}), 400
    
    try:
        user_id, master_key = database.create_user(username, password, display_name)
        
        return jsonify({
            'message': 'registration successful',
            'master_key': master_key,
            'user': {
                'id': user_id,
                'username': username
            }
        }), 201
    
    except Sqlite3Error as e:
        e_status = e.args[1] if len(e.args) > 1 else 500
        e_msg = e.args[0]
        
        return jsonify({'error': f'database error: {str(e_msg)}'}), e_status

@auth.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'mimetype not supported'}), 415
    
    data = request.get_json()
    
    if not all(key in data for key in ['username', 'password']):
        return jsonify({'error': 'missing required fields'}), 400
    
    username = str(data['username']).strip()
    password = str(data['password']).strip()
    
    try:
        user_id, master_key = database.authenticate_user(username, password)
        
        return jsonify({
            'message': 'login successful',
            'master_key': master_key,
            'user': {
                'id': user_id,
                'username': username
            }
        }), 200
    
    except Sqlite3Error as e:
        e_status = e.args[1] if len(e.args) > 1 else 500
        e_msg = e.args[0]
        
        return jsonify({'error': f'database error: {str(e_msg)}'}), e_status
    
    return user_id, master_key
