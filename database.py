#############################################################################
#                                                                           #
# tullingedk/member                                                         #
# Copyright (C) 2020, Tullinge gymnasium datorklubb, <info@tgdk.se>, et al. #
#                                                                           #
# Licensed under the terms of the MIT license, see LICENSE.                 #
# https://github.com/tullingedk/member                                      #
#                                                                           #
#############################################################################

from os import environ
from os.path import isdir

from git import Repo, Actor
from json import dump, load

from datetime import datetime

CACHE_PATH = "database_cache"
GIT_DATABASE = environ.get("GIT_DATABASE", None)


class Database:
    def __init__(self):
        if not isdir(CACHE_PATH):
            self.repo = Repo.clone_from(GIT_DATABASE, CACHE_PATH, branch="master")

        self.repo = Repo(CACHE_PATH)

    def create(self, name, school_class, email, roles):
        self._pull()

        members = self._read_entry()

        members["index"] = members["index"] + 1
        members["members"].append(
            {
                "id": members["index"],
                "email": email,
                "created": str(datetime.now()),
                "modified": str(datetime.now()),
                "archived": None,
            }
        )

        with open(f"{CACHE_PATH}/members.json", "w") as f:
            dump(members, f, indent=4, sort_keys=True)

        with open(f"{CACHE_PATH}/members/{members['index']}.json", "w") as f:
            dump(
                {
                    "id": members["index"],
                    "name": name,
                    "email": email,
                    "school_class": school_class,
                    "roles": roles,
                },
                f,
                indent=4,
                sort_keys=True,
            )

        self._commit(f"Registered member {name}", email, name)
        self._push()

    def get(self, email, archived=False):
        res = next(
            (
                member
                for member in self._read_entry(archived=archived)["members"]
                if member["email"] == email
            ),
            None,
        )

        if not res:
            raise Exception("Member does not exist")

        with open(
            f"{CACHE_PATH}/{'archived' if archived else 'members'}/{res['id']}.json"
        ) as f:
            member = load(f)

        member["created"] = res["created"]
        member["modified"] = res["modified"]
        member["archived"] = res["archived"]

        return member

    def get_all(self):
        entries = self._read_entry()
        members = [
            {**member, **self.get(member["email"])} for member in entries["members"]
        ]

        return members

    def get_archived(self):
        entries = self._read_entry(archived=True)
        members = [
            {**member, **self.get(member["email"])} for member in entries["members"]
        ]

        return members

    def verify(self, email):
        members = self._read_entry()

        if (
            len(
                list(
                    filter(lambda member: member["email"] == email, members["members"])
                )
            )
            == 0
        ):
            return False

        return True

    def _read_entry(self, archived=False):
        with open(f"{CACHE_PATH}/{'archived' if archived else 'members'}.json") as f:
            members = load(f)

        return members

    def _pull(self):
        self.repo.remotes.origin.pull()

    def _push(self):
        self.repo.remotes.origin.push()

    def _commit(self, msg, author_email, author_name):
        self.repo.git.add(all=True)

        author = Actor(author_name, author_email)
        index = self.repo.index

        index.commit(msg, author=author, committer=author)
