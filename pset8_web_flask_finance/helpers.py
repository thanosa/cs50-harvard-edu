import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def list_symbols():
    """Returns a list of the symbols and the company name."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/ref-data/symbols?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        symbols = response.json()
        return symbols
    except (KeyError, TypeError, ValueError):
        return None


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def user_exists(db, username):
    """Checks if a user already exists."""

    sql = """
        SELECT username
        FROM users
        WHERE username = :username"""

    rows = db.execute(sql, username=username)
    user_exists = len(rows) == 1

    return user_exists


def add_user(db, username, password):
    """ Add a user. The password is hashed."""

    # Calculates the password hash.
    password_hash = generate_password_hash(password)

    # Add the user to the database and return the user id.
    sql = """
        INSERT INTO users (username, hash)
        VALUES (:username, :password_hash)"""

    user_id = db.execute(sql, username=username, password_hash=password_hash)

    return user_id


def get_user(db, username):
    """Return user information based on a username."""

    sql = """
        SELECT *
        FROM users
        WHERE username = :username"""

    user = db.execute(sql, username=username)

    return user


def get_cash(db, user_id):
    """Returns the cash value for a user."""

    sql = """
        SELECT cash
        FROM users
        WHERE id = :user_id"""

    response = db.execute(sql, user_id=user_id)

    # Check if the user exists.
    if len(response) != 1:
        return apology("User not found", 403)

    # Converts the cash to float.
    cash = float(response[0]["cash"])

    return cash


def get_portfolio(db, user_id):
    """Return information about a user's portfolio."""

    sql = """
        SELECT symbol, SUM(quantity) AS sum_quantity
        FROM history
        WHERE userid = :user_id
        GROUP BY symbol
        HAVING sum_quantity > 0 """

    portfolio = db.execute(sql, user_id=user_id)

    return portfolio


def get_symbol_quantity(db, user_id, symbol):
    """Returns the quantity of a symbol a user has in his portfolio."""

    # Validate that the user has available stocks to sell.
    sql = """
        SELECT SUM(quantity) AS sum_quantity
        FROM history
        WHERE userid = :user_id AND symbol = :symbol"""

    response = db.execute(sql, user_id=user_id, symbol=symbol)

    symbol_quantity = response[0]["sum_quantity"]

    return symbol_quantity


def get_transactions(db, user_id):
    """Returns the transactions of a user."""

    sql = """SELECT symbol,
        CASE WHEN quantity < 0
            THEN 'Sell'
            ELSE 'Buy'
        END AS action,
        abs(quantity) as quantity, price, transacted
        FROM history
        WHERE userid = :user_id"""

    transactions = db.execute(sql, user_id=user_id)

    return transactions


def register_transaction(db, user_id, cash, symbol, quantity, price, value):
    """Registers a transaction to the database."""

    # Start a transaction with the database.
    db.execute("BEGIN TRANSACTION")

    # First, update the user's available cash.
    response = set_cash(db, user_id, cash)

    # If the update has not been done then rollback.
    if response != 1:
        db.execute("ROLLBACK")
        return False

    # Record the transaction in the history table.
    sql = """
        INSERT INTO
        history (userid, symbol, quantity, price, value)
        VALUES (:userid, :symbol, :quantity, :price, :value)"""

    db.execute(sql, userid=user_id, symbol=symbol, quantity=quantity, price=price, value=value)

    # Commit since everything is ok.
    db.execute("COMMIT")

    return True


def set_cash(db, user_id, cash):
    """ Updates the user's cash."""
    sql = """
        UPDATE users
        SET cash = :cash
        WHERE id = :user_id"""

    response = db.execute(sql, cash=cash, user_id=user_id)

    return response
