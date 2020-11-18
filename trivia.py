import discord
import random
import asyncio
import time
import re
import requests

from discord.ext import commands
from tabulate import tabulate
from mongodb_util import get_current_game_question
from mongodb_util import generate_questions_for_game
from mongodb_util import random_question_200
from mongodb_util import random_question_400
from mongodb_util import random_question_600
from mongodb_util import random_question_800
from mongodb_util import random_question_1000
from mongodb_util import insert_new_server_channel_session
from mongodb_util import update_server_channel_session
from mongodb_util import get_server_channel_session
from bs4 import BeautifulSoup as Soup
from collections import Counter

category_key = {"science": 0, "movies & tv": 1, "pop culture": 2, "history": 3, "music": 4, "food & drink": 5}
value_key = {"200": 0, "400": 1, "600": 2, "800": 3, "1000": 4}

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
  
  return True

def create_attempted_table(user_key_mapping):
  attempted_table = []
  for user in user_key_mapping:
    user_attempted = []
    user_attempted.append(user)
    if user_key_mapping[user]["attempted_current_question"]: # can they attempt == X
      user_attempted.append("No")
    else:
      user_attempted.append("Yes")
    attempted_table.append(user_attempted)
  attempted_table_headers = ["user", "can they attempt?"]
  return tabulate(attempted_table, headers=attempted_table_headers, tablefmt="fancy_grid")

#TODO abstract out all of the self. fields into server ID + channel ID specific data in mongodb, that way you isolate sessions.

