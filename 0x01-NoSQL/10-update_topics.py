#!/usr/bin/env python3
""" funciton that changes topics of a document based on the name """


def update_topics(mongo_collecction, name, topics):
    """changes the topic of a document based on name """
    mongo_collection.update_many({"name": name},
                                {"$set": {"topics": topics}})
