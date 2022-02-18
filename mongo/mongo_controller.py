from asyncio import QueueEmpty
from pprint import pprint

from data.guild import Guild
from data.user import User
from pymongo import MongoClient

from mongo.mongo_util import guildDoesExist


def connectToMongoAndReturnClient(mongoURI: str):
    client = MongoClient(mongoURI)
    db = client.master
    serverStatusResult = db.command('serverStatus')
    pprint('Connected to Database with OK Result: ' + str(serverStatusResult['ok']))
    return client

def addGuild(mongoClient: MongoClient, guild: Guild):
    if (guildDoesExist(mongoClient, guild.guildId)):
        pprint('Guild with id: ' + guild.guildId + ' already exists.')
        return False
    
    masterDB = mongoClient.master
    guildCollection = masterDB[guild.guildId]
    try: 
        insertResult = guildCollection.insert_one(guild.__dict__)
        return True
    except Exception as e:
        pprint('An error occured while inserting: ' + str(e))
        return False


def deleteGuild(mongoClient: MongoClient, guildId: str):
    if (not(guildDoesExist(mongoClient, guildId))):
        pprint('Guild with id: ' + guildId + ' does not exists.')
        return False
    
    masterDB = mongoClient.master
    guildCollection = masterDB[guildId]
    try:
        dropResult = guildCollection.drop()
        return True
    except Exception as e:
        pprint('An error occured when dropping Guild collection: ' + str(e))
        return False


def getGuildById(mongoClient: MongoClient, guildId: str):
    if (not(guildDoesExist(mongoClient, guildId))):
        pprint('Guild with id: ' + guildId + ' does not exists.')
        return (False, None)
        
    masterDB = mongoClient.master
    guildCollection = masterDB[guildId]
    document = guildCollection.find_one()
    return (True, Guild(guildId, document['name'], document['users']))


def addUserToGuild(mongoClient: MongoClient, guildId: str, user: User):
    if (not(guildDoesExist(mongoClient, guildId))):
        pprint('Guild with id: ' + guildId + ' does not exists.')
        return False
    
    masterDB = mongoClient.master
    guildCollection = masterDB[guildId]
    query = { 'name' : guild.name}
    newUsers = {'$push': {'users': user.__dict__}}
    try: 
        guildCollection.update_one(query, newUsers)
        pprint('Successfully inserted: ' + str(user))
        return True
    except Exception as e:
        pprint('An error occured when adding user to guild: ' + str(e))
        return False

def deleteUserInGuild()