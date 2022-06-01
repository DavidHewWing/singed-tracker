from datetime import date
from pprint import pprint

from data.user import User
from pymongo import MongoClient

from mongo.mongo_util import guildDoesExist


def connectToMongoAndReturnClient(mongoURI: str):
    client = MongoClient(mongoURI)
    db = client.master
    serverStatusResult = db.command('serverStatus')
    pprint('Connected to Database with OK Result: ' + str(serverStatusResult['ok']))
    return client

def addGuild(mongoClient: MongoClient, guildId: str):
    if (guildDoesExist(mongoClient, guildId)):
        pprint('Guild with id: ' + guildId + ' already exists.')
        return False
    
    masterDB = mongoClient.master
    historicalDB = mongoClient.historical
    try: 
        masterDB.create_collection(guildId)
        historicalDB.create_collection(guildId)
        return True
    except Exception as e:
        pprint('An error occured while adding a guild: ' + str(e))
        return False


def deleteGuild(mongoClient: MongoClient, guildId: str):
    if (not(guildDoesExist(mongoClient, guildId))):
        pprint('Guild with id: ' + guildId + ' does not exists.')
        return False
    masterDB = mongoClient.master
    historicalDB = mongoClient.historical
    guildCollection = masterDB[guildId]
    historicalCollection = historicalDB[guildId]
    try:
        guildDropResult = guildCollection.drop()
        historicalDropResult = historicalCollection.drop()
        return True
    except Exception as e:
        pprint('An error occured when dropping Guild collection: ' + str(e))
        return False

def addUserToGuild(mongoClient: MongoClient, guildId: str, user: User):
    masterDB = mongoClient.master
    guildCollection = masterDB[guildId]
    userJson = transform_to_dict(user)
    try: 
        guildCollection.insert_one(userJson)
        pprint('Successfully inserted user with id: ' + str(user.discordId))
        return True
    except Exception as e:
        pprint('An error occured when adding user to guild: ' + str(e))
        return False

def deleteUserInGuild(mongoClient: MongoClient, guildId: str, discordId: str):
    masterDB = mongoClient.master
    guildCollection = masterDB[guildId]
    query = { 'discordId' : discordId}
    try:
        result = guildCollection.delete_one(query)
        if (result.deleted_count == 0):
            pprint('Could not find user with discord id: ' + discordId)
            return False
        pprint('Successfully removed user with discord id: ' + discordId)
        return True
    except Exception as e:
        pprint('An error occured when deleting user from guild: ' + str(e))
        return False

def getUserInGuildByDiscordId(mongoClient: MongoClient, guildId: str, discordId: str):
    masterDB = mongoClient.master
    guildCollection = masterDB[guildId]
    query = {'discordId': discordId}
    try: 
        result = guildCollection.find_one(query)
        if (result == None):
            pprint('Could not find user with discord id: ' + discordId)
            return None, False
        return result, True
    except Exception as e:
        pprint('An error occured when retreiving user from guild: ' + str(e))
        return None, False

def getAllUsersInGuildNoPerfData(mongoClient: MongoClient, guildId):
    masterDB = mongoClient.master
    guildCollection = masterDB[guildId]
    try: 
        users = guildCollection.find({}, { 'summoner': { 'performanceData' : 0 } , 'guildId': 0, '_id': 0, 'name': 0})
        return users, True
    except Exception as e:
        pprint('An error when getting all users: ' + str(e))
        return None, False

def getAllGuilds(mongoClient: MongoClient):
    db = mongoClient.master
    collectionList = db.list_collection_names()
    collectionList.remove('guilds')
    return collectionList

def updatePerformanceData(mongoClient: MongoClient, guildId: str, perfData, summonerName: str, championPlayed: str):
    masterDB = mongoClient.master
    historicalDB = mongoClient.historical
    guildCollection = masterDB[guildId]
    historicalCollection = historicalDB[guildId]
    championPlayedField = 'summoner.championsPlayed.' + championPlayed
    query = { 'summoner.summonerName' : summonerName } 
    update = { '$inc' : {
        'summoner.performanceData.totDeaths': perfData.totDeaths,
        'summoner.performanceData.totKills': perfData.totKills,
        'summoner.performanceData.totAssists': perfData.totAssists,
        'summoner.performanceData.totCS': perfData.totCS,
        'summoner.performanceData.totDPS': perfData.totDPS,
        'summoner.performanceData.totDamageTaken': perfData.totDamageTaken,
        'summoner.performanceData.totTurretDamage': perfData.totTurretDamage,
        'summoner.performanceData.totGoldEarned': perfData.totGoldEarned,
        'summoner.performanceData.totVisionScore': perfData.totVisionScore,
        'summoner.performanceData.totHealsOnTeammates': perfData.totHealsOnTeammates,
        'summoner.performanceData.totTimeCCOthers': perfData.totTimeCCOthers,
        'summoner.performanceData.totShieldingOthers': perfData.totShieldingOthers,
        'summoner.performanceData.totGames': perfData.totGames,
        championPlayedField : 1
    } }
    user = guildCollection.update_one(query, update)
    today = date.today()
    todayDate = today.strftime("%d/%m/%Y")

    historicalUpdate = {
        'totDeaths': perfData.totDeaths,
        'totKills': perfData.totKills,
        'totAssists': perfData.totAssists,
        'totCS': perfData.totCS,
        'totDPS': perfData.totDPS,
        'totDamageTaken': perfData.totDamageTaken,
        'totTurretDamage': perfData.totTurretDamage,
        'totGoldEarned': perfData.totGoldEarned,
        'totVisionScore': perfData.totVisionScore,
        'totHealsOnTeammates': perfData.totHealsOnTeammates,
        'totTimeCCOthers': perfData.totTimeCCOthers,
        'totShieldingOthers': perfData.totShieldingOthers,
        'totGames': perfData.totGames,
        'championPlayed' : championPlayed,
        'summonerName': summonerName,
        'dateRecorded': todayDate
    }
    historicalCollection.insert_one(historicalUpdate)

    return user
    
def getAllUsersInGuild(mongoClient: MongoClient, guildId: str):
    masterDB = mongoClient.master
    guildCollection = masterDB[guildId]
    try: 
        users = guildCollection.find({})
        return users, True
    except Exception as e:
        pprint('An error when getting all users: ' + str(e))
        return None, False


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