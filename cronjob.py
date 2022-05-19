
from json import dumps
from bson import json_util
import json
from dotenv import load_dotenv
import os

from mongomock import MongoClient
from data.performance_data import PerformanceData
from mongo.mongo_controller import connectToMongoAndReturnClient, getAllGuilds, getAllUsersInGuildNoPerfData
from rito.rito_controller import getMatchData, getMatches
from rito.rito_endpoint_helper import getRequestHeaders

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
RITO_URI = os.getenv('RITO_BASE_URI')
RITO_REGION_BASE_URI = os.getenv('RITO_REGION_BASE_URI')
RITO_API_KEY = os.getenv('RITO_API_KEY')
requestHeader = getRequestHeaders(RITO_API_KEY)

# Detects games in which there are 'playerThreshold' amount of players in the same game from the same guild
def detectGamesForAllGuilds(mongoClient: MongoClient, playerThreshold):
    guilds = getAllGuilds(mongoClient)
    for guild in guilds:
        matchesWithFiveMembers = []
        matches = {}
        result, error = getAllUsersInGuildNoPerfData(mongoClient, guild)
        users = list(result)[0]['users']
        for user in users:
            currMatch = getMatches(RITO_REGION_BASE_URI, requestHeader, user['summoner']['puuid'])
            for matchId in currMatch:
                summonerName = user['summoner']['summonerName']
                if not(matchId in matches):
                    matches[matchId] = {}
                    matches[matchId] = []
                matches[matchId].append(summonerName)
        for matchId, match in matches.items():
            if len(matches[matchId]) >= playerThreshold:
                entry = {
                    'participants': match,
                    'guildId': guild
                }
                matchesWithFiveMembers.append({matchId: entry})
    return matchesWithFiveMembers

# Gets performance data from a matches array
def getPerformanceData(mongoClient: MongoClient, matches):
    for match in matches:
        matchData = getIndividualPerfomanceData(mongoClient, match)


def getIndividualPerfomanceData(mongoClient: MongoClient, match):
    for matchId in match:
        matchValue = match[matchId]
        data = getMatchData(RITO_REGION_BASE_URI, matchId, requestHeader)
        streamedData = [participant for participant in data['info']['participants'] if participant['summonerName'] in matchValue['participants']]
        playerDataForMatch = []
        for playerData in streamedData:
            championPlayed = playerData['championName']
            tempPerfData = PerformanceData(
                totDeaths = playerData['deaths'], 
                totKills = playerData['kills'],
                totAssists = playerData['assists'], 
                totCS = playerData['totalMinionsKilled'] + playerData['neutralMinionsKilled'],
                totDPS = playerData['totalDamageDealtToChampions'], 
                totDamageTaken = playerData['totalDamageTaken'],
                totTurretDamage = playerData['damageDealtToTurrets'], 
                totVisionScore = playerData['visionScore'],
                totGoldEarned = playerData['goldEarned'],
                totHealOnTeammates = playerData['totalHealsOnTeammates'],
                totTimeCCOthers = playerData['timeCCingOthers'],
                totShieldingOthers = playerData['totalDamageShieldedOnTeammates']
            )
            print(championPlayed)
            print(tempPerfData)

if __name__ == '__main__':
    print('cronjob.py is running!')
    mongoClient = connectToMongoAndReturnClient(MONGO_URI)
    matches = detectGamesForAllGuilds(mongoClient, 5)
    performanceData = getPerformanceData(mongoClient, matches)