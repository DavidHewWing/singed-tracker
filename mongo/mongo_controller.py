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


async def addUserToGuild(mongoClient: MongoClient, guildId: str, user: User):
    _, guild = getGuildById(mongoClient, guildId)
    masterDB = mongoClient.master
    guildCollection = masterDB[guildId]
    query = { 'name' : guild.name}
    newUsers = {'$push': {'users': transform_to_dict(user)}}
    try: 
        guildCollection.update_one(query, newUsers)
        pprint('Successfully inserted user with id: ' + str(user.discordId))
        return True
    except Exception as e:
        pprint('An error occured when adding user to guild: ' + str(e))
        return False

def deleteUserInGuild(mongoClient: MongoClient, guildId: str, discordId: str):
    _, guild = getGuildById(mongoClient, guildId)
    masterDB = mongoClient.master
    guildCollection = masterDB[guildId]
    query = { 'name' : guild.name}
    removeUser = { '$pull': { 'users' : {'discordId': discordId } } }
    try:
        result = guildCollection.update_one(query, removeUser)
        if (result.modified_count == 0):
            pprint('Could not find user with discord id: ' + discordId)
            return False
        pprint('Successfully removed user with discord id: ' + discordId)
        return True
    except Exception as e:
        pprint('An error occured when deleting user from guild: ' + str(e))
        return False

def getUserInGuildByDiscordId(mongoClient: MongoClient, guildId: str, discordId: str):
    _, guild = getGuildById(mongoClient, guildId)
    masterDB = mongoClient.master
    guildCollection = masterDB[guildId]
    query = {'users.discordId': discordId}
    try: 
        result = guildCollection.find_one(query)
        resultUser = None
        for user in result['users']:
            if user['discordId'] == discordId:
                resultUser = user
                break
        if (result == None or resultUser == None):
            pprint('Could not find user with discord id: ' + discordId)
            return None, False

        return resultUser, True
    except Exception as e:
        pprint('An error occured when retreiving user from guild: ' + str(e))
        return None, False

def getAllUsersInGuildNoPerfData(mongoClient: MongoClient, guildId):
    _, guild = getGuildById(mongoClient, guildId)
    masterDB = mongoClient.master
    guildCollection = masterDB[guildId]
    try: 
        users = guildCollection.find({}, {'users' : { 'summoner': { 'performanceData' : 0 } }, 'guildId': 0, '_id': 0, 'name': 0})
        return users, True
    except Exception as e:
        pprint('An error when getting all users: ' + str(e))
        return None, False

def getAllGuilds(mongoClient: MongoClient):
    db = mongoClient.master
    collectionList = db.list_collection_names()
    collectionList.remove('guilds')
    return collectionList

def transform_to_dict(obj):
    if not  hasattr(obj,"__dict__"):
        return obj
    result = {}
    for key, val in obj.__dict__.items():
        if key.startswith("_"):
            continue
        element = []
        if isinstance(val, list):
            for item in val:
                element.append(transform_to_dict(item))
        else:
            element = transform_to_dict(val)
        result[key] = element
    return result