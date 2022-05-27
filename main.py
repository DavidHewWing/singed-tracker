import os

from flask import escape
import functions_framework

from dotenv import load_dotenv

from discord.discord import run_discord
from cronjob.cronjob import detectGamesForAllGuilds, getPerformanceData
from data.summoner import Summoner
from data.user import User

from mongo.mongo_controller import addGuild, addUserToGuild, connectToMongoAndReturnClient, deleteGuild, deleteUserInGuild, getAllGuilds, getAllUsersInGuildNoPerfData, getUserInGuildByDiscordId

load_dotenv()
MONGO_URI = os.environ.get('MONGO_URI') if os.getenv('MONGO_URI') == 'None' else os.getenv('MONGO_URI')
TOKEN = os.environ.get('DISCORD_TOKEN') if os.getenv('DISCORD_TOKEN') == 'None' else os.getenv('DISCORD_TOKEN')
RITO_URI = os.environ.get('RITO_BASE_URI') if os.getenv('RITO_BASE_URI') == 'None' else os.getenv('RITO_BASE_URI')
RITO_REGION_BASE_URI = os.environ.get('RITO_REGION_BASE_URI') if os.getenv('RITO_REGION_BASE_URI') == 'None' else os.getenv('RITO_REGION_BASE_URI')
RITO_API_KEY = os.environ.get('RITO_API_KEY') if os.getenv('RITO_API_KEY') == 'None' else os.getenv('RITO_API_KEY')

@functions_framework.http
def run_cronjob(request):
    mongoClient = connectToMongoAndReturnClient(MONGO_URI)
    matches = detectGamesForAllGuilds(mongoClient, 5)
    performanceData = getPerformanceData(mongoClient, matches)
    return {
        'data': performanceData
    }
