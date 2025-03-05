import sqlite3
import hashlib
import time
import os
from . import master_key as mk
from constants import DATABASE, URANDOM_SIZE

def create_user(username, password, display_name, description):
    user_id = os.urandom(URANDOM_SIZE['USER_ID']).hex()
    salt = os.urandom(URANDOM_SIZE['SALT']).hex()
    password_hash = hashlib.sha512((password + salt).encode()).hexdigest()
    
    with sqlite3.connect(DATABASE['USERS']) as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO
                auths
                (id, salt, hash)
            VALUES
                (?, ?, ?)
        ''', (user_id, salt, password_hash))
        
        creation_date = time.time()
        
        try:
            cursor.execute('''
                INSERT INTO
                    infos
                    (id, username, display_name, description, creation_date, avatar)
                VALUES
                    (?, ?, ?, ?, ?, NULL)
            ''', (user_id, username, display_name, description, creation_date))
        except sqlite3.IntegrityError:
            raise sqlite3.IntegrityError('username already exists', 409)
        
        conn.commit()
    
    return {
        'master_key': mk.generate_masterkey(user_id, salt, password_hash),
        'user': {
            'id': user_id,
            'creation_date': creation_date,
            'username': username,
            'display_name': display_name,
            'avatar': None,
            'description': description
        }
    }

def authenticate_user(username, password):
    with sqlite3.connect(DATABASE['USERS']) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT
                auth.id,
                auth.salt,
                auth.hash
            FROM
                auths auth
            INNER JOIN
                infos info ON auth.id = info.id
            WHERE
                info.username = ?
        ''', (username,))
        
        auth_result = cursor.fetchone()
        
        if auth_result is None:
            raise sqlite3.Error('invalid username or incorrect password', 401)
        
        user_id = auth_result['id']
        salt = auth_result['salt']
        pass_hash = auth_result['hash']
        
        input_hash = hashlib.sha512((password + salt).encode()).hexdigest()
        if input_hash != pass_hash:
            raise sqlite3.Error('invalid username or incorrect password', 401)
        
        cursor.execute('''
            SELECT
                display_name,
                description,
                avatar,
                creation_date
            FROM
                infos
            WHERE
                username = ?
        ''', (username,))
        
        info_result = cursor.fetchone()
    
    return {
        'master_key': mk.generate_masterkey(user_id, salt, pass_hash),
        'user': {
            'id': user_id,
            'creation_date': info_result['creation_date'],
            'username': username,
            'display_name': info_result['display_name'],
            'avatar': info_result['avatar'],
            'description': info_result['description']
        }
    }


def get_user_info(user_id):
    with sqlite3.connect(DATABASE['USERS']) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT
                creation_date,
                username,
                display_name,
                avatar,
                description
            FROM
                infos
            WHERE
                id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
    
    if result is None:
        return None
    
    return result + {'id': user_id}
