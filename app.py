import sqlite3
from flask import Flask
from flask import url_for, abort, redirect, render_template, request, session, flash
import config
import users
import reviews
from datetime import date
from secrets import compare_digest, token_hex


app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_reviews = reviews.get_reviews()
    return render_template("index.html", reviews=all_reviews)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user_by_id(user_id)
    if user is None:
        abort(404)

    user_reviews = users.get_reviews_by_user(user_id)
    return render_template("show_user.html", user=user, reviews=user_reviews)

@app.route("/search_review")
def search_review():
    query = request.args.get("query")

    if query:
        results = reviews.search_reviews(query)

    else:
        query = ""
        results = []

    return render_template("search_review.html", query=query, results=results)

@app.route("/review/<int:review_id>")
def show_review(review_id):
    review = reviews.get_review(review_id)
    if not review:
        abort(404)

    classes = reviews.get_classes(review_id)
    comments = reviews.get_comments(review_id)

    return render_template(
        "show_review.html", review=review, classes=classes, comments=comments
    )


@app.route("/create_comment", methods=["POST"])
def create_comment():
    user_id = require_login()
    check_csrf()

    review_id = request.form.get("review_id", type=int)
    if review_id is None or reviews.get_review(review_id) is None:
        abort(404)

    body = request.form.get("comment", "").strip()
    if not body or len(body) > 500:
        flash("Enter a comment between 1 and 500 characters.", "comment")
    else:
        try:
            reviews.add_comment(review_id, user_id, body)
        except sqlite3.IntegrityError as error:
            if error.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_FOREIGNKEY:
                abort(404)
            raise

    return redirect(url_for("show_review", review_id=review_id, _anchor="comments"))

def check_csrf():
    token = session.get("csrf_token")
    submitted = request.form.get("csrf_token", "")
    if not token or not compare_digest(token.encode(), submitted.encode()):
        abort(403)



def require_login():
    user_id = session.get("user_id")
    if user_id is None:
        abort(403)
    return user_id

@app.route("/new_review")
def new_review():
    require_login()
    classes = reviews.get_all_classes()
    return render_template("new_review.html", classes=classes)

@app.route("/submit_review", methods=["POST"])
def submit_review():
    user_id = require_login()
    check_csrf()
    album_title = request.form["album_title"]
    artist = request.form["artist"]
    release_year = request.form["release_year"]
    rating = request.form["rating"]
    review = request.form["review"]

    classes = [
        entry.split(":", 1)
        for entry in request.form.getlist("classes")
        if entry
    ]

    error = validate_review(album_title, artist, release_year, rating, review, classes)
    if error:
        flash(error)
        return redirect("/new_review")

    release_year = int(release_year)
    rating = int(rating)

    reviews.add_review(album_title, artist, release_year, rating, review, user_id, classes)

    return redirect("/")

@app.route("/edit_review/<int:review_id>")
def edit_review(review_id):
    review = reviews.get_review(review_id)

    if not review:
        abort(404)

    if session.get("user_id") != review["user_id"]:
        abort(403)

    all_classes = reviews.get_all_classes()
    classes = {title: [] for title in all_classes}

    for entry in reviews.get_classes(review_id):
        classes.setdefault(entry["title"], []).append(entry["value"])

    return render_template(
        "edit_review.html",
        review=review,
        classes=classes,
        all_classes=all_classes,
    )


@app.route("/remove_review/<int:review_id>", methods=["GET", "POST"])
def remove_review(review_id):
    review = reviews.get_review(review_id)
    user_id = session.get("user_id")

    if not review:
        abort(404)

    if user_id != review["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_review.html", review=review)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            reviews.remove_review(review_id, session["user_id"])
            return redirect("/")

        else:
            return redirect("/review/" + str(review_id))



@app.route("/update_review", methods=["POST"])
def update_review():
    require_login()
    check_csrf()    
    review_id = request.form["review_id"]
    review = reviews.get_review(review_id)

    if not review:
        abort(404)

    if session.get("user_id") != review["user_id"]:
        abort(403)

    album_title = request.form["album_title"]
    artist = request.form["artist"]
    release_year = request.form["release_year"]
    rating = request.form["rating"]
    review = request.form["review"]

    classes = [
        entry.split(":", 1)
        for entry in request.form.getlist("classes")
        if entry
    ]

    error = validate_review(album_title, artist, release_year, rating, review, classes)
    if error:
        flash(error)
        return redirect("/edit_review/" + str(review_id))

    release_year = int(release_year)
    rating = int(rating)

    reviews.update_review(review_id, album_title, artist, release_year, rating, review, classes)

    return redirect("/review/" + str(review_id))

def validate_review(album_title, artist, release_year, rating, review, classes):
    album_title = album_title.strip()
    artist = artist.strip()

    if not album_title:
        return "Enter an album title."
    if len(album_title) > 200:
        return "Album title must be 200 characters or fewer."

    if not artist:
        return "Enter an artist."
    if len(artist) > 200:
        return "Artist must be 200 characters or fewer."

    if classes:
        all_classes = reviews.get_all_classes()
        seen_choices = set()

        for parts in classes:
            if len(parts) != 2 or parts[0] not in all_classes:
                return "Choose a valid genre or language."

            title, value = parts
            if value not in all_classes[title]:
                return f"Choose a valid {title.lower()}."

            choice = (title, value)
            if choice in seen_choices:
                return f"Choose each {title.lower()} only once."
            seen_choices.add(choice)

    try:
        release_year = int(release_year)
    except ValueError:
        return "Release year must be a whole number."

    current_year = date.today().year
    if not 1900 <= release_year <= current_year:
        return f"Release year must be between 1900 and {current_year}."

    try:
        rating = int(rating)
    except ValueError:
        return "Rating must be a whole number."

    if not 1 <= rating <= 10:
        return "Rating must be between 1 and 10."

    if len(review.split()) > 500:
        return "Review must be 500 words or fewer."

    return None

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        flash("The passwords don't match")
        return redirect("/register")

    try:
        users.create_user(username, password1)

    except sqlite3.IntegrityError:
        flash("Username already taken")
        return redirect("/register")

    flash("Account created succesfully!")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]
    user_id = users.check_login(username, password)

    if user_id is None:
        flash("Wrong username or password")
        return redirect("/login")

    session["user_id"] = user_id
    session["username"] = username
    session["csrf_token"] = token_hex(16)
    return redirect("/")

@app.route("/logout", methods=["POST"])
def logout():
    require_login()
    check_csrf()
    session.clear()
    return redirect("/")

