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
from os import urandom, environ
from datetime import datetime

from blueprints.auth import auth_blueprint
from decorators import logged_in, member, admin
from models import db, Member

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY", urandom(24))

MYSQL_USER = environ.get("MYSQL_USER", "member")
MYSQL_PASSWORD = environ.get("MYSQL_PASSWORD", "password")
MYSQL_HOST = environ.get("MYSQL_HOST", "127.0.0.1")
MYSQL_DATABASE = environ.get("MYSQL_DATABASE", "member")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=["POST", "GET"])
@logged_in
def index():
    if request.method == "GET":
        member = Member.query.filter_by(email=session["google_email"]).all()

        if member:
            member = member[0]

        return render_template(
            "index.html",
            member=member,
            email=session["google_email"],
            picture_url=session["google_picture_url"],
            name=session["google_name"],
        )

    if request.method == "POST":
        if len(Member.query.filter_by(email=session["google_email"]).all()) > 0:
            abort(400, "You are already a member.")

        school_class = request.form["school_class"].upper()
        stadgar = request.form["stadgar"]

        if not stadgar:
            abort(400, "Stadgar must be accepted")

        if len(school_class) < 4 or len(school_class) > 5:
            abort(400, "Too long or too short school_class.")

        # Create new member object
        member = Member(
            name=session["google_name"],
            email=session["google_email"],
            school_class=school_class,
            admin=False,
            archived=False,
        )

        # Add to database
        db.session.add(member)
        db.session.commit()

        return redirect("/")


@app.route("/list")
@logged_in
@member
@admin
def admin_list():
    members = Member.query.filter_by(archived=False).all()

    return render_template("admin/list.html", members=members, time=datetime.now())


@app.route("/archived-list")
@logged_in
@member
@admin
def archived_list():
    members = Member.query.filter_by(archived=True).all()

    return render_template(
        "admin/list.html", members=members, time=datetime.now(), archived=True
    )


@app.route("/archive/<id>")
@logged_in
@member
@admin
def archive(id):
    member = Member.query.get(id)

    member.time_archived = None if member.archived else datetime.now()
    member.archived = False if member.archived else True

    # Add to database
    db.session.add(member)
    db.session.commit()

    return redirect("/list")


# register blueprints
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
