import database
import re
from flask import Blueprint, request, jsonify
from sqlite3 import Error as Sqlite3Error
from constants import MAX_LENGTH, MIN_LENGTH, REGEX

REQUIRED_PARAMS = ['username', 'password']
auth = Blueprint('auth', __name__, url_prefix='/auth')

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
    description = data.get('description')
    
    if len(username) > MAX_LENGTH['USER_NAME'] or \
       len(username) < MIN_LENGTH['USER_NAME']:
        return jsonify({'error': f'username too big or small ({MIN_LENGTH["USER_NAME"]}-{MAX_LENGTH["USER_NAME"]} characters)'}), 400
    
    elif not re.match(REGEX['LIMITED_CHARACTERS'], username):
        return jsonify({'error': f'username {REGEX["LIMITED_CHARACTERS_ERROR"]}'}), 400
    
    if len(password) < MIN_LENGTH['PASSWORD']:
        return jsonify({'error': f'password too small ({MIN_LENGTH["PASSWORD"]} characters min)'}), 400
    
    if display_name is not None:
        display_name = display_name.strip()
        
        if len(display_name) > MAX_LENGTH['USER_DISPLAYNAME'] or len(display_name) < 1:
            return jsonify({'error': f'display_name too big or small (max: {MAX_LENGTH["USER_DISPLAYNAME"]})'}), 400
    
    if description is not None:
        description = description.strip()
        
        if len(description) > MAX_LENGTH['USER_DESCRIPTION'] or len(description) < 1:
            return jsonify({'error': f'description too big or small (max: {MAX_LENGTH["USER_DESCRIPTION"]})'}), 400
    
    
    try:
        user_data = database.create_user(username, password, display_name, description)
        
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
    
    if len(username) < 1 or len(password) < 1:
        return jsonify({'error': 'username or/and password empty'}), 400
    
    try:
        user_data = database.authenticate_user(username, password)
        
        return jsonify(user_data), 200
    
    except Sqlite3Error as e:
        e_status = e.args[1] if len(e.args) > 1 else 500
        e_msg = e.args[0]
        
        return jsonify({'error': f'database error: {str(e_msg)}'}), e_status
