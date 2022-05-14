import datetime
import requests

from rito.rito_endpoint_helper import getMatchEndpoint, getMatchesEndpoint, getSummonerEndpoint

# Retrieves the summoner info via summoner name.
def getSummonerBySummonerName(riotURI: str, requestHeader, summonerName):
    summonerEndPoint = getSummonerEndpoint(summonerName)
    response = requests.get(riotURI + summonerEndPoint, headers=requestHeader)

    validation = validateResponse(response.status_code)
    if (validation['status_code'] != 200):
        return validation 
    response_json = response.json()
    
    return response_json

# Retrieves the games played in the last two hours
def getMatches(riotURI: str, requestHeader, puuid):
    lastTwoHourDateTime = int((datetime.datetime.now() - datetime.timedelta(hours = 2)).timestamp())
    matchesEndpoint = getMatchesEndpoint(puuid)
    query = {'startTime': lastTwoHourDateTime}
    response = requests.get(riotURI + matchesEndpoint, params=query, headers=requestHeader)

    validation = validateResponse(response.status_code)
    if (validation['status_code'] != 200):
        return validation 
    
    return response.json()

# Retrieves the match data for a game
def getMatchData(riotURI, matchId: str, requestHeader):
    matchEndpoint = getMatchEndpoint(matchId)
    response = requests.get(riotURI + matchEndpoint, headers=requestHeader)
    validation = validateResponse(response.status_code)
    if (validation['status_code'] != 200):
        return validation
    return response.json()


def validateResponse(statusCode):
    if (statusCode == 400):
        return {
            'status_code': 400,
            'message': 'Bad Request'
        }
    elif (statusCode == 401):
        return {
            'status_code': 401,
            'message': 'Unauthorized'
        }
    elif (statusCode == 403):
        return {
            'status_code': 403,
            'message': 'Forbidden'
        }
    elif (statusCode == 404):
        return {
            'status_code': 404,
            'message': 'Not Found'
        }
    elif (statusCode == 415):
        return {
            'status_code': 415,
            'message': 'Unsupported Media Type'
        }
    elif (statusCode == 429):
        return {
            'status_code': 429,
            'message': 'Rate Limit Exceeded'
        }
    elif (statusCode == 500):
        return {
            'status_code': 500,
            'message': 'Internal Server Error'
        }
    elif (statusCode == 503):
        return {
            'status_code': 503,
            'message': 'Service Unavailable'
        }
    else:
        return {
            'status_code': 200,
            'message': 'OK'
        }