from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from helpers import login_required, lookup

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOADED"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///users.db")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login2.html")
    else:
        username = request.form.get("name")
        password = request.form.get("password")

        if not username:
            flash("Please type username")
            return render_template("login2.html")

        elif not password:
            flash("Please type password")
            return render_template("login2.html")

        row = db.execute("SELECT * from users WHERE username = ?", username)

        if len(row) != 1 or not check_password_hash(row[0]["password"], password):
            flash("invalid username/password")
            return render_template("login2.html")

        session["user_id"] = row[0]["id"]
        return redirect("/anime")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    else:
        name = request.form.get("name")
        passwords = request.form.get("password")
        repassword = request.form.get("repassword")

        if not name:
            flash("Please input name")
            return render_template("signup.html")

        elif not passwords:
            flash("Please input password")
            return render_template("signup.html")

        elif not repassword:
            flash("Please retype password confirmation")
            return render_template("signup.html")

        if passwords != repassword:
            flash("Unmatched password, please try again")
            return render_template("signup.html")


        password = generate_password_hash(passwords)

        try:
            new_user = db.execute("INSERT INTO users (username, password) VALUES(?, ?)", name, password)
        except:
            flash("Username already exists")

        session["user_id"] = new_user
        return redirect("/anime")

@app.route("/anime")
@login_required
def anime():
    return render_template("anime.html")

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")

@app.route("/rateanime")
def rate():

    return render_template("rateme.html")

@app.route("/back")
def back():
    return redirect("/")

@app.route("/animeinfo")
def info():
    name = request.form.get("title")
    anime = lookup(name)

    db.execute("INSERT INTO anime (title) VALUES (?)", name)
    return render_template("animeinfo.html", title = anime["name"], image = anime["image"], synopsis = anime["sypnosis"])


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/developer")
def developer():
    return render_template("homepage.1.html")



