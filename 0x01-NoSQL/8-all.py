#!/usr/bin/env python3
""" function that lists all mongodb documents in a collection """


def list_all(mongo_collection):
    """ lists all documents in a collection"""
    return [d for d in mongo_collection.find()]
