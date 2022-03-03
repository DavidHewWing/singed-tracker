class User:
    def __init__(self, discordId, leagueApiId, summonerName, discordName):
        self.discordId = discordId
        self.leagueApiId = leagueApiId
        self.summonerName = summonerName
        self.discordName = discordName
    
    def __str__(self):
        return self.discordId + " " + self.leagueApiId + " " + self.summonerName + " " + self.discordName
