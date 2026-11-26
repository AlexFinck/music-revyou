CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    album_title TEXT NOT NULL,
    artist TEXT NOT NULL,
    release_year INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 10),
    review TEXT,
    user_id INTEGER NOT NULL REFERENCES users
);

CREATE TABLE review_classes (
    id INTEGER PRIMARY KEY,
    review_id INTEGER NOT NULL REFERENCES reviews(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    value TEXT NOT NULL
);