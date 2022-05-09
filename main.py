import os
from pprint import pprint

from dotenv import load_dotenv

from data.guild import Guild
from data.summoner import Summoner
from data.user import User
from mongo.mongo_controller import (addGuild, addUserToGuild, connectToMongoAndReturnClient,
                                    deleteGuild, getGuildById, deleteUserInGuild, getUserInGuildByDiscordId)
from rito.rito_controller import getMatches, getSummonerBySummonerName
from rito.rito_endpoint_helper import getRequestHeaders

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
RITO_URI = os.getenv('RITO_BASE_URI')
RITO_REGION_BASE_URI = os.getenv('RITO_REGION_BASE_URI')
RITO_API_KEY = os.getenv('RITO_API_KEY')

def ritoConnection():
    requestHeader = getRequestHeaders(RITO_API_KEY)
    rawSummoner = getSummonerBySummonerName(RITO_URI, requestHeader, 'Hewyy')
    print(rawSummoner)
    summoner = Summoner(rawSummoner['accountId'], rawSummoner['id'], rawSummoner['puuid'], rawSummoner['name'])
    matches = getMatches(RITO_REGION_BASE_URI, requestHeader, summoner.puuid)
    user = User('discordId', 'cyeungster', summoner)
    print(summoner)
    print(matches)


if __name__ == '__main__':
    ritoConnection()
    # mongoClient = connectToMongoAndReturnClient(MONGO_URI)
    # guild = Guild('123', 'andius', [])
    # user = User('1234', '2345', 'BeautifulBussy', 'cyeungster')
    # addGuild(mongoClient, guild)
    # result, guild = getGuildById(mongoClient, '123')
    # result1 = addUserToGuild(mongoClient, '123', user)
    # result = deleteUserInGuild(mongoClient, '123', '1234')
    # document, result = getUserInGuildByDiscordId(mongoClient, '123', '09809')
    # print(document)
