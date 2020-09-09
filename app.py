#############################################################################
#                                                                           #
# tullingedk/member                                                         #
# Copyright (C) 2020, Tullinge gymnasium datorklubb, <info@tgdk.se>, et al. #
#                                                                           #
# Licensed under the terms of the MIT license, see LICENSE.                 #
# https://github.com/tullingedk/member                                      #
#                                                                           #
#############################################################################

from flask import Flask, session, render_template, redirect
from os import urandom

from blueprints.auth import auth_blueprint

app = Flask(__name__)
app.secret_key = urandom(24)


@app.route("/")
def index():
    if "logged_in" in session:
        return render_template(
            "index.html",
            email=session["google_email"],
            picture_url=session["google_picture_url"],
            name=session["google_name"],
        )

    return redirect("/login")


# register blueprints
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
