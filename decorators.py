#############################################################################
#                                                                           #
# tullingedk/member                                                         #
# Copyright (C) 2020 - 2021, Tullinge gymnasium datorklubb, <info@tgdk.se>  #
# Created by Vilhelm Prytz <vilhelm@prytznet.se> https://vilhelmprytz.se    #
#                                                                           #
# Licensed under the terms of the MIT license, see LICENSE.                 #
# https://github.com/tullingedk/member                                      #
#                                                                           #
#############################################################################

from functools import wraps
from flask import session, redirect

from models import Member


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
        if len(Member.query.filter_by(email=session["google_email"]).all()) < 1:
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function


def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        member = Member.query.filter_by(email=session["google_email"]).one()

        if not member.admin:
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function
