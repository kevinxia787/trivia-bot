import os

import discord
import random
import asyncio

from discord.ext import commands
from tabulate import tabulate
from mongodb_util import get_current_game_question
from mongodb_util import generate_questions_for_game

def show_scoreboard():
  # show scoreboard
  score_board = [[0, 0, 0, 0]]
  return tabulate(score_board, headers=["beemu", "docquan", "bombuh", "parz"], tablefmt="fancy_grid")

def random_player():
  players = ["beemu", "docquan", "bombuh", "parz"]
  random_player = players[random.randint(0, 3)]
  return random_player

def mark_question_selected(table, category, value):
  category = category.lower()
  if category == "science":
    if value == 200:
      table[0][0] = "X"
    elif value == 400:
      table[1][0] = "X"
    elif value == 600:
      table[2][0] = "X"
    elif value == 800:
      table[3][0] = "X"
    elif value == 1000:
      table[4][0] = "X"
  elif category == "movies & tv":
    if value == 200:
      table[0][1] = "X"
    elif value == 400:
      table[1][1] = "X"
    elif value == 600:
      table[2][1] = "X"
    elif value == 800:
      table[3][1] = "X"
    elif value == 1000:
      table[4][1] = "X"
  elif category == "pop culture":
    if value == 200:
      table[0][2] = "X"
    elif value == 400:
      table[1][2] = "X"
    elif value == 600:
      table[2][2] = "X"
    elif value == 800:
      table[3][2] = "X"
    elif value == 1000:
      table[4][2] = "X"
  elif category == "history":
    if value == 200:
      table[0][3] = "X"
    elif value == 400:
      table[1][3] = "X"
    elif value == 600:
      table[2][3] = "X"
    elif value == 800:
      table[3][3] = "X"
    elif value == 1000:
      table[4][3] = "X"
  elif category == "music":
    if value == 200:
      table[0][4] = "X"
    elif value == 400:
      table[1][4] = "X"
    elif value == 600:
      table[2][4] = "X"
    elif value == 800:
      table[3][4] = "X"
    elif value == 1000:
      table[4][4] = "X"
  elif category == "food & drink":
    if value == 200:
      table[0][5] = "X"
    elif value == 400:
      table[1][5] = "X"
    elif value == 600:
      table[2][5] = "X"
    elif value == 800:
      table[3][5] = "X"
    elif value == 1000:
      table[4][5] = "X"
  
  return table

def check_question_grid():
  pass

class Trivia(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.game_start = False
    self.question_selector = None
    self.headers = ["Science", "Movies & TV", "Pop Culture", "History", "Music", "Food & Drink"]
    self.table = [[200, 200, 200, 200, 200, 200],[400, 400, 400, 400, 400, 400],[600, 600, 600, 600, 600, 600],[800, 800, 800, 800, 800, 800],[1000, 1000, 1000, 1000, 1000, 1000]]
    self.current_question = None
    self.answerer = None

  @commands.command()
  async def arise(self, ctx):
    await ctx.send("I have arisen.") # set tts flag to true --> ctx.send("message", tts=True)

  @commands.command()
  async def answer_question(self, ctx):
    print(ctx.guild.text_channels)
    await ctx.send("After I say 'Go!', 'buzz' a message to the channel (it can be anything) to get to answer this question! \n Note: If you got the question wrong earlier you are NOT allowed to participate.")
    await asyncio.sleep(10)
    await ctx.send("3")
    await asyncio.sleep(random.randint(1, 5))
    await ctx.send("2")
    await asyncio.sleep(random.randint(1,5))
    await ctx.send("1")
    await asyncio.sleep(random.randint(1,5))
    await ctx.send("Go!")
    await asyncio.sleep(5)
    answerer = None
    for channel in ctx.guild.text_channels:
      if channel.name == "trivia-night":
        messages = await channel.history(limit=4, oldest_first=True).flatten()
        # if message appears before Go!, consider disqualifying the person that sent that message, increase limit to 10 maybe.
        # condition for the answerer is first valid message AFTER Go!
        answerer = messages[0].author.name
        print(answerer)
        break
    
    self.answerer = answerer
    # answerer gets to answer the question, create an answer command
  

  @commands.command()
  async def select(self, ctx, category, value):
    user = str(ctx.author).split('#')[0]
    question = get_current_game_question(category, value)
    await ctx.send(f'{user}' + " selected " + f'{category}' + " for " + f'{value}')
    print(question["answer"])
    self.current_question = question
    new_table = mark_question_selected(self.table, category, int(value))
    print(new_table)
    self.table = new_table
    await ctx.send("```" + question["question"] + "```")

    await ctx.invoke(self.bot.get_command("answer_question"))

  # start game functionality, never ending loop that has local variables of all of the players + scores, and constantly shows the table of questions
  @commands.command()
  async def start_game(self, ctx):
    generate_questions_for_game()
    await ctx.send("```Question Table: \n" + f'{tabulate(self.table, headers=self.headers, tablefmt="fancy_grid")}' + "```")

    await ctx.send("```Scoreboard: \n" + f'{show_scoreboard()}' + "```")

    # randomly select first player to select question
    
    self.question_selector = random_player()
    await ctx.send("It is " + f'{self.question_selector}' + "\'s turn to select a category!")

      
      

def setup(bot):
    bot.add_cog(Trivia(bot))