import os

import discord
import random
import asyncio
import time

from discord.ext import commands
from tabulate import tabulate
from mongodb_util import get_current_game_question
from mongodb_util import generate_questions_for_game

category_key = {"science": 0, "movies & tv": 1, "pop culture": 2, "history": 3, "music": 4, "food & drink": 5}
value_key = {"200": 0, "400": 1, "600": 2, "800": 3, "1000": 4}
user_key_mapping = {"beemu": 0, "docquan": 1, "bombuh": 2, "parz": 3, "0": "beemu", "1": "docquan", "2": "bombuh", "3": "parz"}

def show_scoreboard(scoreboard):
  # show scoreboard
  return tabulate(scoreboard, headers=["beemu", "docquan", "bombuh", "parz"], tablefmt="fancy_grid")

def random_player():
  players = ["beemu", "docquan", "bombuh", "parz"]
  random_player = players[random.randint(0, 3)]
  return random_player

def mark_question_selected(table, category, value):
  category = category.lower()
  c_key = category_key[category]
  v_key = value_key[str(value)]
  table[v_key][c_key] = "---"
  return table

def question_already_selected(table, category, value):
  category = category.lower()
  c_key = category_key[category]
  v_key = value_key[str(value)]
  if table[v_key][c_key] == "---":
    return True
  else:
    return False

def check_question_grid_empty(table):
  for value in table:
    for category in value:
      if category != "---":
        return False
  
  return true

