CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    price INTEGER NOT NULL,
    description TEXT,
    condition TEXT,
    height INTEGER NOT NULL,
    width INTEGER NOT NULL,
    length INTEGER NOT NULL,
    weight_maj INTEGER NOT NULL,
    weight_min INTEGER NOT NULL,
    pictures INTEGER,
    illustrator TEXT,
    genre TEXT,
    publisher TEXT,
    publication_year TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id) 
);

CREATE TABLE IF NOT EXISTS user_tokens (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    token INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);