import os
from pprint import pprint

from dotenv import load_dotenv

from data.guild import Guild
from data.user import User
from mongo.mongo_controller import (addGuild, addUserToGuild, connectToMongoAndReturnClient,
                                    deleteGuild, getGuildById)

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

if __name__ == '__main__':
    mongoClient = connectToMongoAndReturnClient(MONGO_URI)
    guild = Guild('123', 'andius', [])
    user = User('1234', '2345', 'BeautifulBussy', 'cyeungster')
    addGuild(mongoClient, guild)
    result, guild = getGuildById(mongoClient, '123')
    result = addUserToGuild(mongoClient, '123', user)
