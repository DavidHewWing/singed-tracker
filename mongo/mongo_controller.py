from pymongo import MongoClient
from pprint import pprint

def connectToMongoAndReturnClient(mongoURI: str):
    client = MongoClient(mongoURI)
    db=client.master
    serverStatusResult=db.command('serverStatus')
    pprint(serverStatusResult)