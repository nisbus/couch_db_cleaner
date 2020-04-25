#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   Copyright (C) 2020 nisbus.com.

This file is part of CouchDB Cleaner.

CouchDB Cleaner is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

CouchDB Cleaner is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CouchDB Cleaner.  If not, see <https://www.gnu.org/licenses/>.


Cleaning tool for CouchDB

__author__ "nisbus"
__maintainer__ "nisbus@gmail.com"
"""
import json
import requests
import argparse


class Purger:
    """
    Class for purging and compacting a CouchDb database
    """

    def __init__(self, protocol, username, password, url, database):
        request_url = _build_url(
            protocol, username, password, url, database, "_changes")
        response = requests.get(request_url)
        documents = response.json()[u"results"]
        purge_url = _build_url(
            protocol, username, password, url, database, "_purge")
        counter = 0
        errors = 0
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept": "text/plain; charset=utf-8"}
        for document in documents:
            if "deleted" in document:
                doc_id = document["id"]
                revisions = [rev["rev"] for rev in document["changes"]]
                request = json.dumps({doc_id: revisions})
                delete_response = requests.post(purge_url, data=request,
                                                headers=headers)
                if delete_response.status_code > 204:
                    errors = errors + 1
                    print("Response {} - {}".format(delete_response.text,
                                                    delete_response.status_code))  # pylint: disable=line-too-long
                else:
                    counter = counter + 1
        print("Purged {} documents\nErrors {}\nNow compacting database and views".format(  # pylint: disable=line-too-long
            counter, errors))
        compact_url = _build_url(
            protocol, username, password, url, database, "_compact")
        compact_response = requests.post(compact_url,
                                         headers=headers)
        print("Compact response {}".format(compact_response.text))
        compact_view_url = _build_url(
            protocol, username, password, url, database, "_view_cleanup")
        compact_view_response = requests.post(compact_view_url,
                                              headers=headers)
        print("View cleanup response {}".format(compact_view_response))
        print("All done")


def _build_url(protocol, username, password, url, database, endpoint):
    if not username and not password:
        return "{}://{}/{}/{}".format(protocol, url, database, endpoint)
    else:
        return "{}://{}:{}@{}/{}/{}".format(
            protocol, username, password, url, database, endpoint)


if __name__ == "__main__":
    def get_args():
        parser = argparse.ArgumentParser(
            description="Cleanup for couchdb deleted documents")
        parser.add_argument(
            "--user",
            nargs="?",
            type=str,
            help="The username of a user with access to the database"
        )
        parser.add_argument(
            "--password",
            nargs="?",
            type=str,
            help="The password of the user"
        )
        parser.add_argument(
            "--host",
            nargs="?",
            type=str,
            help="The hostname of the database (including port), default: localhost:5984",
            default="localhost:5984"
        )
        parser.add_argument(
            "--database",
            nargs="?",
            type=str,
            help="The database to cleanup, if not provided will try and clean all databases",
            default="all"
        )
        parser.add_argument(
            "--protocol",
            nargs="?",
            type=str,
            help="The protocol to use (http/https) default: http",
            default="http"
        )
        return parser.parse_args()
    print("Starting cleanup")
    ARGS = get_args()
    if ARGS.database == "all":

        all_databases = "{}://{}:{}@{}/_all_dbs".format(
            ARGS.protocol, ARGS.user, ARGS.password, ARGS.host)
        database_request = requests.get(all_databases,
                                        headers={"Accept": "application/json"})
        for db in database_request.json():
            print("Cleaning {}".format(db))
            Purger(ARGS.protocol, ARGS.user,
                   ARGS.password, ARGS.host, db)
    else:
        print("Cleaning {}".format(ARGS.database))
        Purger(ARGS.protocol, ARGS.user,
               ARGS.password, ARGS.host, ARGS.database)
