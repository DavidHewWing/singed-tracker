class User:
    def __init__(self, discordId, discordName, summoner):
        self.discordId = discordId
        self.discordName = discordName
        self.summoner = summoner
    
    def __str__(self):
        return "discordId: " + str(self.discordId) + " discordName: " + self.discordName + " summoner: " + str(self.summoner)

    def setLastCheckedGameId(self, lastGamesIds):
        self.lastGameIds = lastGamesIds
