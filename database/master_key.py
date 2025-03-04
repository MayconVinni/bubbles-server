import sqlite3
import hashlib
from constants import DATABASE

def generate_masterkey(user_id, salt, password_hash):
    return '.'.join((
        user_id,
        hashlib.sha1((user_id + salt).encode()).hexdigest(),
        hashlib.sha224((salt + salt).encode()).hexdigest(),
        hashlib.sha256((password_hash + salt).encode()).hexdigest()
    ))

def validate_masterkey(master_key):
    parts = master_key.split('.')
    
    with sqlite3.connect(DATABASE['USERS']) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT
                auth.salt,
                auth.hash
            FROM
                auths auth
            WHERE
                auth.id = ?
        ''', (parts[0],))
        
        result = cursor.fetchone()
    
    if result is not None:
        salt = result['salt']
        pass_hash = result['hash']
        
        hashed_id = hashlib.sha1((parts[0] + salt).encode()).hexdigest(),
        hashed_salt = hashlib.sha224((salt + salt).encode()).hexdigest(),
        hashed_hash = hashlib.sha256((pass_hash + salt).encode()).hexdigest()
        
        if parts[1] == hashed_id   and \
           parts[2] == hashed_salt and \
           parts[3] == hashed_hash:
            return True, parts[0]
    
    return False, None
