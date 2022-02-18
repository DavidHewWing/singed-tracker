class Guild:
    def __init__(self, guildId, name, users):
        self.guildId = guildId
        self.name = name
        self.users = users
    
    def __str__(self):
        return self.guildId + " " + self.name + " " + str(self.users)
