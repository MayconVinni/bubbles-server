DATABASE = {
    'USERS': 'db/users.db',
    'GUILDS': 'db/guilds.db'
}

URANDOM_SIZE = {
    'USER_ID': 16,
    'GUILD_ID': 16, 
    'SALT': 32
}

MAX_LENGTH = {
    'USER_NAME': 25,
    'USER_DISPLAYNAME': 30,
    'USER_ABOUTME': 100,
    
    'GUILD_NAME': 30,
    'GUILD_DESCRIPTION': 200,
    'GUILD_INVITE': 16,
    
    'MEMBER_NICKNAME': 30,
    
    'ROLE_NAME': 25,
    
    'CHANNEL_NAME': 30,
    'CHANNEL_DESCRIPTION': 100,
    
    'MESSAGE_CONTENT': 1000
}

MIN_LENGTH = {
    'PASSWORD': 4,
    'USER_NAME': 3,
    'GUILD_NAME': 1
}

MAX_BYTE_SIZE = {
    #     Byte: 1
    # KiloByte: 1_000
    # MegaByte: 1_000_000
    # GigaByte: 1_000_000_000
    
    'FILE_UPLOAD': 120_000_000,
    'AVATAR': 10_000_000
}
