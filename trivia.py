import os

import discord

from discord.ext import commands

class Trivia(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def arise(self, ctx):
    await ctx.send("I have arisen.") # set tts flag to true --> ctx.send("message", tts=True)

  @commands.command()
  async def pick_question(self, ctx, category, value):
    

def setup(bot):
    bot.add_cog(Trivia(bot))