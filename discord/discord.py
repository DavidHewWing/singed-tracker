# bot.py
import os

import discord
from dotenv import load_dotenv
from table2ascii import table2ascii as t2a, PresetStyle
from discord.ext import commands
from data.summoner import Summoner
from data.user import User
from mongo.mongo_controller import addGuild, addUserToGuild, connectToMongoAndReturnClient, getAllUsersInGuild
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

    @bot.command(name='add', help='Add a user with Riot Data and Discord Data')
    async def add(ctx, summonerName, discordUser: discord.User):
        summonerData = getSummonerBySummonerName(RITO_URI, requestHeader, summonerName)

        if summonerData['status_code'] == 200:
            mongoClient = connectToMongoAndReturnClient(MONGO_URI)
            summoner = Summoner(summonerData['accountId'], summonerData['id'], summonerData['puuid'], summonerName)
            user = User(discordUser.id, str(discordUser), summoner)
            exists = guildDoesExist(mongoClient, f'{str(ctx.guild.id)}-{str(ctx.guild.name)}')
            guildAdded = addGuild(mongoClient, f'{str(ctx.guild.id)}-{str(ctx.guild.name)}')

            if (guildAdded or exists):
                added = addUserToGuild(mongoClient, f'{str(ctx.guild.id)}-{str(ctx.guild.name)}', user)
                if (not(added)):
                    await ctx.send('Error when inserting to MongoDB')
                else:
                    await ctx.send(f'Successfully added {str(user.discordName)} to Singed Tracker')
        else:
            await ctx.send(f"Error happened! {summonerData['status_code']} : {summonerData['message']}.")

    @bot.command(name = 'stats', help = 'Displays all stats in the discord bot')
    async def stats(ctx):
        mongoClient = connectToMongoAndReturnClient(MONGO_URI)
        guildId = str(ctx.guild.id) + '-' + str(ctx.guild.name)
        getAllUsersResponse = getAllUsersInGuild(mongoClient, guildId)
        if not(getAllUsersResponse[1]):
            await ctx.send('Error when getting all users!')
        else:
            tableRow1 = []
            tableRow2 = []
            tableRow3 = []
            users = getAllUsersResponse[0]
            for user in users:
                tempArr1 = []
                performanceData = user['summoner']['performanceData']
                tempArr1.append(user['summoner']['summonerName'])
                tempArr1.append(performanceData['totGames'])
                tempArr1.append(performanceData['totKills'])
                tempArr1.append(performanceData['totDeaths'])
                tempArr1.append(performanceData['totAssists'])
                tempArr1.append(performanceData['totCS'])
                tableRow1.append(tempArr1)

                tempArr2 = []
                tempArr2.append(user['summoner']['summonerName'])
                tempArr2.append(performanceData['totDPS'])
                tempArr2.append(performanceData['totDamageTaken'])
                tempArr2.append(performanceData['totTurretDamage'])
                tempArr2.append(performanceData['totGoldEarned'])
                tableRow2.append(tempArr2)

                tempArr3 = []
                tempArr3.append(user['summoner']['summonerName'])
                tempArr3.append(performanceData['totVisionScore'])
                tempArr3.append(performanceData['totHealsOnTeammates'])
                tempArr3.append(performanceData['totTimeCCOthers'])
                tempArr3.append(performanceData['totShieldingOthers'])
                tableRow3.append(tempArr3)

            table = t2a(
                header=['Name', 'Total Games', 'Total Kills', 'Total Deaths', 'Total Assists', 'Total CS'],
                body=tableRow1,
                style=PresetStyle.thin_compact
            )
            await ctx.send(f"```\n{table}\n```")

            table = t2a(
                header=['Name', 'Total Damage To Champions', 'Total Damage Taken', 'Total Turret Damage', 'Total Gold Earned'],
                body=tableRow2,
                style=PresetStyle.thin_compact
            )
            await ctx.send(f"```\n{table}\n```")

            table = t2a(
                header=['Name', 'Total Vis. Score', 'Total Heals ', 'Total Time CC-ing Others (s)', 'Total Shielding to Others'],
                body=tableRow3,
                style=PresetStyle.thin_compact
            )
            await ctx.send(f"```\n{table}\n```")

            await ctx.send('Temporary data visualization solution. Improvements made in the future.')

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('You do not have the requirement arguments for this command. Type !help for more details.')
        else:
            await ctx.send(error)

    bot.run(TOKEN)