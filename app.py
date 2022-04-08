import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]



    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = user_cash[0]["cash"]

    transaction = db.execute("SELECT symbol, SUM(shares) AS shares, price, total FROM transactions GROUP BY symbol")
    return render_template("transaction.html", transaction = transaction, cash = cash)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        symbol = request.form.get("symbol").upper()

        if not symbol:
            return apology("Must give symbol")

        shares = int(request.form.get("shares"))

        if not shares:
            return apology("Must give shares")

        if shares < 0:
            return apology("Must not provide negative number")

        stocks = lookup(symbol)

        if stocks == None:
            return apology("No symbol found")

        transaction_value = shares * stocks["price"]

        user_id = session["user_id"]

        cash_value_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

        user_cash = cash_value_db[0]["cash"]
        if user_cash < transaction_value:
            return apology("no enough money")

        buy = "buy"

        update = user_cash - transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update, user_id)

        date = datetime.datetime.now()
        buy = "buy"
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, date, total, type) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", user_id, stocks["symbol"], stocks["name"], shares, stocks["price"], date, shares * stocks["price"], buy)
        db.execute("INSERT INTO buy (user_id, symbol, name, shares, price, date, type) VALUES(?, ?, ?, ?, ?, ?, ?)", user_id, stocks["symbol"], stocks["name"], shares, stocks["price"], date, buy)
        flash("Bought")

        return redirect("/")

@app.route("/addcash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash"""
    if request.method == "GET":
        return render_template("addcash.html")

    else:
        user_id = session["user_id"]
        user_cash = int(request.form.get("cash"))

        cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = cash_db[0]["cash"]

        value = cash + user_cash

        db.execute("UPDATE users SET cash = ? WHERE id = ?", value, user_id)

        return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]

    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)

    return render_template("history.html", transactions = transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")

    else:
        symbol = request.form.get("symbol").upper()

        if not symbol:
            return apology("Must give symbol")

        stocks = lookup(symbol)

        if stocks == None:
            return apology("No symbol found")

        return render_template("quoted.html", name = stocks["name"], price = stocks["price"], symbol = stocks["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":

        if not username:
            return apology("Must provide username")

        elif not password:
            return apology("Must provide password")

        elif not confirmation:
            return apology("Must provide password confirmation")

        if password != confirmation:
            return apology("Must provide exact password in confrimation")

        hashs = generate_password_hash(password)
        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashs)
        except:
            return apology("Username already exists")

        session["user_id"] = new_user
        return redirect("/")

    elif request.method == "GET":
        return render_template("registration.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbol_db = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", symbol = [row["symbol"] for row in symbol_db])

    else:
        user_id = session["user_id"]
        shares = int(request.form.get("shares"))
        symbol = request.form.get("symbol").upper()
        stocks = lookup(symbol)

        if not symbol:
            return apology("Please enter symbol name")

        share = (db.execute("SELECT shares FROM transactions WHERE symbol = ? AND user_id = ?", symbol, user_id))

        if not share:
            return apology("Invalid stock")

        if shares < 0:
            return apology("No negative integer")

        date = datetime.datetime.now()

        sell = "sell"
        price = stocks["price"] - stocks["price"]

        db.execute("INSERT INTO sell (user_id, symbol, shares, price, name, date, type) VALUES ( ?, ?, ?, ?, ?, ?, ?)", user_id, symbol, shares, stocks["price"], stocks["name"], date, sell)
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, date, total, type) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", user_id, stocks["symbol"], stocks["name"], (-1)*shares, stocks["price"], date, price, sell)


        cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = cash_db[0]["cash"]

        value = cash + (shares * stocks["price"])

        db.execute("UPDATE users SET cash = ? WHERE id = ?", value, user_id)

        flash("Sold")
        return redirect("/")