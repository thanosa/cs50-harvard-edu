import logging
import os
import random

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Make sure the API KEY has been sen in the environment.
assert len(os.environ.get("API_KEY")) == 35

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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks."""

    # Shortcut variables.
    user_id = session["user_id"]

    # Get the user's cash.
    cash = get_cash(db, user_id)

    # Get the portfolio information about the user aggregated per symbol.
    stocks = get_portfolio(db, user_id)

    # Looks up the company names based on the symbols.
    portfolio_value = 0
    for stock in stocks:
        # Look up the symbol data.
        symbol_data = lookup(stock["symbol"])

        # Calculate the stock value.
        quantity = float(stock["sum_quantity"])
        price = float(symbol_data["price"])
        stock_value = round(quantity * price, 2)

        # Sums up the total portfolio value.
        portfolio_value += stock_value

        # Saves the name and the price and the value
        stock["name"] = symbol_data["name"]
        stock["price"] = "$ {:.2f}".format(price)
        stock["value"] = "$ {:.2f}".format(stock_value)

    # The user's total is the portfolio value plus the available cash on hand.
    total = "$ {:.2f}".format(portfolio_value + cash)

    # Format cash with 2 decimals
    cash = "$ {:.2f}".format(cash)

    return render_template("index.html", stocks=stocks, cash=cash, total=total)


@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    # Shortcut variables.
    user_id = session["user_id"]

    # Get the user's transactions from the history table.
    stocks = get_transactions(db, user_id)

    # Sets the format of the values.
    for stock in stocks:
        stock["price"] = "$ {:.2f}".format(stock["price"])

    return render_template("history.html", stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Shortcut variables.
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted.
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted.
        elif not password:
            return apology("must provide password", 403)

        # Query database for a username.
        user = get_user(db, username)

        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in.
        session["user_id"] = user[0]["id"]
        session["username"] = username

        # Redirect user to home page.
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # Clean up the session.
    session.clear()

    # Redirect user to login form.
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # Shortcut variables
    me = "quote.html"

    # Samples symbols randomly.
    SAMPLE_SIZE = 5
    sample_symbols = random.sample(list_symbols(), SAMPLE_SIZE)

    if request.method == "GET":
        # Renders the quote template listing the random symbols.
        return render_template(me, symbols=sample_symbols)
    else:
        # Looks up the quote for the symbol entered by the user.
        symbol = request.form.get("symbol")

        # If the symbol is None then something wrong happended.
        if symbol == None:
            return apology(f"Symbol is None")

        # If the symbol has bigger length then inform the user.
        if len(symbol) > 6:
            flash(f"Invalid symbol: {symbol}", "danger")
            return redirect("/quote")

        # Lookup the quote for the symbol via the API.
        quote = lookup(symbol)

        # Check if the quote is valid.
        if quote == None:
            return apology(f"Symbol not found: {symbol}")

        return render_template(me, quote=quote, symbols=sample_symbols)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Shortcut variables
    me = "register.html"

    if request.method == "GET":
        return render_template(me)
    else:
        # The validations have been done in the front end as well.
        # These checks are needed for cases where the users has
        # deactivated the js on the browser.

        # Shortcut variables.
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if the user entered a username.
        if not username:
            return apology("must provide username", 400)

        # Check if the user entered a password.
        elif not password:
            return apology("must provide password", 400)

        # Check if the user entered a confirmation.
        elif not confirmation:
            return apology("must provide confirmation", 400)

        # Check if the password matches the confirmation.
        if password != confirmation:
            return apology("password and confirmation must match", 400)

        # Check if there is a registered user with the same user name.
        rows = db.execute("SELECT username FROM users WHERE username = :username", username=username)
        if len(rows) == 1:
            flash("username already exists", "danger")
            return render_template(me)
        else:
            # Add the user.
            user_id = add_user(db, username, password)

            # Extra validation that user has been created.
            if not user_id:
                return apology(f"Error in registering the user: {username}", 400)

            # Store the user id on the session.
            session["user_id"] = user_id

            # Confirmation message for the user registration.
            flash(f"New user has been created: {username}", "primary")

            # Redirect user to home page
            return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # Shortucut variables
    me = "buy.html"

    if request.method == "GET":
        return render_template(me)
    else:
        # Shortcut variables
        user_id = session["user_id"]
        symbol = request.form.get("symbol")
        quantity = int(request.form.get("quantity"))

        # Lookup the symbol data and checks if the symbol is valid.
        symbol_data = lookup(symbol)
        if symbol_data == None:
            return apology("Symbol not found", 400)

        # Retrieves the price to calculate the value.
        price = float(symbol_data["price"])
        value = round(quantity * price, 2)

        # Retrieves the user's cash.
        cash = get_cash(db, user_id)

        # Check if the cash is enough.
        cash_new = round(cash - value, 2)
        if cash_new < 0:
            return apology("Not enough cash", 406)

        # Register the transaction
        response = register_transaction(db, user_id, cash_new, symbol, quantity, price, value)

        # If failed report to the user
        if not response:
            flash("Transaction has not completed.", "danger")
            return render_template(me, stocks=stocks)

        # Inform the user about the outcome.
        flash(f"Transaction completed. Purchase value: $ {value}. Available cash: $ {cash_new}", "primary")
        return render_template(me)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Shorcut variable.
    user_id = session["user_id"]
    me = "sell.html"

    # Retrieves all the symbols from the stocks the user has available quantity
    stocks = get_portfolio(db, user_id)

    if request.method == "GET":
        return render_template(me, stocks=stocks)
    else:
        # Get the user's entries
        symbol = request.form.get("symbol")
        quantity = int(request.form.get("quantity"))

        # Validate that the user has available stocks to sell.
        available = get_symbol_quantity(db, user_id, symbol)
        if quantity > available:
            return apology("Not enough shares", 406)

        # Look up the symbol data.
        symbol_data = lookup(symbol)

        # Calculate the selling value.
        price = float(symbol_data["price"])
        value = round(quantity * price, 2)

        # Caclulate the new cash value.
        cash = get_cash(db, user_id)
        cash_new = round(cash + value, 2)

        # Register the transaction. The quentity should be negative.
        response = register_transaction(db, user_id, cash_new, symbol, -1 * quantity, price, value)

        # If failed report to the user
        if not response:
            flash("Transaction has not completed.", "danger")
            return render_template(me, stocks=stocks)

        # Inform the user about the outcome.
        flash(f"Transaction completed. Selling value: $ {value}. Available cash: $ {cash_new}", "primary")

        # We should retrieve the stock symbols again as the user might have sold all of a kind.
        stocks = get_portfolio(db, user_id)
        return render_template(me, stocks=stocks)


@app.route("/cash", methods=["GET", "POST"])
def cash():
    """Let's the user add more cash."""

    # Shorcut variable.
    user_id = session["user_id"]

    if request.method == "GET":
        return render_template("cash.html")
    else:
        # Gets the cash user wants to add.
        added_cash = int(request.form.get("quantity"))

        # Caclulate the new cash value.
        cash = get_cash(db, user_id)
        cash_new = round(cash + added_cash, 2)

        # Set the user's new cash
        set_cash(db, user_id, cash_new)

        # Informs the user about the added cash.
        flash("Added cash: " + added_cash + ". Available cash: " + cash_new)
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
