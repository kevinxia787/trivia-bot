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

def show_scoreboard(user_key_mapping):
  scoreboard = [[]]
  headers = []
  for user in user_key_mapping:
    headers.append(user)
    scoreboard[0].append(user_key_mapping[user]["score"])
  # show scoreboard
  return tabulate(scoreboard, headers=headers, tablefmt="fancy_grid")

def random_player(user_key_mapping):
  players = [user for user in user_key_mapping]
  random_player = players[random.randint(0, len(players) - 1)]
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
    self.user_key_mapping = {}
    self.override = False
  
  @commands.command(description="adds invoker to the list of players prior to game start")
  async def join(self, ctx):
    if self.game_start:
      await ctx.send("Psst...there's a game currently running. Wait for your turn!")
      return
    user = str(ctx.author).split("#")[0].lower()
    if user in self.user_key_mapping:
      await ctx.send("Hey " + f'{user}' + ", you're already in the game!")
      return
    player_data = {"attempted_current_question": False, "score": 0}
    self.user_key_mapping[user] = player_data
    print(self.user_key_mapping)
    await ctx.send(f'{user}' + " joined today's trivia night!")

  @commands.command(description="removes invoker to the list of players prior to game start")
  async def leave(self, ctx):
    user = str(ctx.author).split("#")[0].lower()
    if user not in self.user_key_mapping:
      await ctx.send(f'{user}' + " you're not in tonight's game. ")
      return
    if user in self.user_key_mapping:
      del self.user_key_mapping[user]
    print(self.user_key_mapping)
    await ctx.send(f'{user}' + " left today's trivia night...smells like chicken!")

  @commands.command(description="starts 'buzzer' cycle. do not call this manually as a non-bot user")
  async def kickoff_answer_cycle(self, ctx):
    # this command starts the buzzing cycle but should not be envoked manually.
    if not self.game_start:
      await ctx.send("Game session has not been started yet...run the ```!start_game``` command to commence Trivia Night!")
      return
    await ctx.send("After I say 'Go!', first person to send a message(ONE MESSAGE) to the channel gets to answer the question. \nNote: If you got the question wrong earlier you are NOT allowed to participate.")
    await asyncio.sleep(5)
    await ctx.send("3")
    await asyncio.sleep(random.randint(1, 5))
    await ctx.send("2")
    await asyncio.sleep(random.randint(1,5))
    await ctx.send("1")
    await asyncio.sleep(random.randint(1,5))
    await ctx.send("Go!")
    await asyncio.sleep(5)
    answerer = None
    messages = None
    for channel in ctx.guild.text_channels:
      if channel.name == "trivia-night":
        messages = await channel.history(limit=len(self.user_key_mapping) * 2).flatten()
        break

    player_messages = []
    for message in messages:
      obj = {}
      name = str(message.author).split("#")[0].lower()
      players = [user for user in self.user_key_mapping]
      if name == "trivia-bot" or self.user_key_mapping[name]["attempted_current_question"] or name not in players:
        continue
      timestamp = message.created_at.timestamp()
      content = message.system_content
      obj["name"] = name
      obj["timestamp"] = timestamp
      obj["content"] = content
      player_messages.append(obj)

    player_messages = sorted(player_messages, key = lambda msg: msg['timestamp'])
    timestamp_grid = []
    for player_message in player_messages:
      player_list = []
      player_list.append(player_message["name"])
      player_list.append(player_message["timestamp"])
      timestamp_grid.append(player_list)
    
    answerer = player_messages[0]["name"].lower()
    self.answerer = answerer

    # print the messages so that ppl know who won definitevly
    await ctx.send("```Timestamps (lower is better): \n" + f'{tabulate(timestamp_grid, headers=["player", "timestamp"], tablefmt="fancy_grid", floatfmt=".3f")}' +  "\n" f'{answerer}' + " gets to answer the question!```")
    return 

  @commands.command(description="command to answer the current question (for the person who wins the buzzer)")
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
    self.override = None
    answer = answer.lower()
    if self.answerer != user:
      await ctx.send("Not your turn...!!")
    else:
      if answer in correct_answer or answer == correct_answer or answer in correct_answer_split:
        # correct! + value to the scoreboard
        await ctx.send("Correct!\n" + f'{user}' + " is awarded " + f'{self.current_question["value"]}' + ".")

        self.user_key_mapping[user]["score"] += self.current_question["value"]
        
        # Show updated scoreboard
        await ctx.send("```Scoreboard: \n" + f'{show_scoreboard(self.user_key_mapping)}' + "```")

        # check if there are questions left
        if check_question_grid_empty(self.table):
          await ctx.send("We're in the endgame now.")
          # call endgame function
          self.bot.get_command("endgame")
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
        # start override process HERE, wait for user input
        await ctx.author.send("The correct answer was: ```" + f'{correct_answer}' + "```")
        await ctx.author.send("You answered: ```" + f'{answer}' + "```")
        await ctx.author.send("If it's good enough, you can override.")
        await ctx.send("Run override command if you were correct. If I don't hear from you in 10 seconds I am assuming you got the answer wrong. ")
        await asyncio.sleep(10)
        if self.override:
          return

        self.user_key_mapping[user]["attempted_current_question"] = True

        every_player_attempted = all(self.user_key_mapping[user]["attempted_current_question"] == True for user in self.user_key_mapping)
        if every_player_attempted:
          # do not go back to the kick off answer cycle, end the current cycle
          await ctx.send("Looks like that question stumped everyone! The correct answer is " + f'{self.current_question["answer"]}')

          # check if there are questions left
          if check_question_grid_empty(self.table):
            await ctx.send("We're in the endgame now.")
            # call endgame function
            self.bot.get_command("endgame")
            return

          # Show updated table
          await ctx.send("```Question Table: \n" + f'{tabulate(self.table, headers=self.headers, tablefmt="fancy_grid")}' + "```")

          self.question_selector = random_player(self.user_key_mapping)
          await ctx.send("It is " + f'{self.question_selector}' + "\'s turn to select a category!")

          # clear answer, question
          self.answerer = None
          self.question = None

          # clear attempted_list
          for user in self.user_key_mapping:
            self.user_key_mapping[user]["attempted_current_question"] = False

        else:
          # incorrect! restart the kickoff question process
          await ctx.send("Womp womp! Incorrect!\nRest of the players (who have not attempted to answer the question) can steal.")
          # mark user as attempted in the attempted list

          print("attempted list: ", [(player, self.user_key_mapping[player]["attempted_current_question"]) for player in self.user_key_mapping])
          
          await ctx.invoke(self.bot.get_command("kickoff_answer_cycle"))
        return
      
  @commands.command(description="selects a question category and value")
  async def select(self, ctx, category, value):
    if not self.game_start:
      await ctx.send("Game session has not been started yet...run the ```!start_game``` command to commence Trivia Night!")
      return
    user = str(ctx.author).split('#')[0]

    if question_already_selected(self.table, category, value):
      await ctx.send("That category has already been selected! Pick another one please.")
      return

    self.override = None
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
  @commands.command(description="starts the game")
  async def start_game(self, ctx):
    if len(self.user_key_mapping) == 0:
      await ctx.send("We're gonna need some players first...use the ```!join``` command to add yourself to the game.")
      return

    generate_questions_for_game()
    await ctx.send("```Question Table: \n" + f'{tabulate(self.table, headers=self.headers, tablefmt="fancy_grid")}' + "```")

    await ctx.send("```Scoreboard: \n" + f'{show_scoreboard(self.user_key_mapping)}' + "```")

    # randomly select first player to select question
    
    self.game_start = True

    self.question_selector = random_player(self.user_key_mapping)
    await ctx.send("It is " + f'{self.question_selector}' + "\'s turn to select a category!")

  @commands.command(description="overrides the incorrect answer, user gets the points (misspellings, off by one char, weird formatting, etc)")
  async def override(self, ctx):
    user = str(ctx.author).split("#")[0]
    correct_answer = self.current_question["answer"]
    if self.answerer != user:
      await ctx.send("You're not allowed to run this command.")
      return
    else:
      await ctx.send(f'{user}' + " has started an override.")
      self.override = True
      await ctx.send("The correct answer was: " + "```" + correct_answer + "```")

      await ctx.send(f'{user}' + " is awarded " + f'{self.current_question["value"]}' + ".")

      self.user_key_mapping[user]["score"] += self.current_question["value"]
        
      # Show updated scoreboard
      await ctx.send("```Scoreboard: \n" + f'{show_scoreboard(self.user_key_mapping)}' + "```")

      # check if there are questions left
      if check_question_grid_empty(self.table):
        await ctx.send("We're in the endgame now.")
        self.bot.get_command("endgame")
        return

      # Show updated table
      await ctx.send("```Question Table: \n" + f'{tabulate(self.table, headers=self.headers, tablefmt="fancy_grid")}' + "```")

      # Set user as the next selector
      self.question_selector = user
      await ctx.send("It is " + f'{self.question_selector}' + "\'s turn to select a category!")

      # clear answer, question
      self.answerer = None
      self.question = None


  @commands.command(description="ends the game, and declares a winner. only use if you need to stop the game, because this happens naturally when all questions are selected. ")
  async def endgame(self, ctx):
    await ctx.send("```Scoreboard: \n" + f'{show_scoreboard(self.user_key_mapping)}' + "```")
    winner = max(self.user_key_mapping.keys(), key=(lambda key: self.user_key_mapping[key]["score"]))

    await ctx.send("Congratulations to " + f'{winner}' " for winning today's trivia night!!")

    self.game_start = False
    self.question_selector = None
    self.headers = ["Science", "Movies & TV", "Pop Culture", "History", "Music", "Food & Drink"]
    self.table = [[200, 200, 200, 200, 200, 200],[400, 400, 400, 400, 400, 400],[600, 600, 600, 600, 600, 600],[800, 800, 800, 800, 800, 800],[1000, 1000, 1000, 1000, 1000, 1000]]
    self.current_question = None
    self.answerer = None
    self.user_key_mapping = {}

    return

      
      

def setup(bot):
    bot.add_cog(Trivia(bot))
    