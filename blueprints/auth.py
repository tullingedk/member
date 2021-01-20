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

from flask import Blueprint, request, abort, session, redirect, render_template

from os import environ
from oauthlib.oauth2 import WebApplicationClient
from requests import get, post
from json import dumps

# define configuration (from environment variables)
GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_HOSTED_DOMAIN = environ.get("GOOGLE_HOSTED_DOMAIN", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

auth_blueprint = Blueprint("auth", __name__, template_folder="../templates")


# functions
def get_google_provider_cfg():
    return get(GOOGLE_DISCOVERY_URL).json()


@auth_blueprint.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="https://" + request.base_url[7:] + "/callback",
        scope=["openid", "email", "profile"],
    )

    return render_template("login.html", login_url=request_uri)


@auth_blueprint.route("/login/callback")
def callback():
    # Get authorization code Google sent back
    code = request.args.get("code")

    # If no code was sent
    if not code:
        abort(400, "missing oauth token")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url="https://" + request.base_url[7:],
        code=code,
    )
    token_response = post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens
    client.parse_request_body_response(dumps(token_response.json()))

    # Now that you have tokens let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        hd = None

        if "hd" not in userinfo_response.json():
            abort(
                401,
                "Email is not hosted domain. Please use organization Google Account.",
            )

        hd = userinfo_response.json()["hd"]

        if hd != GOOGLE_HOSTED_DOMAIN:
            abort(
                401,
                " ".join(
                    (
                        f"Member system only allows hosted domains for organization {GOOGLE_HOSTED_DOMAIN}.",
                        f"Your organization, {hd}, is not allowed.",
                    )
                ),
            )

        session["logged_in"] = True
        session["google_unique_id"] = userinfo_response.json()["sub"]
        session["google_email"] = userinfo_response.json()["email"]
        session["google_picture_url"] = userinfo_response.json()["picture"]
        session["google_name"] = userinfo_response.json()["name"]

        return redirect("/")

    abort(400, "User email not available or not verified by Google")


@auth_blueprint.route("/logout")
def logout():
    session.pop("logged_in", None)

    return redirect("/")
