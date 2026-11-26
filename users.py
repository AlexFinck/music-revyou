import db
from werkzeug.security import check_password_hash, generate_password_hash

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def get_user(username):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if result:
        return result[0]
    else:
        return None

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user = result[0]
    if check_password_hash(user["password_hash"], password):
        return user["id"]

    return None

def get_user_by_id(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_reviews_by_user(user_id):
    sql = """SELECT id, album_title, artist, rating
             FROM reviews
             WHERE user_id = ?
             ORDER BY id DESC"""
    return db.query(sql, [user_id])