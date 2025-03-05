CREATE TABLE IF NOT EXISTS auths (
    id TEXT PRIMARY KEY NOT NULL,
    
    salt TEXT NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS infos (
    id TEXT PRIMARY KEY NOT NULL,
    
    creation_date REAL NOT NULL,
    username TEXT UNIQUE NOT NULL,
    display_name TEXT,
    description TEXT,
    avatar TEXT,
    
    FOREIGN KEY (id)
    REFERENCES auths (id)
);
