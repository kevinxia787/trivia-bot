import os
import discord
import redis

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv() # comment out when deploying
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# redis_server = redis.Redis() # create redis access

# DISCORD_TOKEN = str(redis_server.get('DISCORD_TOKEN').decode('utf-8'))

startup_ext = ["trivia"]

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
  print("Trivia Bot Running")  

if __name__ == "__main__":
    for ext in startup_ext:
        try:
            bot.load_extension(ext)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(ext, exc))


bot.run(DISCORD_TOKEN)