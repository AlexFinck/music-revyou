import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []

    for title, value in result:
        classes[title].append(value)

    return classes

def add_review(album_title, artist, release_year, rating, review, user_id, classes):
    sql = """INSERT INTO reviews
    (album_title, artist, release_year, rating, review, user_id)
    VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [album_title, artist, release_year, rating, review, user_id])

    review_id = db.last_insert_id()

    sql = "INSERT INTO review_classes (review_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [review_id, title, value])

def get_classes(review_id):
    sql = "SELECT title, value FROM review_classes WHERE review_id = ?"
    return db.query(sql, [review_id])

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
    result = db.query(sql, [review_id])
    return result[0] if result else None

def update_review(review_id, album_title, artist, release_year, rating, review, classes):
    connection = db.get_connection()

    try:
        with connection:
            sql = """UPDATE reviews
                     SET album_title = ?, artist = ?, release_year = ?, rating = ?, review = ?
                     WHERE id = ?"""
            connection.execute(sql, [album_title, artist, release_year, rating, review, review_id])

            sql = "DELETE FROM review_classes WHERE review_id = ?"
            connection.execute(sql, [review_id])

            sql = "INSERT INTO review_classes (review_id, title, value) VALUES (?, ?, ?)"
            for title, value in classes:
                connection.execute(sql, [review_id, title, value])
    finally:
        connection.close()

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
    
def add_comment(review_id, user_id, body):
    sql = "INSERT INTO comments (review_id, user_id, body) VALUES (?, ?, ?)"
    db.execute(sql, [review_id, user_id, body])


def get_comments(review_id):
    sql = """SELECT comments.body, users.id AS user_id, users.username
             FROM comments JOIN users ON comments.user_id = users.id
             WHERE comments.review_id = ?
             ORDER BY comments.id DESC"""
    return db.query(sql, [review_id])