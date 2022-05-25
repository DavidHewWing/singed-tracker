import os

from dotenv import load_dotenv

from discord.discord import run_discord
from data.summoner import Summoner
from data.user import User

from mongo.mongo_controller import addGuild, addUserToGuild, connectToMongoAndReturnClient, deleteGuild, deleteUserInGuild, getAllGuilds, getAllUsersInGuildNoPerfData, getUserInGuildByDiscordId

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

if __name__ == '__main__':
    print('main.py is running!')
    run_discord()
    # mongoClient = connectToMongoAndReturnClient(MONGO_URI)
    # user = User('discId1', 'discName1', Summoner('12','23','34','name1'))
    # addGuild(mongoClient, '123')
    # addUserToGuild(mongoClient, '123', user)
    # deleteGuild(mongoClient, '123')
    # deleteUserInGuild(mongoClient, '123', 'discId')
    # print(getUserInGuildByDiscordId(mongoClient, '123', 'discId'))
    # docs = getAllUsersInGuildNoPerfData(mongoClient, '123')
    # for doc in docs[0]:
    #     print(doc)
    # print(getAllGuilds(mongoClient))
