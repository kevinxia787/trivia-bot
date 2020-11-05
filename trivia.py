import os

import discord

from discord.ext import commands
from mongodb_util import get_current_game_question
from mongodb_util import generate_questions_for_game

class Trivia(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def arise(self, ctx):
    await ctx.send("I have arisen.") # set tts flag to true --> ctx.send("message", tts=True)

  @commands.command()
  async def create_game(self, ctx):
    generate_questions_for_game()
    await ctx.send("Generated the questions!")

  @commands.command()
  async def select(self, ctx, category, value):
    user = str(ctx.author).split('#')[0]
    question = get_current_game_question(category, value)
    await ctx.send(f'{user}' + " selected " + f'{category}' + " for " + f'{value}')
    print(question["answer"])
    await ctx.send(question["question"])

  
  # start game functionality, never ending loop that has local variables of all of the players + scores, and constantly shows the table of questions


def setup(bot):
    bot.add_cog(Trivia(bot))