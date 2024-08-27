#!/usr/bin/env python3
"""function that returns a list of collection having a specific topic """


def school_by_topic(mongo_collection, topic):
    """ returns a list of school with a specific topic"""
    return mongo_collection.find({"topics": topic})
