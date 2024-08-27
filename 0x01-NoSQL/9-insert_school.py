#!/usr/bin/env python3
""" inserts a new document using python pymongo """


def insert_school(mongo_collection, **kwargs):
    """ inserts a new mongo dg document """
    return mongo_collection.insert_one(kwargs).inserted_id
