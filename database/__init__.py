import sqlite3
from constants import DATABASE

from .guilds import create_guild
from .master_key import generate_masterkey, validate_masterkey
from .users import create_user, authenticate_user

def init():
    FILES = [
        (DATABASE['USERS'], 'sql/init_users.sql'),
        (DATABASE['GUILDS'], 'sql/init_guilds.sql')
    ]
    
    for FILE in FILES:
        db_path = FILE[0]
        sql_path = FILE[1]
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            with open(sql_path) as sql_file:
                sql_content = sql_file.read()
            
            cursor.executescript(sql_content)
            
            conn.commit()
