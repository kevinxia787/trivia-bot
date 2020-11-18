import os

import pymongo
import re
import unidecode

from pymongo import MongoClient
from dotenv import load_dotenv

# client = MongoClient() # local dev

# load_dotenv() # comment out when deploying
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

client_url = "mongodb+srv://" + MONGO_USER + ":" + MONGO_PASSWORD + "@question-cluster.lg2yr.mongodb.net/trivia-bot-db?retryWrites=true&w=majority"
client = pymongo.MongoClient(client_url)

trivia_bot_db = client.trivia_bot_db

current_game = trivia_bot_db.current_game

science_200 = trivia_bot_db.science_200
science_400 = trivia_bot_db.science_400
science_600 = trivia_bot_db.science_600
science_800 = trivia_bot_db.science_800
science_1000 = trivia_bot_db.science_1000

movies_tv_200 = trivia_bot_db.movies_tv_200
movies_tv_400 = trivia_bot_db.movies_tv_400
movies_tv_600 = trivia_bot_db.movies_tv_600 
movies_tv_800 = trivia_bot_db.movies_tv_800
movies_tv_1000 = trivia_bot_db.movies_tv_1000

pop_culture_200 = trivia_bot_db.pop_culture_200
pop_culture_400 = trivia_bot_db.pop_culture_400
pop_culture_600 = trivia_bot_db.pop_culture_600
pop_culture_800 = trivia_bot_db.pop_culture_800
pop_culture_1000 = trivia_bot_db.pop_culture_1000

history_200 = trivia_bot_db.history_200
history_400 = trivia_bot_db.history_400
history_600 = trivia_bot_db.history_600
history_800 = trivia_bot_db.history_800
history_1000 = trivia_bot_db.history_1000

music_200 = trivia_bot_db.music_200
music_400 = trivia_bot_db.music_400
music_600 = trivia_bot_db.music_600
music_800 = trivia_bot_db.music_800
music_1000 = trivia_bot_db.music_1000

food_drink_200 = trivia_bot_db.food_drink_200
food_drink_400 = trivia_bot_db.food_drink_400
food_drink_600 = trivia_bot_db.food_drink_600
food_drink_800 = trivia_bot_db.food_drink_800
food_drink_1000 = trivia_bot_db.food_drink_1000

server_sessions = trivia_bot_db.server_sessions

# random question from 200 by category
def random_question_200(category):
  if category == "Science":
    return science_200.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Movies & TV":
    return movies_tv_200.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Pop Culture":
    return pop_culture_200.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "History":
    return history_200.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Music":
    return music_200.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Food & Drink":
    return food_drink_200.aggregate([{"$sample": {"size": 1}}]).next()
  else:
    return "Incorrect category. No questions!"

def random_question_400(category):
  if category == "Science":
    return science_400.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Movies & TV":
    return movies_tv_400.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Pop Culture":
    return pop_culture_400.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "History":
    return history_400.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Music":
    return music_400.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Food & Drink":
    return food_drink_400.aggregate([{"$sample": {"size": 1}}]).next()
  else:
    return "Incorrect category. No questions!"

def random_question_600(category):
  if category == "Science":
    return science_600.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Movies & TV":
    return movies_tv_600.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Pop Culture":
    return pop_culture_600.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "History":
    return history_600.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Music":
    return music_600.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Food & Drink":
    return food_drink_600.aggregate([{"$sample": {"size": 1}}]).next()
  else:
    return "Incorrect category. No questions!"

def random_question_800(category):
  if category == "Science":
    return science_800.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Movies & TV":
    return movies_tv_800.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Pop Culture":
    return pop_culture_800.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "History":
    return history_800.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Music":
    return music_800.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Food & Drink":
    return food_drink_800.aggregate([{"$sample": {"size": 1}}]).next()
  else:
    return "Incorrect category. No questions!"

def random_question_1000(category):
  if category == "Science":
    return science_1000.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Movies & TV":
    return movies_tv_1000.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Pop Culture":
    return pop_culture_1000.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "History":
    return history_1000.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Music":
    return music_1000.aggregate([{"$sample": {"size": 1}}]).next()
  elif category == "Food & Drink":
    return food_drink_1000.aggregate([{"$sample": {"size": 1}}]).next()
  else:
    return "Incorrect category. No questions!"

def format_answer(answer):
  answer = answer.replace("<i>", "")
  answer = answer.replace("&", "and")
  answer = answer.replace("</i>", "").lower().strip('"')
  answer = unidecode.unidecode(answer)
  # answer = re.sub('[^A-Za-z0-9\']+', ' ', answer)
  return answer
  
def simplify_question_object(question):
  simple_question_object = {}
  simple_question_object["question"] = question["question"]
  simple_question_object["answer"] = format_answer(question["answer"])
  simple_question_object["value"] = question["value"]
  return simple_question_object

