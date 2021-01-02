from flask import Blueprint, render_template
from werkzeug.exceptions import HTTPException

errors = Blueprint('error', __name__)


def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("errors/apology.html", top=code, bottom=message), code


@errors.app_errorhandler(HTTPException)
def error_other(error):

    if not isinstance(error, HTTPException):
        error = InternalServerError()
    
    return apology(error.description, error.code)

