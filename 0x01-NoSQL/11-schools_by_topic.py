#!/usr/bin/env python3
"""ALX SE"""

def schools_by_topic(mongo_collection, topic):
    """Return the list of schools having a specific topic"""
    result = mongo_collection.find({"topics": {"$in": [topic]}})
    return result
