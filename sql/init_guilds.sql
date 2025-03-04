CREATE TABLE IF NOT EXISTS infos (
    id TEXT PRIMARY KEY NOT NULL,
    owner_id TEXT NOT NULL,
    creation_date REAL NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    invite TEXT UNIQUE,
    is_public BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS members (
    id TEXT PRIMARY KEY NOT NULL,
    guild_id TEXT NOT NULL,
    nickname TEXT,
    
    FOREIGN KEY (guild_id)
    REFERENCES infos (id)
);

CREATE TABLE IF NOT EXISTS roles (
    id TEXT PRIMARY KEY NOT NULL,
    guild_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color INTEGER,
    
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
    content TEXT NOT NULL,
    datetime REAL NOT NULL,
    
    FOREIGN KEY (channel_id)
    REFERENCES channels (id)
);