class Trivia(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.game_start = False
    self.question_selector = None
    self.headers = ["Science", "Movies & TV", "Pop Culture", "History", "Music", "Food & Drink"]
    self.table = [[200, 200, 200, 200, 200, 200],[400, 400, 400, 400, 400, 400],[600, 600, 600, 600, 600, 600],[800, 800, 800, 800, 800, 800],[1000, 1000, 1000, 1000, 1000, 1000]]
    self.current_question = None
    self.answerer = None
    self.scoreboard = [[0, 0, 0, 0]]
    self.attempted_list = [False, False, False, False]

  @commands.command()
  async def arise(self, ctx):
    await ctx.send("I have arisen.") # set tts flag to true --> ctx.send("message", tts=True)

  @commands.command()
  async def kickoff_answer_cycle(self, ctx):
    if not self.game_start:
      await ctx.send("Game session has not been started yet...run the ```!start_game``` command to commence Trivia Night!")
      return
    print(ctx.guild.text_channels)
    await ctx.send("After I say 'Go!', first person to send a message(ONE MESSAGE) to the channel gets to answer the question. \nNote: If you got the question wrong earlier you are NOT allowed to participate.\nDo not begin typing until I say go.")
    await asyncio.sleep(5)
    await ctx.send("3")
    await asyncio.sleep(random.randint(1, 5))
    await ctx.send("2")
    await asyncio.sleep(random.randint(1,5))
    await ctx.send("1")
    await asyncio.sleep(random.randint(1,5))
    await ctx.send("Go!") # I should grab this message also
    await asyncio.sleep(5)
    answerer = None
    messages = None
    for channel in ctx.guild.text_channels:
      if channel.name == "trivia-night":
        messages = await channel.history(limit=4).flatten()
        # if message appears before Go!, consider disqualifying the person that sent that message, increase limit to 10 maybe.
        # condition for the answerer is first valid message AFTER Go!
        break

    player_messages = []
    for message in messages:
      obj = {}
      name = str(message.author).split("#")[0]
      if name == "trivia-bot":
        continue
      timestamp = message.created_at.timestamp()
      content = message.system_content
      obj["name"] = name
      obj["timestamp"] = timestamp
      obj["content"] = content
      player_messages.append(obj)

    player_messages = sorted(player_messages, key = lambda msg: msg['timestamp'])

    answerer = player_messages[0]["name"].lower()
    self.answerer = answerer
    print(messages)
    print(player_messages)

    #answerer gets to answer the question, create an answer command
    await ctx.send(f'{answerer}' + " gets to answer the question!")
    return 

  @commands.command()
  async def answer_question(self, ctx, answer):
    if not self.game_start:
      await ctx.send("Game session has not been started yet...run the ```!start_game``` command to commence Trivia Night!")
      return
    if self.current_question == None or self.answerer == None:
      await ctx.send("No question provisioned...maybe select a category first?")
      return
    
    user = str(ctx.author).split('#')[0].lower()
    correct_answer = self.current_question["answer"].lower()
    correct_answer_split = self.current_question["answer"].lower().split(" ")
    answer = answer.lower()
    if self.answerer != user:
      await ctx.send("Not your turn...50 pts will be deducted!!")
    else:
      if answer in correct_answer or answer == correct_answer or answer in correct_answer_split:
        # correct! + value to the scoreboard
        await ctx.send("Correct!\n" + f'{user}' + " is awarded " + f'{self.current_question["value"]}' + ".")

        self.scoreboard[0][user_key_mapping[user]] += self.current_question["value"]

        # if user == "beemu":
        #   self.scoreboard[0][0] += self.current_question["value"]
        # elif user == "docquan":
        #   self.scoreboard[0][1] += self.current_question["value"]
        # elif user == "bombuh":
        #   self.scoreboard[0][2] += self.current_question["value"]
        # elif user == "parz":
        #   self.scoreboard[0][3] += self.current_question["value"]
        
        # Show updated scoreboard
        await ctx.send("```Scoreboard: \n" + f'{show_scoreboard(self.scoreboard)}' + "```")

        # check if there are questions left
        if check_question_grid_empty(self.table):
          await ctx.send("We're in the endgame now.")
          # call endgame function

          return

        # Show updated table
        await ctx.send("```Question Table: \n" + f'{tabulate(self.table, headers=self.headers, tablefmt="fancy_grid")}' + "```")

        # Set user as the next selector
        self.question_selector = user
        await ctx.send("It is " + f'{self.question_selector}' + "\'s turn to select a category!")

        # clear answer, question
        self.answerer = None
        self.question = None

        return
      else: 
        # incorrect! restart the kickoff question process
        await ctx.send("Womp womp! Incorrect!\nRest of the players (who have not attempted to answer the question) can steal.")
        # mark user as attempted in the attempted list

        self.attempted_list[user_key_mapping[user]] = True 

        print("attempted list: ", self.attempted_list)

        every_player_attempted = all(player == True for player in self.attempted_list)
        if every_player_attempted:
          # do not go back to the kick off answer cycle, end the current cycle
          await ctx.send("Looks like that question stumped everyone! The correct answer is " + f'{self.current_question["answer"]}')

          # check if there are questions left
          if check_question_grid_empty(self.table):
            await ctx.send("We're in the endgame now.")
            # call endgame function

            return


          # Show updated table
          await ctx.send("```Question Table: \n" + f'{tabulate(self.table, headers=self.headers, tablefmt="fancy_grid")}' + "```")

          self.question_selector = random_player()
          await ctx.send("It is " + f'{self.question_selector}' + "\'s turn to select a category!")

          # clear answer, question
          self.answerer = None
          self.question = None

          # clear attempted_list
          self.attempted_list = [False, False, False, False]
        else:
          await ctx.invoke(self.bot.get_command("kickoff_answer_cycle"))
        return
      
  @commands.command()
  async def select(self, ctx, category, value):
    if not self.game_start:
      await ctx.send("Game session has not been started yet...run the ```!start_game``` command to commence Trivia Night!")
      return
    user = str(ctx.author).split('#')[0]

    if question_already_selected(self.table, category, value):
      await ctx.send("That category has already been selected! Pick another one please.")
      return

    category = category.lower()
    question = get_current_game_question(category, value)
    await ctx.send(f'{user}' + " selected " + f'{category}' + " for " + f'{value}')
    self.current_question = question
    print("answer: " + question["answer"])
    new_table = mark_question_selected(self.table, category, int(value))
    self.table = new_table
    await ctx.send("```" + question["question"] + "```")

    await ctx.invoke(self.bot.get_command("kickoff_answer_cycle"))

  # start game
  @commands.command()
  async def start_game(self, ctx):
    generate_questions_for_game()
    await ctx.send("```Question Table: \n" + f'{tabulate(self.table, headers=self.headers, tablefmt="fancy_grid")}' + "```")

    await ctx.send("```Scoreboard: \n" + f'{show_scoreboard(self.scoreboard)}' + "```")

    # randomly select first player to select question
    
    self.game_start = True

    self.question_selector = random_player()
    await ctx.send("It is " + f'{self.question_selector}' + "\'s turn to select a category!")

  @commands.command()
  async def endgame(self, ctx):
    await ctx.send("```Scoreboard: \n" + f'{show_scoreboard(self.scoreboard)}' + "```")

    scores = self.scoreboard[0]
    index = scores.index(max(scores))
    winner = user_key_mapping[str(index)]

    await ctx.send("Congratulations to " + f'{winner}' "!!")

    self.game_start = False
    self.question_selector = None
    self.headers = ["Science", "Movies & TV", "Pop Culture", "History", "Music", "Food & Drink"]
    self.table = [[200, 200, 200, 200, 200, 200],[400, 400, 400, 400, 400, 400],[600, 600, 600, 600, 600, 600],[800, 800, 800, 800, 800, 800],[1000, 1000, 1000, 1000, 1000, 1000]]
    self.current_question = None
    self.answerer = None
    self.scoreboard = [[0, 0, 0, 0]]
    self.attempted_list = [False, False, False, False]

    return

      
      

def setup(bot):
    bot.add_cog(Trivia(bot))
    