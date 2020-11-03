import pymongo
from pymongo import MongoClient

client = MongoClient()

trivia_bot_db = client.trivia_bot_db

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

# already done, use it as a reference
def insert_science_questions(question):
  value = question['value']
  if value == 200:
    science_200.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Science 200.")
  elif value == 400:
    science_400.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Science 400.")
  elif value == 600:
    science_600.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Science 600.")
  elif value == 800:
    science_800.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Science 800.")
  elif value == 1000:
    science_1000.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Science 1000.")
  else:
    print("Error occured.")

  return

def insert_movies_tv_questions(question):
  value = question['value']
  if value == 200:
    movies_tv_200.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Movies & TV 200.")
  elif value == 400:
    movies_tv_400.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Movies & TV 400.")
  elif value == 600:
    movies_tv_600.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Movies & TV 600.")
  elif value == 800:
    movies_tv_800.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Movies & TV 800.")
  elif value == 1000:
    movies_tv_1000.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Movies & TV 1000.")
  else:
    print("Error occured.")

  return

def insert_pop_culture_questions(question):
  value = question['value']
  if value == 200:
    pop_culture_200.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Pop Culture 200.")
  elif value == 400:
    pop_culture_400.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Pop Culture 400.")
  elif value == 600:
    pop_culture_600.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Pop Culture 600.")
  elif value == 800:
    pop_culture_800.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Pop Culture 800.")
  elif value == 1000:
    pop_culture_1000.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Pop Culture 1000.")
  else:
    print("Error occured.")

  return

def insert_history_questions(question):
  value = question['value']
  if value == 200:
    history_200.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into History 200.")
  elif value == 400:
    history_400.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into History 400.")
  elif value == 600:
    history_600.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into History 600.")
  elif value == 800:
    history_800.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into History 800.")
  elif value == 1000:
    history_1000.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into History 1000.")
  else:
    print("Error occured.")

  return

def insert_music_questions(question):
  value = question['value']
  if value == 200:
    music_200.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Music 200.")
  elif value == 400:
    music_400.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Music 400.")
  elif value == 600:
    music_600.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Music 600.")
  elif value == 800:
    music_800.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Music 800.")
  elif value == 1000:
    music_1000.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Music 1000.")
  else:
    print("Error occured.")

  return

def insert_food_drink_questions(question):
  value = question['value']
  if value == 200:
    food_drink_200.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Food & Drink 200.")
  elif value == 400:
    food_drink_400.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Food & Drink 400.")
  elif value == 600:
    food_drink_600.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Food & Drink 600.")
  elif value == 800:
    food_drink_800.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Food & Drink 800.")
  elif value == 1000:
    food_drink_1000.insert_one(question)
    print("Inserted question id " + str(question['id']) + " into Food & Drink 1000.")
  else:
    print("Error occured.")

  return