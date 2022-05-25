# bot.py
import os

import discord
from dotenv import load_dotenv

from discord.ext import commands
from data.summoner import Summoner
from data.user import User
from mongo.mongo_controller import addGuild, addUserToGuild, connectToMongoAndReturnClient
from mongo.mongo_util import guildDoesExist

from rito.rito_controller import getSummonerBySummonerName
from rito.rito_endpoint_helper import getRequestHeaders

def run_discord():
    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    MONGO_URI = os.getenv('MONGO_URI')
    RITO_URI = os.getenv('RITO_BASE_URI')
    RITO_REGION_BASE_URI = os.getenv('RITO_REGION_BASE_URI')
    RITO_API_KEY = os.getenv('RITO_API_KEY')
    requestHeader = getRequestHeaders(RITO_API_KEY)
    bot = commands.Bot(command_prefix='!')

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')

    @bot.command(name='add', help='Addes a user with Riot Data and Discord Data')
    async def add(ctx, summonerName, discordUser: discord.User):
        summonerData = getSummonerBySummonerName(RITO_URI, requestHeader, summonerName)

        if summonerData['status_code'] == 200:
            print('here')
            mongoClient = connectToMongoAndReturnClient(MONGO_URI)
            summoner = Summoner(summonerData['accountId'], summonerData['id'], summonerData['puuid'], summonerName)
            user = User(discordUser.id, str(discordUser), summoner)
            exists = guildDoesExist(mongoClient, str(ctx.guild.id))
            guildAdded = addGuild(mongoClient, str(ctx.guild.id))

            if (guildAdded or exists):
                added = addUserToGuild(mongoClient, str(ctx.guild.id), user)
                if (not(added)):
                    await ctx.send('Error when inserting to MongoDB')
                else:
                    await ctx.send(f'Successfully added {str(user.discordName)} to Singed Tracker')
        else:
            await ctx.send(f"Error happened! {summonerData['status_code']} : {summonerData['message']}.")

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('You do not have the requirement arguments for this command. Type !help for more details.')
        else:
            await ctx.send(error)

    bot.run(TOKEN)