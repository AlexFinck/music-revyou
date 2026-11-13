import db

def add_review(album_title, artist, release_year, rating, review, user_id):
    sql = """INSERT INTO reviews
    (album_title, artist, release_year, rating, review, user_id)
    VALUES (?, ?, ?, ?, ?, ?)"""

    db.execute(sql, [album_title, artist, release_year, rating, review, user_id])
