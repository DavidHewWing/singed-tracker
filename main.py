import os

from dotenv import load_dotenv

from discord.discord import run_discord

load_dotenv()

if __name__ == '__main__':
    print('main.py is running!')
    run_discord()
