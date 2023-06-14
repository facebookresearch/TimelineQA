# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


import sys, getopt
import random
import numpy as np
from pprint import pprint
import json, csv
import pandas as pd

from persona_generator import generate_persona, FEMALE_NAMES_DB, MALE_NAMES_DB, PETS_NAMES_DB, HOBBIES_DB, EXERCISE_DB, EXERCISE_DB, EXCUR_ACTIVITIES, profession_dict, location_dict
from episodeGenerator import *

import settings

#generates and adds an episode of type episode according to persona into db
def addEpisode(db, persona, episode):
    #lifetime episodes: birth, move, marriage
    if episode == "birth_info":
        generateBirthEpisode(db, persona, episode)
        if settings.verbose:
            print("Added birth episode...")
    elif episode == "relocation":
        generateMoveEpisodes(db, persona, episode)
        if settings.verbose:
            print("Added relocation episodes...")
    elif episode == "marriage":
        if persona["num_marriages"]>=1:
            for marriage_index in range(len(persona["married"])):
                generateMarriageEpisode(db, persona, episode, marriage_index)
            if settings.verbose:
                print("Added ", end="")
                print(len(persona["married"]), end="")
                print(" marriage episodes...")
    elif episode == "travel":
        #year = settings.current_age + persona["birth_year"]
        generateTripEpisodes(db, persona, episode, settings.current_year)
        if settings.verbose:
            print("Added travel episodes...")
    elif episode == "annual":
        # generates annual epsiodes in the year given by the person's current age
        generateAnnualEpisodes(db, persona)
        if settings.verbose:
            print("Added annual episodes...")
    elif episode == "monthly":
        generateMonthlyEpisodes(db, persona)
        if settings.verbose:
            print("Added monthly episodes...")
    elif episode == "weekly":
        generateWeeklyEpisodes(db, persona)
        if settings.verbose:
            print("Added weekly episodes...")
    elif episode == "daily":
        generateDailyEpisodes(db, persona)
        if settings.verbose:
            print("Added daily episodes...")

        

