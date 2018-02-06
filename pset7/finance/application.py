import time

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

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


def add_transaction(user_id, symbol, amount, price):
    """Inserts a transaction in to the database"""
    status = db.execute("INSERT INTO transactions (id, symbol, amount, price) VALUES (:id, :symbol, :amount, :price)",
                        id=user_id,
                        symbol=symbol,
                        amount=amount,
                        price=price)

    # Catch DB error
    if not status:
        return apology("DB error on insert transactions")


@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():
    """Allow user to change their passwords"""
    if not request.form or request.method != "POST":
        return render_template("changepass.html")

    # Check for empty fields
    if not request.form["currentpass"] or not request.form["newpass"] or not request.form["confirmnewpass"]:
        return apology("Fields cannot be empty")
    user_id = session["user_id"]

    # Get current hash
    res = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=user_id)
    if not res:
        return apology("DB error")

    # Compare hashes
    if not check_password_hash(res[0]["hash"], request.form["currentpass"]):
        return apology("Wrong password")
    password = request.form["newpass"]

    # Confirm passwords
    if password != request.form["confirmnewpass"]:
        return apology("Passwords do not match")

    # Update DB with new hash
    password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    update_pass = db.execute(
        "UPDATE users SET hash = :password WHERE id = :user_id", password=password, user_id=user_id)

    # Catch DB Error
    if not update_pass:
        return apology("DB error on update password")
    flash("Password Changed")
    return redirect("/")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Get user portfolio and cash
    data = db.execute("SELECT * FROM portfolio WHERE id = :user_id", user_id=user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
    cash = float(cash[0]["cash"])
    total = cash

    # Look up symbols
    for field in data:
        res = lookup(field["symbol"])
        field["price"] = usd(res["price"])
        field["total"] = float(res["price"]) * int(field["amount"])
        total += field["total"]
        field["total"] = usd(field["total"])
    return render_template("index.html", data=data, cash=usd(cash), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if not request.form or request.method != "POST":
        return render_template("buy.html")
    stock = lookup(request.form["symbol"])

    # Check if symbol is valid
    if not stock:
        return apology("Invalid symbol")
    amount = request.form["shares"]

    # Check if amount is valid
    if not amount:
        return apology("Amount must not be empty")
    if not amount.isdigit() or int(amount) <= 0:
        return apology("Invalid amount")
    amount = int(amount)
    user_id = session["user_id"]
    user_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
    user_cash = float(user_cash[0]["cash"])
    symbol = stock["symbol"]
    name = stock["name"]
    price = float(stock["price"])
    cost = price * amount

    # Check if user has sufficient amount
    if cost > user_cash:
        return apology("Insufficient funds")

    # Check if the symbol already exists in DB
    exists = db.execute(
        "SELECT id, symbol FROM portfolio WHERE id = :user_id AND symbol = :symbol", user_id=user_id, symbol=symbol)

    # Create a new row for the symbol
    if len(exists) == 0:
        create_folio_sym = db.execute(
            "INSERT INTO portfolio (id, symbol, name, amount) VALUES (:user_id, :symbol, :name, 0)", user_id=user_id, symbol=symbol, name=name)

        # Catch DB error
        if not create_folio_sym:
            return apology("DB error on create folio")

    # Update fields
    res = db.execute("SELECT amount FROM portfolio WHERE id = :user_id AND symbol = :symbol",
                     user_id=user_id, symbol=symbol)
    update_folio = db.execute("UPDATE portfolio SET amount = :amount WHERE id = :user_id AND symbol = :symbol",
                              user_id=user_id, symbol=symbol, amount=amount + res[0]["amount"])

    # Catch DB error
    if not update_folio:
        return apology("DB error on update folio")

    # Update user cash
    update_cash = db.execute("UPDATE users SET cash = :new_cash WHERE id = :user_id",
                             new_cash=user_cash - cost, user_id=user_id)

    # Catch DB error
    if not update_cash:
        return apology("DB error on update cash")

    # Add transaction
    add_transaction(user_id, symbol, amount, price)
    flash("Bought")
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE id=:user_id ORDER BY time DESC", user_id=session["user_id"])
    return render_template("history.html", transactions=transactions)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        flash('Logged in success')
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
    flash("Logged out")
    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
#@login_required
def quote():
    """Get stock quote."""
    if not request.form or request.method != "POST":
        return render_template("quote.html")

    # Check if symbol is valid
    stock = lookup(request.form["symbol"])
    if not stock:
        return apology("Invalid symbol")
    stock["price"] = usd(stock["price"])
    flash("Quoted")
    return render_template("quoted.html", stock=stock)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if not request.form or request.method != "POST":
        return render_template("register.html")

    # Validate fields
    if not request.form["username"]:
        return apology("Username cannot be empty")
    if not request.form["password"] or not request.form["confirmation"]:
        return apology("Passwords cannot be empty")
    if request.form["password"] != request.form["confirmation"]:
        return apology("Passwords do not match")

    # Insert the new user and hash
    res = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
                     username=request.form["username"],
                     password=generate_password_hash(request.form["password"], method='pbkdf2:sha256', salt_length=8))

    # Catch DB error
    if not res:
        return apology("Username already taken")
    flash("Registered")
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    if not request.form or request.method != "POST":

        # Get avaliable symbols from user to render
        symbols = db.execute(
            "SELECT symbol, amount FROM portfolio WHERE id = :user_id", user_id=user_id)
        return render_template("sell.html", symbols=symbols)

    # Check if symbol is valid
    symbol = request.form["symbol"]
    if not symbol:
        return apology("Invalid symbol")
    amount = request.form["shares"]

    # Validate amount
    if not amount:
        return apology("Amount must not be empty")
    if not amount.isdigit() or int(amount) <= 0:
        return apology("Invalid amount")
    amount = int(amount)

    # Get current shares from user
    res = db.execute("SELECT symbol, amount FROM portfolio WHERE id = :user_id AND symbol = :symbol",
                     user_id=user_id, symbol=symbol)
    if not res or amount > int(res[0]["amount"]):
        return apology("Not enough shares to sell")

    # Update user shares
    new_amount = res[0]["amount"] - amount
    update_folio = db.execute("UPDATE portfolio SET amount = :amount WHERE id = :user_id AND symbol = :symbol",
                              user_id=user_id, symbol=symbol, amount=new_amount)

    # Catch DB error
    if not update_folio:
        return apology("DB error on update folio")

    # Delete row if amount is empty
    if new_amount == 0:
        delete_status = db.execute(
            "DELETE FROM portfolio WHERE id = :user_id AND symbol = :symbol", user_id=user_id, symbol=symbol)

        # Catch DB error
        if not delete_status:
            return apology("DB error on delete folio")

    # Update user cash
    user_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
    user_cash = float(user_cash[0]["cash"])
    price = float(lookup(symbol)["price"])
    update_cash = db.execute("UPDATE users SET cash = :new_cash WHERE id = :user_id", new_cash=user_cash + (amount * price),
                             user_id=user_id)

    # Catch DB error
    if not update_cash:
        return apology("DB error on update cash")

    # Add transaction
    add_transaction(user_id, symbol, -1 * amount, price)
    flash("Sold")
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
