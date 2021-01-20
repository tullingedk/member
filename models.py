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

from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


@dataclass
class Member(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)
    email: str = db.Column(db.String(255), unique=True, nullable=False)
    school_class: str = db.Column(db.String(255), unique=False, nullable=False)
    admin: bool = db.Column(db.Boolean(), unique=False, nullable=False)
    discord: bool = db.Column(db.Boolean(), unique=False, nullable=False)

    archived: bool = db.Column(db.Boolean(), unique=False, nullable=False)
    time_archived: db.DateTime = db.Column(db.DateTime(timezone=False), nullable=True)

    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
