from data.performance_data import PerformanceData

class Summoner:
    def __init__(self, accountId, summonerId, puuid, summonerName):
        self.accountId = accountId
        self.summonerId = summonerId
        self.puuid = puuid
        self.summonerName = summonerName
        self.performanceData = PerformanceData(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    
    def __str__(self):
        return "accountId: " + self.accountId + " \n summonerId: " + self.summonerId + " \n puuid: " + self.puuid + "\n summonerName: " + self.summonerName + "\n peformanceData: " + str(self.performanceData)