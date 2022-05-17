class PerformanceData:
    def __init__(self, totDeaths, totKills, totAssists, totCS, totDPS, totDamageTaken, totTurretDamage, totGoldEarned, totTowerDestroyed):
        self.totDeaths = totDeaths
        self.totKills = totKills
        self.totAssists = totAssists
        self.totCS = totCS
        self.totDPS = totDPS
        self.totDamageTaken = totDamageTaken
        self.totTurretDamage = totTurretDamage
        self.totGoldEarned = totGoldEarned
        self.totTowerDestroyed = totTowerDestroyed

    def __str__(self):
        return f' \n Total Deaths: {str(self.totDeaths)} \n Total Kills: {str(self.totKills)} \n Total CS: {str(self.totCS)}\
        \n Total DPS: {str(self.totDPS)} \n Total Damage Taken: {str(self.totDamageTaken)} \n Total Turret Damage: {str(self.totTurretDamage)} \
        \n Total Gold Earned {str(self.totGoldEarned)} \n Total Tower Destroyed: {str(self.totTowerDestroyed)}'