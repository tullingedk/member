#############################################################################
#                                                                           #
# tullingedk/member                                                         #
# Copyright (C) 2020, Tullinge gymnasium datorklubb, <info@tgdk.se>, et al. #
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

email = input("Enter email: ")

with app.app_context():
    member = Member.query.filter_by(email=email).one()
    member.admin = True

    db.session.add(member)
    db.session.commit()
