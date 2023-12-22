#!/usr/bin/env python3
"""ALX SE"""

def list_all(mongo_collection):
    """"list all documents in a collection"""
    if mongo_collection is None:
        return []
    return mongo_collection.find()
