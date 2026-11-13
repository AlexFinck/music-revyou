import db

def add_review(album_title, artist, release_year, rating, review, user_id):
    sql = """INSERT INTO reviews
    (album_title, artist, release_year, rating, review, user_id)
    VALUES (?, ?, ?, ?, ?, ?)"""

    db.execute(sql, [album_title, artist, release_year, rating, review, user_id])

def get_reviews():
    sql = "SELECT id, album_title, artist, rating FROM reviews ORDER BY id DESC"

    return db.query(sql)

def get_review(review_id):
    sql = """SELECT
    u.username,
    r.album_title,
    r.artist,
    r.release_year,
    r.rating,
    r.review
    FROM users u, reviews r
    WHERE u.id = r.user_id
    AND r.id = ?"""
    return db.query(sql, [review_id])[0]