def create_new_server_channel_session(server_id, channel_id, server_name, channel_name):
  server_channel_session = {}
  server_channel_session["server_name"] = server_name
  server_channel_session["channel_name"] = channel_name
  server_channel_session['session_id'] = str(server_id) + "#" + str(channel_id)
  server_channel_session['current_game_questions'] = {}
  server_channel_session['game_start'] = False
  server_channel_session['question_selector'] = None
  server_channel_session['selected_question'] = None
  server_channel_session['answerer'] = None
  server_channel_session['user_key_mapping'] = {}
  server_channel_session['table'] = [[200, 200, 200, 200, 200, 200],[400, 400, 400, 400, 400, 400],[600, 600, 600, 600, 600, 600],[800, 800, 800, 800, 800, 800],[1000, 1000, 1000, 1000, 1000, 1000]]
  return server_channel_session

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
  
  async def next_question_logic(self, ctx):
    query = get_server_channel_session(ctx.message.guild.id, ctx.message.channel.id)

    if query == None:
      await ctx.send("Looks like your server & channel aren't set up yet. Run the !setup command to create your session.")
      return

    if check_question_grid_empty(query["table"]):
      await ctx.send("We're in the endgame now.")
      # call endgame function
      await ctx.invoke(self.bot.get_command("endgame"))
      
      return

    # Show updated table
    await ctx.send(f'```Question Table: \n{tabulate(query["table"], headers=self.headers, tablefmt="fancy_grid")}```')

    query["question_selector"] = random_player(query["user_key_mapping"])
    await ctx.send(f'It is {query["question_selector"]}\'s turn to select a category!')

    # clear answerer, question
    query["answerer"] = None
    query["selected_question"] = None

    # clear attempted_list
    for user in query["user_key_mapping"]:
      query["user_key_mapping"][user]["attempted_current_question"] = False
    
    update_server_channel_session(query)
    return
  
  @commands.command(description="adds invoker to the list of players prior to game start")
  async def join(self, ctx):

    query = get_server_channel_session(ctx.message.guild.id, ctx.message.channel.id)

    if query == None:
      await ctx.send("Looks like you haven't ran the !setup command yet. Do that first before you join your session. ")
      return
    
    if query["game_start"]:
      await ctx.send("Psst...there's a game currently running. Wait for your turn!")
      return

    user = str(ctx.author).split("#")[0].lower()
    if user in query["user_key_mapping"]:
      await ctx.send(f'Hey {user} you\'re already in the game!')
      return

    player_data = {"attempted_current_question": False, "score": 0}
    query["user_key_mapping"][user] = player_data
    update_server_channel_session(query)
    await ctx.send(f'{user} joined today\'s jeopardy game!')

  @commands.command(description="removes invoker to the list of players prior to game start")
  async def leave(self, ctx):

    query = get_server_channel_session(ctx.message.guild.id, ctx.message.channel.id)

    if query == None:
      await ctx.send("Looks like your server & channel aren't set up yet. Run the !setup command to create your session.")
      return

    user = str(ctx.author).split("#")[0].lower()
    if user not in query["user_key_mapping"]:
      await ctx.send(f'{user} you\'re not in tonight\'s game.''')
      return
    if user in query["user_key_mapping"]:
      user_key_mapping = query["user_key_mapping"]
      del user_key_mapping[user]
      query["user_key_mapping"] = user_key_mapping
    
    update_server_channel_session(query)
    await ctx.send(f'{user}  left today\'s trivia night...smells like chicken!')

  @commands.command(hidden=True)
  async def kickoff_answer_cycle(self, ctx):
    query = get_server_channel_session(ctx.message.guild.id, ctx.message.channel.id)
    channel_id = ctx.message.channel.id
    if query == None:
      await ctx.send("Looks like your server & channel aren't set up yet. Run the !setup command to create your session.")
      return

    # this command starts the buzzing cycle but should not be envoked manually.
    if not query["game_start"]:
      await ctx.send("Game session has not been started yet...run the ```!start_game``` command to commence Trivia Night!")
      return
    # add a table here
    await ctx.send(f'```Who can attempt table: \n{create_attempted_table(query["user_key_mapping"])}```')
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
      if channel.id ==  channel_id:
        messages = await channel.history(limit=len(query["user_key_mapping"]) * 2).flatten()
        break

    #@TODO loop through messages, get all of them, find index of Go! message, take the slice of it, sort the slice
    player_messages = []
    print(messages)
    for message in messages:
      obj = {}
      name = str(message.author).split("#")[0].lower()
      players = [user for user in query["user_key_mapping"]]
      if name != "play-jeopardy" and name not in players:
        continue

      if name != "play-jeopardy" and query["user_key_mapping"][name]["attempted_current_question"]:
        continue
      timestamp = message.created_at.timestamp()
      content = message.system_content
      obj["name"] = name
      obj["timestamp"] = timestamp
      obj["content"] = content
      player_messages.append(obj)

    player_messages = sorted(player_messages, key = lambda msg: msg['timestamp'])    
    print(player_messages)
    timestamp_grid = []
    go_message = [message for message in player_messages if message["content"] == "Go!" and message["name"] == "play-jeopardy"]
    trivia_bot_cutoff = player_messages.index(go_message[0])

    for player_message in player_messages:
      player_list = []
      if player_message["name"] == "play-jeopardy":
        continue
      player_list.append(player_message["name"])
      player_list.append(player_message["timestamp"])
      timestamp_grid.append(player_list)

    if len(player_messages) - 1 == trivia_bot_cutoff:
      #assuming players are giving up
      await ctx.send("Aww, we have a bunch of chickens who didn't wanna buzz! The correct answer is " + f'{query["selected_question"]["answer"]}')
      await self.next_question_logic(ctx)
      return

    answerer = player_messages[trivia_bot_cutoff + 1]["name"].lower()
    query["answerer"] = answerer

    update_server_channel_session(query)

    # print the timestamps so that ppl know who won definitevly
    await ctx.send(f'```Timestamps (lower is better): \n{tabulate(timestamp_grid, headers=["player", "timestamp"], tablefmt="fancy_grid", floatfmt=".3f")}\n{answerer} gets to answer the question!```')
    return 

  @commands.command(description="command to answer the current question (for the person who wins the buzzer)")
  async def answer(self, ctx, answer):

    query = get_server_channel_session(ctx.message.guild.id, ctx.message.channel.id)

    if query == None:
      await ctx.send("Looks like your server & channel aren't set up yet. Run the !setup command to create your session.")
      return

    if not query["game_start"]:
      await ctx.send("Game session has not been started yet...run the ```!start_game``` command to commence Trivia Night!")
      return
    if query["selected_question"] == None or query["answerer"] == None:
      await ctx.send("No question provisioned...maybe select a category first?")
      return
    
    user = str(ctx.author).split('#')[0].lower()
    correct_answer = query["selected_question"]["answer"].lower()
    correct_answer_split = query["selected_question"]["answer"].lower().split(" ")
    answer = answer.lower()
    if query["answerer"] != user:
      await ctx.send("Not your turn...!!")
      return
    else:
      if answer == correct_answer or answer in correct_answer_split:
        # correct! + value to the scoreboard
        await ctx.send(f'Correct!\n{user} is awararded {query["selected_question"]["value"]} points.')

        query["user_key_mapping"][user]["score"] += query["selected_question"]["value"]
        
        # Show updated scoreboard
        await ctx.send(f'```Scoreboard: \n{show_scoreboard(query["user_key_mapping"])}```')

        update_server_channel_session(query)
        await self.next_question_logic(ctx)

        return
      else: 
        # start override process HERE, wait for user input
        answer_table = [[user, answer, correct_answer]]
        answer_headers = ["Name", "Your Answer", "Correct Answer"]
        await ctx.author.send(f'```Trivia night in (Server: {query["server_name"]} Channel: {query["channel_name"]}): If your answer is close enough, use the override command in the trivia-night channel to give yourself the points: \n{tabulate(answer_table, headers=answer_headers, tablefmt="fancy_grid")}```')

        await ctx.send(f'{user}' + ", check your DMs. Do you want to override? Send Y (yes) to override, N (no) to skip.")
        msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        if msg.content == "Y" or msg.content == "y" or msg.content.lower() == "yes":
          await ctx.send(f'{user} has started an override.')
          await ctx.send("The correct answer was: " + "```" + correct_answer + "```")

          await ctx.send(f'{user} is awarded {query["selected_question"]["value"]} points.')

          query["user_key_mapping"][user]["score"] += query["selected_question"]["value"]
            
          # Show updated scoreboard
          await ctx.send(f'```Scoreboard: \n{show_scoreboard(query["user_key_mapping"])}```')
          update_server_channel_session(query)
          # check if there are questions left
          await self.next_question_logic(ctx)
          return
        else:
          query["user_key_mapping"][user]["attempted_current_question"] = True

          every_player_attempted = all(query["user_key_mapping"][user]["attempted_current_question"] == True for user in query["user_key_mapping"])
          if every_player_attempted:
            # do not go back to the kick off answer cycle, end the current cycle
            await ctx.send(f'Looks like that question stumped everyone! The correct answer is {query["selected_question"]["answer"]}')

            await self.next_question_logic(ctx)

          else:
            # incorrect! restart the kickoff question process
            await ctx.send("Womp womp! Incorrect!\nRest of the players (who have not attempted to answer the question) can steal.")
            update_server_channel_session(query)
            await ctx.invoke(self.bot.get_command("kickoff_answer_cycle"))
          return
      
  @commands.command(description="selects a question category and value")
  async def select(self, ctx, category, value):

    query = get_server_channel_session(ctx.message.guild.id, ctx.message.channel.id)

    if query == None:
      await ctx.send("Looks like your server & channel aren't set up yet. Run the !setup command to create your session.")
      return

    if not query["game_start"]:
      await ctx.send("Game session has not been started yet...run the ```!start_game``` command to commence Trivia Night!")
      return
    user = str(ctx.author).split('#')[0]

    if question_already_selected(query["table"], category, value):
      await ctx.send("That category has already been selected! Pick another one please.")
      return

    # reset attempted question field
    for user in query["user_key_mapping"]:
      query["user_key_mapping"][user]["attempted_current_question"] = False
    category = category.lower()

    # check if there are URLs in the question
    question = get_current_game_question(query, category, value)
    print(question)
    question_text = question["question"]
    parser = Soup(question_text, 'html.parser')
    urls_in_question = [a['href'] for a in parser.find_all('a')]
    cleaned_question = re.sub(re.compile('<.*?>'), '', question_text)

    # clean up everything between < > characters
    await ctx.send(f'{query["question_selector"]} selected {category} for {value}.')
    query["selected_question"] = question
    new_table = mark_question_selected(query["table"], category, int(value))
    query["table"] = new_table
    
    update_server_channel_session(query)

    await ctx.send("```Question: " + cleaned_question + "```")
    if len(urls_in_question) != 0:
      for url in urls_in_question:
        if requests.get(url).status_code == 404:
          continue
        
        if url[-3:] == "mp3":
          continue
        embed_obj = discord.Embed()
        embed_obj.set_image(url=url)
        await ctx.send(embed=embed_obj)
    await ctx.invoke(self.bot.get_command("kickoff_answer_cycle"))

  # start game
  @commands.command(description="starts the game", pass_context=True)
  async def start_game(self, ctx):
    # create a session for the channel + server
    query = get_server_channel_session(ctx.message.guild.id, ctx.message.channel.id)

    if query == None:
      await ctx.send("Looks like your server & channel aren't set up yet. Run the !setup command to create your session.")
      return
    
    if len(query["user_key_mapping"]) == 0:
      await ctx.send("We're gonna need some players first...use the ```!join``` command to add yourself to the game.")
      return

    query["current_game_questions"] = generate_questions_for_game()
    await ctx.send(f'```Question Table: \n{tabulate(query["table"], headers=self.headers, tablefmt="fancy_grid")}```')

    await ctx.send(f'```Scoreboard: \n{show_scoreboard(query["user_key_mapping"])}```')

    # randomly select first player to select question
    
    query["game_start"] = True
    query["question_selector"] = random_player(query["user_key_mapping"])
    update_server_channel_session(query)
    await ctx.send(f'It is {query["question_selector"]}\'s turn to select a category!')

  @commands.command(description="ends the game, and declares a winner. only use if you need to stop the game, because this happens naturally when all questions are selected. ")
  async def endgame(self, ctx):
    query = get_server_channel_session(ctx.message.guild.id, ctx.message.channel.id)

    if query == None:
      await ctx.send("Looks like your server & channel aren't set up yet. Run the !setup command to create your session.")
      return

    await ctx.send(f'```Scoreboard: \n{show_scoreboard(query["user_key_mapping"])}```')
    winner = max(query["user_key_mapping"].keys(), key=(lambda key: query["user_key_mapping"][key]["score"]))

    winning_score = query["user_key_mapping"][winner]["score"]
    scores = [query["user_key_mapping"][key]["score"] for key in query["user_key_mapping"]]

    num_each_score = Counter(scores)

    if num_each_score[winning_score] > 1:
      await ctx.send("We have a tie! Commencing the tiebreak question, winner takes all!")
      random_question_list = []
      for category in self.headers:
        random_question_list.append(random_question_200(category))
        random_question_list.append(random_question_400(category))
        random_question_list.append(random_question_600(category))
        random_question_list.append(random_question_800(category))
        random_question_list.append(random_question_1000(category))
      random.shuffle(random_question_list)
      question = random_question_list[0]
      query["selected_question"] = question
      question_text = question["question"]
      parser = Soup(question_text, 'html.parser')
      urls_in_question = [a['href'] for a in parser.find_all('a')]
      cleaned_question = re.sub(re.compile('<.*?>'), '', question_text)
      await ctx.send("```Question: " + cleaned_question + "```")
      if len(urls_in_question) != 0:
        for url in urls_in_question:
          if requests.get(url).status_code == 404:
            continue
          if url[-3:] == "mp3":
            continue
          embed_obj = discord.Embed()
          embed_obj.set_image(url=url)
          await ctx.send(embed=embed_obj)
      await ctx.invoke(self.bot.get_command("kickoff_answer_cycle"))
      return


    await ctx.send(f'Congratulations to {winner} for winning today\'s jeopardy game!')

    query = create_new_server_channel_session(ctx.message.guild.id, ctx.message.channel.id, ctx.message.guild.name, ctx.message.channel.name)
    update_server_channel_session(query)

    return

  @commands.command(description="tutorial on how the trivia-bot works")
  async def info(self, ctx):
    await ctx.send("```Play-Jeopardy How To:\n\nFirst, run the !setup command to create a session dedicated to your server and channel. You only need to do this once. \n\nTo join the game, players need to use the !join the game. Once players have joined, run the start command to start the game. \n\nTrivia-Bot will show a table of categories, the score, and randomly select a player to select a question.\n\nThis player can use the !select command to pick a category and a value.\n\nIf the category has a space in it (e.g. food & drink or movies & tv) you'll need to wrap the category in quotes - !select \"movies & tv\" 400. \n\nOnce the question is picked, Play-Jeopardy will initate a countdown. After the bot sends \"Go!\" to the channel, the buzzing window starts. \n\nType any message to the channel (don't prepend with an !) and Play-Jeopardy will pick the message that came right after \"Go!\". Sometimes you'll probably see your message first on your discord client and your friends might see the same for them on their client, so Play-Jeopardy also sends a table of message timestamps so no one can dispute who was first. \n\nThe player who gets to answer uses the !answer command followed by their answer wrapped in quotes (e.g. !answer \"hello world\"). \n\nIf the player gets the answer right off the bat, the game continues as normal - the previous answerer gets to pick the new category and the cycle restarts from there. \n\nIf Play-Jeopardy is unsure if your answer is correct or incorrect, it will DM you the correct answer, and your answer for you to make the best judgement on whether or not you got it right. Play-Jeopardy will wait for your input in the channel, and you can type Y or N to proceed. \n\nY overrides and gives you the points, and continues. N does not override and lets other players steal. \n\nWhen all questions are selected, the game ends, and a winner is declared. \n\nHappy Jeopardy-ing!```")    
      
  @commands.command(description="set up trivia-bot for your server + channel")
  async def setup(self, ctx):
    session = create_new_server_channel_session(ctx.message.guild.id, ctx.message.channel.id, ctx.message.guild.name, ctx.message.channel.name)

    query = get_server_channel_session(ctx.message.guild.id, ctx.message.channel.id)
    if query != None:
      await ctx.send("Looks like you've already initiated the setup! Use the !join command to join the session, and !start_game to start.")
      return

    insert_new_server_channel_session(session)
    await ctx.send("Server & Channel Session Created!")

def setup(bot):
    bot.add_cog(Trivia(bot))
    