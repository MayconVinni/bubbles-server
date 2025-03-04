import sqlite3
import hashlib
import time
import os
from . import master_key as mk
from constants import DATABASE, URANDOM_SIZE

def create_guild(master_key, name, description, invite, is_public):
    guild_id = os.urandom(URANDOM_SIZE['GUILD_ID']).hex()
    success, owner_id = mk.validate_masterkey(master_key)
    
    if not success:
        raise sqlite3.Error('invalid master_key', 401)
    
    conn = sqlite3.connect(DATABASE['GUILDS'])
    cursor = conn.cursor()
    
    if invite is not None:
        cursor.execute('''
            SELECT
                info.invite
            FROM
                infos info
            WHERE
                info.invite = ?
        ''', (invite,))
        
        if cursor.fetchone():
            raise sqlite3.Error('invite already used', 409)
    
    creation_date = time.time()
    cursor.execute('''
        INSERT INTO
            infos
            (id, owner_id, creation_date, name, description, invite, is_public)
        VALUES
            (?, ?, ?, ?, ?, ?, ?)
    ''', (guild_id, owner_id, creation_date, name, description, invite, is_public))
    
    conn.commit()
    conn.close()
    
    # TODO: more code
