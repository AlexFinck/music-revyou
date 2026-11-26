import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import config
import users
import reviews
from datetime import date

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

    return render_template("show_review.html", review=review)

@app.route("/new_review")
def new_review():
    return render_template("new_review.html")

@app.route("/submit_review", methods=["POST"])
def submit_review():
    album_title = request.form["album_title"]
    artist = request.form["artist"]
    release_year = request.form["release_year"]
    rating = request.form["rating"]
    review = request.form["review"]
    user_id = session["user_id"]

    error = validate_review(album_title, artist, release_year, rating, review)

    if error:
        flash(error)
        return redirect("/new_review")

    release_year = int(release_year)
    rating = int(rating)

    reviews.add_review(album_title, artist, release_year, rating, review, user_id)

    return redirect("/")

@app.route("/edit_review/<int:review_id>")
def edit_review(review_id):
    review = reviews.get_review(review_id)

    if not review:
        abort(404)

    if session.get("user_id") != review["user_id"]:
        abort(403)
    return render_template("edit_review.html", review = review)


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
        if "remove" in request.form:
            reviews.remove_review(review_id, session["user_id"])
            return redirect("/")
        
        else:
            return redirect("/review/" + str(review_id))



@app.route("/update_review", methods=["POST"])
def update_review():
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

    error = validate_review(album_title, artist, release_year, rating, review)

    if error:
        flash(error)
        return redirect("/edit_review/" + str(review_id))

    release_year = int(release_year)
    rating = int(rating)


    reviews.update_review(review_id, album_title, artist, release_year, rating, review)

    return redirect("/review/" + str(review_id))

def validate_review(album_title, artist, release_year, rating, review):
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
    password_hash = generate_password_hash(password1)

    try:
        users.create_user(username, password_hash)
    
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

    result = users.get_user(username)

    if result is None:
        flash("Wrong username or password")
        return redirect("/login")

    user_id = result["id"]
    password_hash = result["password_hash"]

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        flash("Wrong username or password")
        return redirect("/login")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

