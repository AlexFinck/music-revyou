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
    r.user_id,
    u.username,
    r.id,
    r.album_title,
    r.artist,
    r.release_year,
    r.rating,
    r.review
    FROM users u, reviews r
    WHERE u.id = r.user_id
    AND r.id = ?"""
    return db.query(sql, [review_id])[0]

def update_review(review_id, album_title, artist, release_year, rating, review):
    sql = """UPDATE reviews SET album_title = ?,
    artist = ?,
    release_year = ?,
    rating = ?,
    review = ?
    WHERE id = ?"""
    db.execute(sql, [album_title, artist, release_year, rating, review, review_id])

def remove_review(review_id, user_id):
    sql = """DELETE FROM reviews WHERE id = ? AND user_id = ?"""
    db.execute(sql, [review_id, user_id])

def search_reviews(query):
    sql = """SELECT 
    id, 
    album_title
    FROM reviews
    WHERE album_title LIKE ? OR artist LIKE ?
    ORDER BY id DESC"""
    like = "%" + query + "%"

    return db.query(sql, ["%" + query + "%", "%" + query + "%"])
    
