import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# INDEX


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as shares FROM stocks WHERE user_id = ? GROUP BY symbol HAVING (SUM(shares)) > 0",
        session["user_id"]
    )

    cash = db.execute(
        "SELECT cash FROM users WHERE id = ?",
        session["user_id"]
    )

    user_cash = cash[0]["cash"]

    total_value = user_cash

    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["price"] = quote["price"]
        stock["name"] = quote["name"]
        stock["total"] = stock["price"] * stock["shares"]
        total_value += stock["total"]

    return render_template("index.html", stocks=stocks, total_value=total_value, user_cash=user_cash)

# BUY


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # input
        symbol = request.form.get("symbol").upper()
        no_of_shares = request.form.get("shares")

        # lookup stock
        stock = lookup(symbol)

        # check validity of stock
        if stock is None:
            return apology("Enter vaild stock.")

        if not no_of_shares:
            return apology("Enter vaild stock.")

        if not no_of_shares.isdigit():
            return apology("Enter vaild stock.")

        # check if user could afford it
        buy_cost = float(stock["price"]) * float(no_of_shares)

        user = db.execute(
            "SELECT cash FROM users WHERE id = ?",
            session["user_id"]
        )
        if buy_cost > user[0]["cash"]:
            return render_template("buy.html", message="Not enough cash.")

        # update database
        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?",
            buy_cost,
            session["user_id"]
        )
        db.execute(
            "INSERT INTO stocks (user_id, symbol, shares, type, price) VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            symbol,
            no_of_shares,
            "Bought",
            buy_cost,
        )

        # return to homepage
        return redirect("/")
    else:
        return render_template("buy.html")

# HISTORY


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    stocks = db.execute(
        "SELECT * FROM stocks WHERE user_id = ?",
        session["user_id"]
    )
    for stock in stocks:
        stock["shares"] = abs(int(stock["shares"]))
        stock["price"] = float(stock["price"])

    return render_template("history.html", stocks=stocks)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username")
        )

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

# QUOTE


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        share = lookup(symbol)

        if share is None:
            return apology("Enter vaild stock.")

        return render_template("quoted.html", price=share["price"], name=share["name"], symbol=share["symbol"])
    else:
        return render_template("quote.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # input
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username")

        # Ensure password was submitted
        elif not password:
            return apology("must provide password")

        # Ensure confirm password match
        elif password != confirmation:
            return apology("passswords don't match")

        # Query database for username
        rows = db.execute(
            "SELECT username FROM users WHERE username = ?",
            username
        )

        # check valid username
        if len(rows) != 0:
            return apology("username already taken")

        # hash password
        hashword = generate_password_hash(password)

        # add into database
        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)",
            username,
            hashword
        )

        # login automatically
        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            username
        )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


# SELL


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        # input
        symbol = request.form.get("symbol")
        no_of_shares = request.form.get("shares")

        # check validity of stock and refresh
        if symbol is None:
            return apology("select a valid symbol")
        if not no_of_shares:
            return apology("enter valid number of shares")

        # change shares from str to int
        no_of_shares = int(no_of_shares)

        # check for valid no of shares
        if no_of_shares < 1:
            return apology("enter positive number of shares")

        # check if user owns shares of the stock
        check_stocks = db.execute(
            "SELECT symbol FROM stocks WHERE user_id = ? AND symbol = ? GROUP BY symbol HAVING (SUM(shares)) > 0",
            session["user_id"],
            symbol
        )[0]

        if symbol != check_stocks["symbol"]:
            return apology("you do not own the selected stock")

        # select the share from database
        stocks = db.execute(
            "SELECT SUM(shares) as shares FROM stocks WHERE user_id = ? AND symbol = ?",
            session["user_id"],
            symbol
        )[0]

        # check if user owns enough shares
        if int(stocks["shares"]) < no_of_shares:
            return apology("not enough shares available")

        # quote the stock
        quote = lookup(symbol)

        # values for database entry
        sell_price = quote["price"] * no_of_shares
        db_no_of_shares = -abs(no_of_shares)

        # update database
        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            sell_price,
            session["user_id"]
        )
        db.execute(
            "INSERT INTO stocks (user_id, symbol, shares, type, price) VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            symbol,
            db_no_of_shares,
            "Sold",
            sell_price,
        )

        # Redirect user to home page
        return redirect("/")

    else:
        stocks = db.execute(
            "SELECT symbol, SUM(shares) as shares FROM stocks WHERE user_id = ? GROUP BY symbol HAVING (SUM(shares)) > 0",
            session["user_id"]
        )

        max_shares = 0

        for stock in stocks:
            quote = lookup(stock["symbol"])
            stock["name"] = quote["name"]
            if stock["shares"] > max_shares:
                max_shares = stock["shares"]

        return render_template("sell.html", stocks=stocks, max_shares=max_shares)

# ADDCASH


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    if request.method == "POST":
        # input
        add_amount = int(request.form.get("addcash"))

        # update database
        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            add_amount,
            session["user_id"]
        )

        return redirect("/addcash")
    else:
        cash = db.execute("SELECT cash FROM users WHERE id = ?",
            session["user_id"]
        )[0]

        user_cash = float(cash["cash"])

        return render_template("addcash.html", user_cash = user_cash)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