def generate_questions_for_game(): #TODO fix
  categories = ["Science", "Pop Culture", "Movies & TV", "Music", "Food & Drink", "History"]
  questions = []
  for category in categories:
    category_obj = {}
    category_obj['category'] = category.lower()
    #pull out the question + answer, you don't need the other data. 
    category_obj['200'] = simplify_question_object(random_question_200(category))
    category_obj['400'] = simplify_question_object(random_question_400(category))
    category_obj['600'] = simplify_question_object(random_question_600(category))
    category_obj['800'] = simplify_question_object(random_question_800(category))
    category_obj['1000'] = simplify_question_object(random_question_1000(category))
    questions.append(category_obj)

  return questions

def get_current_game_question(query, category, value): #TODO FIX
  questions = query["current_game_questions"]
  category_obj = [q for q in questions if q["category"] == category.lower()][0]
  return category_obj[str(value)]

# insert new session into db
def insert_new_server_channel_session(session_obj):
  server_sessions.insert_one(session_obj)
  print(f'Inserted {session_obj["session_id"]} into Server Session DB')

def update_server_channel_session(session_obj):
  server_sessions.delete_one({"session_id": session_obj["session_id"]})
  server_sessions.insert_one(session_obj)
  print(f'Updated {session_obj["session_id"]} into Server Session DB')

def get_server_channel_session(server_id, channel_id):
  session_id = str(server_id) + "#" + str(channel_id)
  query = server_sessions.find_one({"session_id": session_id})
  return query

# already done, use it as a reference
def insert_science_questions(question):
  value = question['value']
  question_text = question['question']
  if value == 200:
    if science_200.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      science_200.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Science 200.")
  elif value == 400:
    if science_400.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      science_400.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Science 400.")
  elif value == 600:
    if science_600.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      science_600.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Science 600.")
  elif value == 800:
    if science_800.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      science_800.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Science 800.")
  elif value == 1000:
    if science_1000.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      science_1000.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Science 1000.")
  else:
    print("Error occured.")

  return

def insert_movies_tv_questions(question):
  value = question['value']
  question_text = question['question']
  if value == 200:
    if movies_tv_200.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      movies_tv_200.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Movies & TV 200.")
  elif value == 400:
    if movies_tv_400.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      movies_tv_400.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Movies & TV 400.")
  elif value == 600:
    if movies_tv_600.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      movies_tv_600.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Movies & TV 600.")
  elif value == 800:
    if movies_tv_800.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      movies_tv_800.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Movies & TV 800.")
  elif value == 1000:
    if movies_tv_1000.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      movies_tv_1000.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Movies & TV 1000.")
  else:
    print("Error occured.")

  return

def insert_pop_culture_questions(question):
  value = question['value']
  question_text = question['question']
  if value == 200:
    if pop_culture_200.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      pop_culture_200.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Pop Culture 200.")
  elif value == 400:
    if pop_culture_400.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      pop_culture_400.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Pop Culture 400.")
  elif value == 600:
    if pop_culture_600.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      pop_culture_600.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Pop Culture 600.")
  elif value == 800:
    if pop_culture_800.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      pop_culture_800.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Pop Culture 800.")
  elif value == 1000:
    if pop_culture_1000.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      pop_culture_1000.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Pop Culture 1000.")
  else:
    print("Error occured.")

  return

def insert_history_questions(question):
  value = question['value']
  question_text = question['question']
  if value == 200:
    if history_200.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      history_200.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into History 200.")
  elif value == 400:
    if history_400.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      history_400.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into History 400.")
  elif value == 600:
    if history_600.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      history_600.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into History 600.")
  elif value == 800:
    if history_800.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      history_800.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into History 800.")
  elif value == 1000:
    if history_1000.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      history_1000.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into History 1000.")
  else:
    print("Error occured.")

  return

def insert_music_questions(question):
  value = question['value']
  question_text = question['question']
  if value == 200:
    if music_200.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      music_200.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Music 200.")
  elif value == 400:
    if music_400.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      music_400.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Music 400.")
  elif value == 600:
    if music_600.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      music_600.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Music 600.")
  elif value == 800:
    if music_800.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      music_800.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Music 800.")
  elif value == 1000:
    if music_1000.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      music_1000.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Music 1000.")
  else:
    print("Error occured.")

  return

def insert_food_drink_questions(question):
  value = question['value']
  question_text = question['question']
  if value == 200:
    if food_drink_200.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      food_drink_200.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Food & Drink 200.")
  elif value == 400:
    if food_drink_400.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      food_drink_400.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Food & Drink 400.")
  elif value == 600:
    if food_drink_600.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      food_drink_600.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Food & Drink 600.")
  elif value == 800:
    if food_drink_800.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      food_drink_800.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Food & Drink 800.")
  elif value == 1000:
    if food_drink_1000.find_one({"question": question_text}) != None:
      print("Duplicate detected, not inserting.")
    else:
      food_drink_1000.insert_one(question)
      print("Inserted Question: " + f'{question}' + " into Food & Drink 1000.")
  else:
    print("Error occured.")

  return
