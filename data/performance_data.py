class PerformanceData:
    def __init__(self, totDeaths, totKills, totAssists, totCS, totDPS, totDamageTaken, 
    totTurretDamage, totGoldEarned, totVisionScore,
    totHealOnTeammates, totTimeCCOthers, totShieldingOthers, totGames):
        self.totDeaths = totDeaths
        self.totKills = totKills
        self.totAssists = totAssists
        self.totCS = totCS
        self.totDPS = totDPS
        self.totDamageTaken = totDamageTaken
        self.totTurretDamage = totTurretDamage
        self.totGoldEarned = totGoldEarned
        self.totVisionScore = totVisionScore
        self.totHealsOnTeammates = totHealOnTeammates
        self.totTimeCCOthers = totTimeCCOthers
        self.totShieldingOthers = totShieldingOthers
        self.totGames = totGames
    def __str__(self):
        return f' \n Total Deaths: {str(self.totDeaths)} \n Total Kills: {str(self.totKills)} \n Total Assists : {str(self.totAssists)} \nTotal CS: {str(self.totCS)}\
        \n Total DPS: {str(self.totDPS)} \n Total Damage Taken: {str(self.totDamageTaken)} \n Total Turret Damage: {str(self.totTurretDamage)} \
        \n Total Gold Earned {str(self.totGoldEarned)} \n Total Vision Score: {str(self.totVisionScore)} \
        \n Total Healing to Teammates: {str(self.totHealsOnTeammates)}  \n Total Time CC Others: {str(self.totTimeCCOthers)} \n Total Shielding Others: {str(self.totShieldingOthers)} \
        \n Total Games: {str(self.totGames)}'