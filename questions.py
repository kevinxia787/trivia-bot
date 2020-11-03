import requests
from mongodb_util import insert_science_questions
from mongodb_util import insert_movies_tv_questions
from mongodb_util import insert_pop_culture_questions
from mongodb_util import insert_history_questions
from mongodb_util import insert_music_questions
from mongodb_util import insert_food_drink_questions

# base_url_200 = "https://jservice.io/api/clues?value=200&category="
# base_url_400 = "https://jservice.io/api/clues?value=400&category="
# base_url_600 = "https://jservice.io/api/clues?value=600&category="
# base_url_800 = "https://jservice.io/api/clues?value=800&category="
# base_url_1000 = "https://jservice.io/api/clues?value=1000&category="

base_urls = ["https://jservice.io/api/clues?value=200&category=", "https://jservice.io/api/clues?value=400&category=", "https://jservice.io/api/clues?value=600&category=", "https://jservice.io/api/clues?value=800&category=", "https://jservice.io/api/clues?value=1000&category="]

# pulling the science category - combo of science(25), science & nature(218), general science (1087), physical science(579), science & tech (950)
def pull_science_questions():
  science_ids = [25, 218, 1087, 579, 950]

  # duplicate checker, put clue ids here
  science_question_ids = []

  urls = [[base_url + str(sid) for sid in science_ids] for base_url in base_urls] # create all of the urls i need to call

  for list_url in urls:
    for url in list_url:
      response = requests.get(url)

      # grab json
      questions = response.json()
      for q in questions:
        q_id = q['id']
        if q_id in science_question_ids:
          continue
        else:
          science_question_ids.append(q_id)
          # print(q)
          insert_science_questions(q)

  print("Inserted science questions into DB.")

def pull_movie_tv_questions():
  movie_tv_ids = [309, 67]

  # duplicate checker, put clue ids here
  movie_tv_question_ids = []
  movie_tv_category = []

  urls = [[base_url + str(sid) for sid in movie_tv_ids] for base_url in base_urls] # create all of the urls i need to call

  for list_url in urls:
    for url in list_url:
      response = requests.get(url)

      # grab json
      questions = response.json()
      for q in questions:
        q_id = q['id']
        if q_id in movie_tv_question_ids:
          continue
        else:
          movie_tv_question_ids.append(q_id)
          # print(q)
          insert_movies_tv_questions(q)

def pull_pop_culture_sports_questions():
  pop_culture_ids = [42, 1827, 622]

  pop_culture_question_ids = []

  urls = [[base_url + str(sid) for sid in pop_culture_ids] for base_url in base_urls] # create all of the urls i need to call

  for list_url in urls:
    for url in list_url:
      response = requests.get(url)

      # grab json
      questions = response.json()
      for q in questions:
        q_id = q['id']
        if q_id in pop_culture_question_ids:
          continue
        else:
          pop_culture_question_ids.append(q_id)
          # print(q)
          insert_pop_culture_questions(q)

def pull_history_questions():
  history_ids = [780, 114, 530, 50, 809, 7740]

  history_question_ids = []
  urls = [[base_url + str(sid) for sid in history_ids] for base_url in base_urls]

  for list_url in urls:
    for url in list_url:
      response = requests.get(url)

      # grab json
      questions = response.json()
      for q in questions:
        q_id = q['id']
        if q_id in history_question_ids:
          continue
        else:
          history_question_ids.append(q_id)
          # print(q)
          insert_history_questions(q)

def pull_music_questions():
  music_ids = [770, 65, 1371, 2919, 315, 184]

  music_question_ids = []
  urls = [[base_url + str(sid) for sid in music_ids] for base_url in base_urls]

  for list_url in urls:
    for url in list_url:
      response = requests.get(url)

      # grab json
      questions = response.json()
      for q in questions:
        q_id = q['id']
        if q_id in music_question_ids:
          continue
        else:
          music_question_ids.append(q_id)
          #print(q)
          insert_music_questions(q)

def pull_food_drink_questions():
  food_drink_ids = [49, 253, 777]

  food_drink_question_ids = []
  urls = [[base_url + str(sid) for sid in food_drink_ids] for base_url in base_urls]

  for list_url in urls:
    for url in list_url:
      response = requests.get(url)

      # grab json
      questions = response.json()
      for q in questions:
        q_id = q['id']
        if q_id in food_drink_question_ids:
          continue
        else:
          food_drink_ids.append(q_id)
          # print(q)
          insert_food_drink_questions(q)

