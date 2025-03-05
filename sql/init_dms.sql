CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY NOT NULL,
    sender_id TEXT NOT NULL,
    recipient_id TEXT NOT NULL,
    
    timestamp REAL NOT NULL,
    salt TEXT NOT NULL,
    content TEXT,
    edited BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS attachments (
    id TEXT PRIMARY KEY NOT NULL,
    message_id TEXT NOT NULL,
    
    salt TEXT NOT NULL,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    
    FOREIGN KEY (message_id)
    REFERENCES messages (id)
);