def main(argv):

    settings.init()

    #TODO: add path to data directory
    templatefilename = "../data/templates.json"
    #default outputfile name and seed
    outfile = "default.json"
    settings.seed = 12345
    #TODO: these should ideally be read from a file 
    settings.final_year = 2022
    #episodes begins at age 18 to the current year
    #this assumes that the personas are at least 18 years old in current_year
    settings.current_age = 18
    settings.verbose = False
    settings.template_dict = {}
    settings.model = False
    settings.category = 1

    try:
        opts, args = getopt.getopt(argv,"hvy:d:o:s:c:",["currentyear=", "directory=", "output=", "seed=", "category="])
    except getopt.GetoptError:
        print('generateDB.py -h -v -y <finalyear> -d <directory> -t <template_file> -o <outputfile> -s <seed> -c <category>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print()
            print('generateDB.py -h -y <finalyear> -d <directory> -o <outputfile> -s <seed> -c <category>')
            print()
            print('-y   final year. default is 2022')
            print('-d   directory to use for outputing files')
            print('-t   template file for generating text. defaults to "templates.json" if unspecified')
            print('-v   verbose mode if specified')
            print('-o   outputfilename. defaults to default.json')
            print('-s   seed for random number generator. defaults to 12345')
            print('-c   sparse|medium|dense daily episodes')
            sys.exit()
        elif opt == '-y':
            settings.final_year = int(arg)
        elif opt == '-v':
            settings.verbose = True
        elif opt == '-d':
            directory = arg
        elif opt == '-t':
            templatefilename = arg
        elif opt == '-m':
            model = bool(arg)
        elif opt == '-o':
            outfile = arg
        elif opt == '-s':
            settings.seed = int(arg)
        elif opt == '-c':
            if arg == 'sparse':
                settings.category = 0
            elif arg == 'medium':
                settings.category = 1
            else:
                settings.category = 2

    random.seed(settings.seed)

    #TODO: variables of settings.py should ideally go to data.py
    #read some data files
    settings.city_country_list = []
    #TODO: add path to data directory
    with open("../data/cities.csv", "r") as f:
        obj = csv.reader(f, delimiter=",")
        for row in obj:
            settings.city_country_list.append(row)

    settings.college_list = []
    with open("../data/colleges.csv", "r") as f:
        obj = csv.reader(f, delimiter=",")
        for row in obj:
            settings.college_list.append(row)

    settings.major_list = []
    with open("../data/majors.csv", "r") as f:
        obj = csv.reader(f)
        for row in obj:
            settings.major_list.append(row)
    

    # generate local db and personas
    persona = generate_persona(FEMALE_NAMES_DB, MALE_NAMES_DB, PETS_NAMES_DB, profession_dict,HOBBIES_DB, EXERCISE_DB)

    settings.current_year = settings.current_age + persona["birth_year"]


    #TODO: should place these in a file
    settings.transportation = ["air", "railway", "driving"]
    settings.transportation_prob = [0.45, 0.1, 0.45]
    settings.people_group = ["parents", "friends", "family"]
    settings.people_group_prob = [0.2, 0.3, 0.5]
    #TODO: can make cities a subset of cities in city_country_list
    settings.cities = ["New York City", "The Bay Area", "Chicago", "LA", "Ithaca", "Baltimore"]
    settings.tourist_actions = ["took a selfie", "took a group photo", "recorded some videos", "bought some souvenirs"]
    settings.tourist_actions_prob = [0.3, 0.3, 0.2, 0.2]
    settings.tourist_emotions = ["happy", "special", "impressed"]
    settings.tourist_emotions_prob = [0.35, 0.35, 0.3]
    settings.food_type = ["street food", "local food", "Japanese food", "Italian food", "Chinese food", "Indian food"]
    settings.self_care_list = ["hair cut", "massage", "physical therapy"]
    settings.pet_care_list = ["a bath", "grooming"]
    settings.medical_care_type = {"annual physical checkup":0.9, "annual dental cleaning and checkup":0.7, "annual vision checkup":0.3}
    settings.medical_care_locations = ["private clinic", "hospital", "university hospital"] 
    settings.exercise_list = ["running", "swimming", "weight lifting", "biking", "hiking", "HIIT"]
    settings.body_metric_list = ["heart_rate"]
    settings.body_metric_source_list = ["apple watch", "samsung watch", "fitbit"]
    #probabilities do not need to add up to 1
    settings.visit_a_place = 0.6    #prob of visiting a place in a city etc.
    #TODO: some of these probabilities should be coming from personas
    settings.dining_probability = 0.8
    settings.cooking_probability = 0.1
    #record daily exercise activity (sparse, medium, dense)
    settings.daily_exercise_probability = [0.2, 0.5, 0.9]
    settings.breakfast_list= ["pancakes", "oatmeal", "peanut-butter-jam", "cereals", "eggs, sausages, and bread", "toast and cheese"]
    settings.lunchdinner_list = ["sushi", "a burger", "chinese food", "indian food", "sandwich", "tacos", "pasta", "steak", "fish and chips"]
    #record daily meal activities
    settings.daily_meal_probability = [0.2, 0.5, 1]
    settings.daily_chat_with_friends_probability = [[0.3], [0.5, 0.3], [1, 0.8, 0.6, 0.4]]
    settings.chat_time_list = ['in the morning', 'in the early afternoon', 'in the late afternoon', 'in the early evening', 'late in the evening', 'during lunch hours']
    settings.daily_read_probability = [0.2, 0.5, 1]
    settings.daily_read_list = ['a book', 'news', 'social media']
    settings.daily_watch_tv_probability = [0.2, 0.5, 1]
    settings.daily_watch_list = ["news", "a movie", "a tv series", "a documentary"]
    settings.weekly_bakecook_probability = [[0.2, 0.4], [0.4, 0.6], [0.7, 0.9]]
    settings.weekly_dating_probability = [[0.2, 0.4], [0.4, 0.6], [0.7, 0.9]]
    settings.weekly_hobby_probability = [[0.2, 0.4], [0.4, 0.6], [0.7, 0.9]]
    settings.weekly_grocery_shopping_probability = [[0.2, 0.4], [0.4, 0.6], [0.7, 0.9]]
    settings.fruit_list = ["apples", "oranges", "bananas", "strawberries", "blackberries", "blueberries", "raspberries", "pineapples", "pears", "apricots", "peaches", "nectarines", "cherres", "guava", "watermelons", "mandarins", "clementines", "mangos"]
    settings.drink_list = ["milk", "apple juice", "orange juice", "pineapple juice", "guava juice", "mango juice", "soda", "coffee", "tea", "mineral water", "sports drinks", "chocolate milk"]
    settings.toiletry_list = ["toilet paper", "shampoo", "conditioner", "facial wash", "paper towel", "toothpaste", "shaving cream", "toothbrush", "mouthwash", "body lotion", "mouth wash"]

    settings.eid = 0

    #schemas
    settings.marriages = pd.DataFrame(columns=['eid','married_date','partner_name','location'])
    settings.moves = pd.DataFrame(columns=['eid','date','type_of_move','destination'])
    settings.travel = pd.DataFrame(columns=['eid','start_date','end_date','city','people'])
    settings.travel_places_visited = pd.DataFrame(columns=['eid','start_date','end_date','city','place_visit_date','place','people','action','emotion'])
    settings.travel_dining = pd.DataFrame(columns=['eid','start_date','end_date','city','dining_date','food_type','food_location'])
    settings.annual_medical_care = pd.DataFrame(columns=['eid','date','for_whom','type_of_care'])
    settings.monthly_pet_care = pd.DataFrame(columns=['eid','date','pet_care_type'])
    settings.weekly_grocery = pd.DataFrame(columns=['eid','date','fruits','drinks','toiletries','people_string'])
    settings.weekly_dating = pd.DataFrame(columns=['eid','date','people_string','location'])
    settings.weekly_hobby = pd.DataFrame(columns=['eid','date','hobbies','people_string'])
    settings.weekly_bakeorcook = pd.DataFrame(columns=['eid','date','cuisine','location','people'])
    settings.daily_exercise = pd.DataFrame(columns=['eid','date','exercise','heart_rate'])
    settings.daily_read = pd.DataFrame(columns=['eid','date','readtype','howlong'])
    settings.daily_watchtv = pd.DataFrame(columns=['eid','date','watchtype','howlong'])
    settings.daily_meal = pd.DataFrame(columns=['eid','date','mealtype','foodtype','people_string'])
    settings.daily_chat = pd.DataFrame(columns=['eid','date','timeofday','howlong','friends'])

    #initialize episodicDB
    episodicDB = {}

    #read template file
    with open(templatefilename, "r") as f:
        settings.template_dict = json.load(f)

    #add lifetime episodes (birth, moving, marriage)
    addEpisode(episodicDB, persona, "birth_info")
    addEpisode(episodicDB, persona, "relocation")
    addEpisode(episodicDB, persona, "marriage")

    #current age starts at 18 by default
    #add travel, annual, daily, weekly, monthly episodes
    while settings.current_year <= settings.final_year:
        addEpisode(episodicDB, persona, "travel")
        addEpisode(episodicDB, persona, "annual")
        addEpisode(episodicDB, persona, "monthly")
        addEpisode(episodicDB, persona, "weekly")
        addEpisode(episodicDB, persona, "daily")
        settings.current_age = settings.current_age + 1
        settings.current_year = settings.current_year + 1

    if settings.verbose:
        print("Episodic DB:")
        pprint(episodicDB)

    with open(directory+"/"+outfile, 'w') as f:
        json.dump(episodicDB, f)

    #store episodes into structured tables. not needed but useful for computing ground truth for QA experiments
    pd.set_option('display.max_columns', None)
    settings.marriages.to_csv(directory+"/marriages-log.csv", index=False)
    settings.moves.to_csv(directory+"/moves-log.csv", index=False)
    settings.travel.to_csv(directory+"/travel-log.csv", index=False)
    settings.travel_places_visited.to_csv(directory+"/travel_places_visited-log.csv", index=False)
    settings.travel_dining.to_csv(directory+"/travel_dining-log.csv", index=False)
    settings.annual_medical_care.to_csv(directory+"/annual_medical_care-log.csv", index=False)
    settings.monthly_pet_care.to_csv(directory+"/monthly_pet_care-log.csv", index=False)
    settings.weekly_grocery.to_csv(directory+"/weekly_grocery-log.csv", index=False)
    settings.weekly_dating.to_csv(directory+"/weekly_dating-log.csv", index=False)
    settings.weekly_hobby.to_csv(directory+"/weekly_hobby-log.csv", index=False)
    settings.weekly_bakeorcook.to_csv(directory+"/weekly_bakeorcook-log.csv", index=False)
    settings.daily_exercise.to_csv(directory+"/daily_exercise-log.csv", index=False)
    settings.daily_read.to_csv(directory+"/daily_read-log.csv", index=False)
    settings.daily_watchtv.to_csv(directory+"/daily_watchtv-log.csv", index=False)
    settings.daily_meal.to_csv(directory+"/daily_meal-log.csv", index=False)
    settings.daily_chat.to_csv(directory+"/daily_chat-log.csv", index=False)

    with open(directory+"/persona.json", "w") as outfile:
        json.dump(persona, outfile)

if __name__ == "__main__":
   main(sys.argv[1:])
