import database
import re
from flask import Blueprint, request, jsonify
from sqlite3 import Error as Sqlite3Error
from constants import MAX_LENGTH, MIN_LENGTH

REQUIRED_PARAMS = ['username', 'password']
auth = Blueprint('auth', __name__, url_prefix='/auth')

def _check_username(username):
    if not MIN_LENGTH['USER_NAME'] <= len(username) <= MAX_LENGTH['USER_NAME']:
        return False
    
    return bool(re.match(r'^[a-zA-Z0-9._-]+$', username))


@auth.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({'error': 'mimetype not supported'}), 415
    
    data = request.get_json()
    
    if not all(key in data for key in REQUIRED_PARAMS):
        return jsonify({'error': 'missing required fields'}), 400
    
    
    username = data['username'].strip()
    password = data['password'].strip()
    display_name = data.get('display_name')
    about_me = data.get('about_me')
    
    if display_name is not None:
        display_name = display_name.strip()
        
        if len(display_name) > MAX_LENGTH['USER_DISPLAYNAME']:
            return jsonify({'error': f'display_name too big (max: {MAX_LENGTH["USER_DISPLAYNAME"]})'}), 400
    
    if about_me is not None:
        about_me = about_me.strip()
        
        if len(about_me) > MAX_LENGTH['USER_ABOUTME']:
            return jsonify({'error': f'about_me too big (max: {MAX_LENGTH["USER_ABOUTME"]})'}), 400
    
    
    if not _check_username(username):
        return jsonify({'error': f'invalid username ({MIN_LENGTH["USER_NAME"]}-{MAX_LENGTH["USER_NAME"]} characters)'}), 400
    
    if len(password) < MIN_LENGTH['PASSWORD']:
        return jsonify({'error': f'password too small ({MIN_LENGTH["PASSWORD"]} characters min)'}), 400
    
    
    try:
        user_data = database.create_user(username, password, display_name, about_me)
        
        return jsonify(user_data), 201
    
    except Sqlite3Error as e:
        e_status = e.args[1] if len(e.args) > 1 else 500
        e_msg = e.args[0]
        
        return jsonify({'error': f'database error: {str(e_msg)}'}), e_status

@auth.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'mimetype not supported'}), 415
    
    data = request.get_json()
    
    if not all(key in data for key in REQUIRED_PARAMS):
        return jsonify({'error': 'missing required fields'}), 400
    
    
    username = data['username'].strip()
    password = data['password'].strip()
    
    try:
        user_data = database.authenticate_user(username, password)
        
        return jsonify(user_data), 200
    
    except Sqlite3Error as e:
        e_status = e.args[1] if len(e.args) > 1 else 500
        e_msg = e.args[0]
        
        return jsonify({'error': f'database error: {str(e_msg)}'}), e_status
