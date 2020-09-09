#############################################################################
#                                                                           #
# tullingedk/member                                                         #
# Copyright (C) 2020, Tullinge gymnasium datorklubb, <info@tgdk.se>, et al. #
#                                                                           #
# Licensed under the terms of the MIT license, see LICENSE.                 #
# https://github.com/tullingedk/member                                      #
#                                                                           #
#############################################################################

from functools import wraps
from flask import session, redirect

from database import Database

db = Database()


def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def member(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not db.verify(session["google_email"]):
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function


def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        member = db.get(session["google_email"])

        if "styrelse" not in member["roles"]:
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function
