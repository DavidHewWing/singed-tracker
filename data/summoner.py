class Summoner:
    def __init__(self, accountId, summonerId, puuid, summonerName):
        self.accountId = accountId
        self.summonerId = summonerId
        self.puuid = puuid
        self.summonerName = summonerName
    
    def __str__(self):
        return "accountId: " + self.accountId + " summonerId: " + self.summonerId + " puuid: " + self.puuid + " summonerName: " + self.summonerName