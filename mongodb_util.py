import pymongo
from pymongo import MongoClient

client = MongoClient()

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
  
def simplify_question_object(question):
  simple_question_object = {}
  simple_question_object["question"] = question["question"]
  simple_question_object["answer"] = question["answer"]
  simple_question_object["value"] = question["value"]
  return simple_question_object

def generate_questions_for_game():
  categories = ["Science", "Pop Culture", "Movies & TV", "Music", "Food & Drink", "History"]
  questions = []
  for category in categories:
    category_obj = {}
    category_obj['category'] = category
    #pull out the question + answer, you don't need the other data. 
    category_obj['200'] = simplify_question_object(random_question_200(category))
    category_obj['400'] = simplify_question_object(random_question_400(category))
    category_obj['600'] = simplify_question_object(random_question_600(category))
    category_obj['800'] = simplify_question_object(random_question_800(category))
    category_obj['1000'] = simplify_question_object(random_question_1000(category))
    questions.append(category_obj)
  
  # clear current game db
  current_game.delete_many({})

  for questions_by_category in questions:
    current_game.insert_one(questions_by_category)
    print("Inserted category: " + questions_by_category['category'] + " into Current Game DB. ")

  return questions

def get_current_game_question(category, value):
  category_obj = current_game.find_one({"category": category})
  return category_obj[str(value)]


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



# print("Science 200: " + str(random_question_200("Science")))
# print("Movies & TV 200: " + str(random_question_200("Movies & TV")))
# print("Pop Culture 200: " + str(random_question_200("Pop Culture")))
# print("History 200: " + str(random_question_200("History")))
# print("Music 200: " + str(random_question_200("Music")))
# print("Food & Drink 200: " + str(random_question_200("Food & Drink")))

# print("Science 400: " + str(random_question_400("Science")))
# print("Movies & TV 400: " + str(random_question_400("Movies & TV")))
# print("Pop Culture 400: " + str(random_question_400("Pop Culture")))
# print("History 400: " + str(random_question_400("History")))
# print("Music 400: " + str(random_question_400("Music")))
# print("Food & Drink 400: " + str(random_question_400("Food & Drink")))

# print("Science 600: " + str(random_question_600("Science")))
# print("Movies & TV 600: " + str(random_question_600("Movies & TV")))
# print("Pop Culture 600: " + str(random_question_600("Pop Culture")))
# print("History 600: " + str(random_question_600("History")))
# print("Music 600: " + str(random_question_600("Music")))
# print("Food & Drink 600: " + str(random_question_600("Food & Drink")))

# print("Science 800: " + str(random_question_800("Science")))
# print("Movies & TV 800: " + str(random_question_800("Movies & TV")))
# print("Pop Culture 800: " + str(random_question_800("Pop Culture")))
# print("History 800: " + str(random_question_800("History")))
# print("Music 800: " + str(random_question_800("Music")))
# print("Food & Drink 800: " + str(random_question_800("Food & Drink")))

# print("Science 1000: " + str(random_question_1000("Science")))
# print("Movies & TV 1000: " + str(random_question_1000("Movies & TV")))
# print("Pop Culture 1000: " + str(random_question_1000("Pop Culture")))
# print("History 1000: " + str(random_question_1000("History")))
# print("Music 1000: " + str(random_question_1000("Music")))
# print("Food & Drink 1000: " + str(random_question_1000("Food & Drink")))