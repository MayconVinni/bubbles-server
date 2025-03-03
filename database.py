import sqlite3
import hashlib
import os

USERS_DB = 'db/users.db'
GUILDS_DB = 'db/guilds.db'


def init_users():
    conn = sqlite3.connect(USERS_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_auth (
        id TEXT PRIMARY KEY NOT NULL,
        salt TEXT NOT NULL,
        hash TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_info (
        id TEXT PRIMARY KEY NOT NULL,
        username TEXT UNIQUE NOT NULL,
        display_name TEXT,
        about_me TEXT,
        FOREIGN KEY (id) REFERENCES user_auth (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def init_guilds():
    conn = sqlite3.connect(GUILDS_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_auth (
        id TEXT PRIMARY KEY NOT NULL,
        salt TEXT NOT NULL,
        hash TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_info (
        id TEXT PRIMARY KEY NOT NULL,
        username TEXT UNIQUE NOT NULL,
        display_name TEXT,
        about_me TEXT,
        FOREIGN KEY (id) REFERENCES user_auth (id)
    )
    ''')
    
    conn.commit()
    conn.close()


def generate_master_key(user_id: str, salt: str, password_hash: str) -> str:
    return '.'.join((
        user_id,
        hashlib.sha1((user_id + salt).encode('utf-8')).hexdigest(),
        hashlib.sha224((salt + salt).encode('utf-8')).hexdigest(),
        hashlib.sha256((password_hash + salt).encode('utf-8')).hexdigest()
    ))

def validate_master_key(master_key: str) -> bool:
    parts = master_key.split('.')
    
    conn = sqlite3.connect(USERS_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT
            auth.salt,
            auth.hash
        FROM
            user_auth auth
        WHERE
            auth.id = ?
    ''', (parts[0],))
    
    result = cursor.fetchone()
    conn.close()
    
    if result is None:
        return False
    
    r_salt = result['salt']
    r_pass_hash = result['hash']
    
    hashed_id = hashlib.sha1((parts[0] + r_salt).encode('utf-8')).hexdigest(),
    hashed_salt = hashlib.sha224((r_salt + r_salt).encode('utf-8')).hexdigest(),
    hashed_hash = hashlib.sha256((r_pass_hash + r_salt).encode('utf-8')).hexdigest()
    
    if parts[1] == hashed_id   and \
       parts[2] == hashed_salt and \
       parts[3] == hashed_hash:
        return True
    
    return False

def create_user(username: str, password: str, display_name: str | None) -> tuple[str, str]:
    user_id = os.urandom(16).hex()
    salt = os.urandom(32).hex()
    password_hash = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    
    conn = sqlite3.connect(USERS_DB)
    cursor = conn.cursor()
    
    cursor.execute('SELECT username FROM user_info WHERE username = ?', (username,))
    if cursor.fetchone():
        raise sqlite3.Error('username already exists', 409)
    
    cursor.execute(
        'INSERT INTO user_auth (id, salt, hash) VALUES (?, ?, ?)',
        (user_id, salt, password_hash)
    )
    
    cursor.execute(
        'INSERT INTO user_info (id, username, display_name, about_me) VALUES (?, ?, ?, NULL)',
        (user_id, username, display_name)
    )
    
    conn.commit()
    conn.close()
    
    master_key = generate_master_key(user_id, salt, password_hash)
    
    return user_id, master_key

def authenticate_user(username: str, password: str) -> tuple[str, str]:
    auth_failed = False
    
    conn = sqlite3.connect(USERS_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT
            auth.id,
            auth.salt,
            auth.hash
        FROM
            user_auth auth
        INNER JOIN
            user_info info ON auth.id = info.id
        WHERE
            info.username = ?
    ''', (username,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result is None:
        auth_failed = True
    else:
        result = dict(result)
        
        user_id = result['id']
        salt = result['salt']
        password_hash = result['hash']
        
        input_hash = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
        
        if input_hash != password_hash:
            auth_failed = True
    
    if auth_failed:
        raise sqlite3.Error('invalid username or incorrect password', 401)
    
    master_key = generate_master_key(user_id, salt, password_hash)
    
    return user_id, master_key
