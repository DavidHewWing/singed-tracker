import json
import os
from pprint import pprint

from dotenv import load_dotenv

from data.guild import Guild
from data.summoner import Summoner
from data.user import User
from discord.discord import run_discord
from mongo.mongo_controller import (addGuild, addUserToGuild, connectToMongoAndReturnClient,
                                    deleteGuild, getGuildById, deleteUserInGuild, getUserInGuildByDiscordId)
from rito.rito_controller import getMatchData, getMatches, getSummonerBySummonerName
from rito.rito_endpoint_helper import getRequestHeaders

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
RITO_URI = os.getenv('RITO_BASE_URI')
RITO_REGION_BASE_URI = os.getenv('RITO_REGION_BASE_URI')
RITO_API_KEY = os.getenv('RITO_API_KEY')

# def ritoConnection():
#     requestHeader = getRequestHeaders(RITO_API_KEY)
#     rawSummoner = getSummonerBySummonerName(RITO_URI, requestHeader, 'psychsafety')
#     print(rawSummoner)
#     summoner = Summoner(rawSummoner['accountId'], rawSummoner['id'], rawSummoner['puuid'], rawSummoner['name'])
#     matches = getMatches(RITO_REGION_BASE_URI, requestHeader, summoner.puuid)
#     match = getMatchData(RITO_REGION_BASE_URI, matches[0], requestHeader)
#     print(summoner)
#     print(matches)

    # print(json.dumps(match, indent=4, sort_keys=True))

    # with open("sample.json", "w") as outfile:
    #     json.dump(match, outfile, indent=4, sort_keys=True)


if __name__ == '__main__':
    print('main.py is running!')
    run_discord()
    # s = Summoner('a', 'asd','asd','asd')
    # u = User('a','a', s)
    # print(u)
    # ritoConnection()
    # mongoClient = connectToMongoAndReturnClient(MONGO_URI)
    # guild = Guild('123', 'andius', [])
    # user = User('1234', '2345', 'BeautifulBussy', 'cyeungster')
    # addGuild(mongoClient, guild)
    # result, guild = getGuildById(mongoClient, '123')
    # result1 = addUserToGuild(mongoClient, '123', user)
    # result = deleteUserInGuild(mongoClient, '123', '1234')
    # document, result = getUserInGuildByDiscordId(mongoClient, '123', '09809')
    # print(document)
