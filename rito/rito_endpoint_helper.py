
def getSummonerEndpoint(summonerName: str):
    return 'lol/summoner/v4/summoners/by-name/' + summonerName

def getMatchesEndpoint(puuid: str):
    return 'lol/match/v5/matches/by-puuid/' + puuid + '/ids'

def getMatchEndpoint(matchId: str):
    return 'lol/match/v5/matches/' + matchId

def getRequestHeaders(riotApiKey: str):
    return {
        'Content-Type': 'application/json',
        'X-Riot-Token': riotApiKey
    }