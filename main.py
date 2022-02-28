import os
from pprint import pprint

from dotenv import load_dotenv

from data.guild import Guild
from data.user import User
from mongo.mongo_controller import (addGuild, addUserToGuild, connectToMongoAndReturnClient,
                                    deleteGuild, getGuildById, deleteUserInGuild, getUserInGuildByDiscordId)

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

if __name__ == '__main__':
    # mongoClient = connectToMongoAndReturnClient(MONGO_URI)
    guild = Guild('123', 'andius', [])
    user = User('1234', '2345', 'BeautifulBussy', 'cyeungster')
    # addGuild(mongoClient, guild)
    # result, guild = getGuildById(mongoClient, '123')
    # result1 = addUserToGuild(mongoClient, '123', user)
    # result = deleteUserInGuild(mongoClient, '123', '1234')
    # document, result = getUserInGuildByDiscordId(mongoClient, '123', '09809')
    # print(document)
