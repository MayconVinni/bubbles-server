CREATE TABLE IF NOT EXISTS infos (
    id TEXT PRIMARY KEY NOT NULL,
    owner_id TEXT NOT NULL,
    
    creation_date REAL NOT NULL,
    icon TEXT,
    name TEXT NOT NULL,
    description TEXT,
    invite TEXT UNIQUE,
    invite_only BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS members (
    id TEXT PRIMARY KEY NOT NULL,
    guild_id TEXT NOT NULL,
    
    join_date REAL NOT NULL,
    nickname TEXT,
    muted BOOLEAN NOT NULL DEFAULT FALSE,
    
    FOREIGN KEY (guild_id)
    REFERENCES infos (id)
);

CREATE TABLE IF NOT EXISTS roles (
    id TEXT PRIMARY KEY NOT NULL,
    guild_id TEXT NOT NULL,
    
    name TEXT NOT NULL,
    color INTEGER NOT NULL,
    
    FOREIGN KEY (guild_id)
    REFERENCES infos (id)
);

CREATE TABLE IF NOT EXISTS channels (
    id TEXT PRIMARY KEY NOT NULL,
    guild_id TEXT NOT NULL,
    
    type INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    
    FOREIGN KEY (guild_id)
    REFERENCES infos (id)
);

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY NOT NULL,
    channel_id TEXT NOT NULL,
    
    timestamp REAL NOT NULL,
    content TEXT NOT NULL,
    edited BOOLEAN NOT NULL DEFAULT FALSE,
    
    FOREIGN KEY (channel_id)
    REFERENCES channels (id)
);

CREATE TABLE IF NOT EXISTS attachments (
    id TEXT PRIMARY KEY NOT NULL,
    message_id TEXT NOT NULL,
    
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    
    FOREIGN KEY (message_id)
    REFERENCES messages (id)
);
