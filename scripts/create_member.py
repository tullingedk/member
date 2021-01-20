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

import sys
from pathlib import Path

# add parent folder
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from app import db, app  # noqa: E402
from models import Member  # noqa: E402

name = input("Enter name: ")
email = input("Enter email: ")
school_class = input("Enter school class: ")
admin = True if input("Admin? (y/N): ").lower() == "y" else False
discord = (
    True if input("Has been given role on Discord? (y/N): ").lower() == "y" else False
)
modified_date = input("Enter modified creation date (empty if no): ")

# Create new member object
member = Member(
    name=name,
    email=email,
    school_class=school_class,
    admin=admin,
    archived=False,
    discord=discord,
    time_created=modified_date if modified_date is not None else None,
)

with app.app_context():
    db.session.add(member)
    db.session.commit()
