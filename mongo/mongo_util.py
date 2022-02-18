from pymongo import MongoClient

def guildDoesExist(mongoClient: MongoClient, guildId: str):
    db = mongoClient.master
    collectionList = db.list_collection_names()
    return guildId in collectionList
