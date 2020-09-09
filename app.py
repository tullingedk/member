#############################################################################
#                                                                           #
# tullingedk/member                                                         #
# Copyright (C) 2020, Tullinge gymnasium datorklubb, <info@tgdk.se>, et al. #
#                                                                           #
# Licensed under the terms of the MIT license, see LICENSE.                 #
# https://github.com/tullingedk/member                                      #
#                                                                           #
#############################################################################

from flask import Flask, session, render_template, redirect, request, abort
from os import urandom

from blueprints.auth import auth_blueprint
from database import Database
from decorators import logged_in, member, admin

app = Flask(__name__)
app.secret_key = urandom(24)

db = Database()
db._pull()


@app.route("/", methods=["POST", "GET"])
@logged_in
def index():
    if request.method == "GET":
        member = None

        if db.verify(session["google_email"]):
            member = db.get(session["google_email"])

        return render_template(
            "index.html",
            member=member,
            email=session["google_email"],
            picture_url=session["google_picture_url"],
            name=session["google_name"],
        )

    if request.method == "POST":
        if db.verify(session["google_email"]):
            abort(400, "You are already a member.")

        print(request.form)

        school_class = request.form["school_class"].upper()
        stadgar = request.form["stadgar"]

        print(school_class)
        print(stadgar)

        if len(school_class) < 4 or len(school_class) > 5:
            abort(400, "Too long or too short school_class.")

        db.create(
            session["google_name"], school_class, session["google_email"], roles=[]
        )
        return redirect("/")


@app.route("/list")
@logged_in
@member
@admin
def admin_list():
    members = db.get_all()

    return render_template("admin/list.html", members=members)


# register blueprints
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
