# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


#import numpy as np
import pandas as pd
import random
import datetime
import math

from random import randrange
from data import *
import settings

#TODO: remove hardcoded facts from persona. add more variety

# loading json
# generate a name for the college the person went to TODO
def generate_college(p):
    return random.choice(settings.college_list)

# generate a name for the graduate school  the person went to TODO
def generate_graduate_school(p):
    return random.choice(settings.college_list)

# generate a major for the college the person went to TODO
def generate_college_major(p):
    return random.choice(settings.major_list)

# generate a major for the graduate school the person went to TODO
def generate_graduate_school_major(p):
    return random.choice(settings.major_list)


# generate a country and city that one person lives in:
def generate_city_country_birth(p):
    return random.choice(settings.city_country_list)

#draw a value from a probability distribution
def flip(values, probs):
    return random.choices(values, weights = probs, k = 1)[0]

# given a year generate a date from there
def yearly_month_date_generator(start_year):
    start_year = datetime.datetime(start_year, 1, 1)
    delta = random.randint(0, 365)
    choice_date = start_year + datetime.timedelta(days=delta)
    choice_date = choice_date.strftime("%Y/%m/%d")

    return choice_date

def generate_persona(FEMALE_NAMES_DB, MALE_NAMES_DB, PETS_NAMES_DB, profession_dict, HOBBIES_DB, EXERCISE_DB):

    persona = {}
	#Determine date of birth and age
    persona["age_years"] = random.randrange(18, 75)
    persona["birth_year"] = 2022 - persona["age_years"]
    persona["birth_month"] = random.randrange(1, 12)
    persona["birth_day"] = random.randrange(1, 28)


# refining birth location --> do we need to do this as the probability of 
    persona["birth_city"], persona["birth_country"]=  generate_city_country_birth(p=1)

# sibling informaiton
    persona["num_sibling"] =  flip([0,1,2,3,4,5], [0.1, 0.3, 0.3, 0.1, 0.1, 0.1])
    persona["sibling_names"] = []
    for num in range(persona["num_sibling"]):
        gender = random.randrange(0, 51)
        if gender >= 26:
            persona["sibling_names"].append(random.choice(FEMALE_NAMES_DB))
        else:
            persona["sibling_names"].append(random.choice(MALE_NAMES_DB))
        
    
# refine parents' names
    persona["biological_mom_name"] = random.choice(FEMALE_NAMES_DB)
    persona["biological_dad_name"] = random.choice(MALE_NAMES_DB)

#Determine gender
    gender = random.randrange(0, 51)
    if gender >= 26:
        persona["gender"] = "female"
    else:
        persona["gender"] = "male"


#Graduating from K, elementary school, middle school, high school, college,
# You graduate from K at either age 5 or 6, take either 5 or 6 years in elementary school, 3 years in middle school and 3-5 years in high school.

    values = [5,6]
    probs = [0.5,  0.5]
    persona["k_graduation"] =  flip([5,6], [0.5,  0.5]) + persona["birth_year"]

    persona["e_graduation"] = persona["k_graduation"] + flip([5,6,7], [0.1, 0.8, 0.1])
    persona["m_graduation"] = persona["e_graduation"] + 3
    persona["h_graduation"] = persona["m_graduation"] + flip([3,4,5], [0.1, 0.8, 0.1])

#College, yes or no
    persona["college"] = flip([1,0], [0.5,  0.5])
    persona["graduate_school"] = 0
    if persona["college"] == 1:
        persona["college_graduation"] = persona["h_graduation"] + flip([3,4,5], [0.1, 0.8, 0.1])
        # college location
        persona["college_location"] = generate_college(persona)
        persona["college_major"] = generate_college_major(persona)
        # print("here")
        persona["graduate_school"] = flip([1,0], [0.2,  0.8])
        if persona["graduate_school"] == 1:
            persona["graduate_school_graduation"] = persona["college_graduation"] + flip([3,4,5,6,7], [0.2, 0.2, 0.4, 0.1, 0.1])
            persona["graduate_school_location"] = generate_graduate_school(persona)
            persona["graduate_school_major"] = generate_graduate_school_major(persona)

# Marriages.
# First generate the number of marriages, and then insert the appropriate years. The probability of number of marriages depends a bit on age.
    marriage_probs = [0.3, 0.4, 0.2, 0.07, 0.03]
    if  persona["age_years"] < 40:
        marriage_probs = [0.3, 0.4, 0.2, 0.1, 0.0]
    if  persona["age_years"] < 25:
         marriage_probs = [0.8, 0.2, 0.0, 0.0, 0.0]

    num_marriages = flip([0,1,2,3,4], marriage_probs)
    persona["num_marriages"] = num_marriages
    first_marriage_age = random.randrange(20, 35)
    current_age = first_marriage_age
    persona["married"] = []
    persona["divorced"] = []
    for marriage in range(0, num_marriages):
        if marriage in range(1,  num_marriages):
            persona["divorced"].append(current_age + length)
            current_age = current_age + length + time_till_next
            
        persona["married"].append(current_age)
        length = random.randrange(2, 15)
        time_till_next = random.randrange(2, 7)
# Can't plan for the future. If your age is less than what it takes you to complete your marriages and divorces, we don't let you do it.

        if current_age + length + time_till_next > persona["age_years"]:
            break
#children
    kids_probs = [0.2, 0.2, 0.2, 0.2, 0.2]
    if  persona["age_years"] < 30:
        kids_probs = [0.3, 0.3, 0.3, 0.1, 0.0]
    if  persona["age_years"] < 25:
        kids_probs = [0.7, 0.3, 0.0, 0.0, 0.0]
    num_kids = flip([0,1,2,3,4], kids_probs)
    persona["num_kids"] = num_kids
    time_between_kids_probs = [0.25, 0.20, 0.15, 0.20, 0.1, 0.1]
    age_at_first_kid = random.randrange(20, 30)
    persona["kids"] = []
    if age_at_first_kid > persona["age_years"]:
        age_at_first_kid = persona["age_years"]
    curr_age = age_at_first_kid
    for kid in range(num_kids):
        persona["kids"].append(curr_age)
        curr_age = curr_age + flip([1,2,3,4,5,6], time_between_kids_probs)
        if curr_age > persona["age_years"]:
            break

#jobs
    jobs_probs = [0.2, 0.4, 0.2, 0.1, 0.1]
    if  persona["age_years"] < 40:
        jobs_probs = [0.05, 0.3, 0.3, 0.2, 0.15]
    if  persona["age_years"] < 25:
        jobs_probs = [0.4, 0.3, 0.2, 0.1, 0.0]

    num_jobs = flip([0,1,2,3,4], jobs_probs)
    persona["num_jobs"] = num_jobs
    first_job_age = random.randrange(20, 25)
    current_age = first_job_age
    persona["started_job"] = []
    persona["quit_job"] = []
    for job in range(0, num_jobs):

        if job in range(1,  num_jobs):
            persona["quit_job"].append(current_age + length)
            current_age = current_age + length + time_till_next
            
        persona["started_job"].append(current_age)
        length = random.randrange(2, 15)
        time_till_next = random.randrange(0, 2)
# Can't plan for the future. If your age is less than what it takes you to complete your job transitions, we don't let you do it.
        if current_age + length + time_till_next > persona["age_years"]:
            break
            
# professions: --> correpsonding to started job year
# professions: matching a person's history
    persona["num_professions"] = len(persona["started_job"])
    persona["professions"] = []
    if persona["college"]:
        probs_major = [0.8, 0.2] # prob = 0.8 follow the dictionary, prob=0.2 doesn't follow
        major_key = flip([persona["college_major"], "Others"],  probs_major)[0]
        #the following if statement is a hack as the list of all majors is not in profession_dict right now
        if major_key not in profession_dict:
            major_key = 'Astrophysics'
        persona["professions"].append(random.choice(profession_dict[major_key]))
    else:
        major_key = "Others"
        persona["professions"].append(random.choice(profession_dict[major_key]))
    
    
    
# exercise, hobbies, verboseness, travel
    num_hobbies = random.randrange(2, 8)
    persona["hobbies"] = random.sample(HOBBIES_DB, num_hobbies)	
    
    num_exercise = random.randrange(1, 5)
    persona["exercise"] = random.sample(EXERCISE_DB, num_hobbies)	

    # This is the number of trips the person takes per year. It includes local, regional and international trips
    persona["trips_per_year"] = random.randrange(1, 4)

    # This is the expected number of daily or weekly events that the person is likely to record in their DB. 
    persona["verboseness"] = random.randrange(1, 10)

    # generate the name of kids, normally you name your kids with different names
    temp_db_male = MALE_NAMES_DB
    temp_db_female = FEMALE_NAMES_DB
    persona["kids_names"] = []
    if persona["num_kids"]>=1:
        for kid in range(persona["num_kids"]):
            # decide gender of a child
            if random.randrange(0, 51) <= 25:
                temp_name = random.choice(temp_db_female)
                persona["kids_names"].append(temp_name)
                temp_db_female.remove(temp_name)
            else:
                temp_name = random.choice(temp_db_male)
                persona["kids_names"].append(temp_name)
                temp_db_male.remove(temp_name)

    # generate the name of partner, consider the diversity
    persona["partners_names"] = []
    # name your partners
    if persona['num_marriages']>=1:
        for partner in range(persona['num_marriages']):
            if persona["gender"] == "male":
                partner_probs = [0.9, 0.1]
            else:
                partner_probs = [0.1, 0.9]
            gender_probability = flip(["female", "male"], partner_probs)
            if gender_probability == "female":
                persona["partners_names"].append(random.choice(temp_db_female))
            else:
                persona["partners_names"].append(random.choice(temp_db_male))
                
# remove partners' names from db -- in general you don't name your kids the same name as your past or current partner                
    
    # name friends
    persona["num_close_friends"] = random.randrange(7, 15)
    persona["close_friends_names"] = []
    for friends in range(persona["num_close_friends"]):
        if random.randrange(0, 51) <= 25:
            persona["close_friends_names"].append(random.choice(FEMALE_NAMES_DB))
        else:
            persona["close_friends_names"].append(random.choice(FEMALE_NAMES_DB))
            
    # generate pets and their names, avoid 
    temp_pets_db = PETS_NAMES_DB
    persona["num_pets"] = random.randrange(0, 3)
    persona["pet_year"] = []
    persona["pet_names"] = []
    if persona["num_pets"]>=1:
        for pet in range( persona["num_pets"]):
            persona["pet_year"].append(random.randrange(1, persona["age_years"]))
            temp_pet_name = random.choice(temp_pets_db)
            persona["pet_names"].append(temp_pet_name)
            temp_pets_db.remove(temp_pet_name)

    # persona deciding whether a person records his/her body metric or not
    persona["body_metric"] = False
    threshold = random.randrange(0, 51)
    # 10% of human beings will be recording their body metrics
    if threshold <= 50:
        persona["body_metric"] = True

    # deciding the amount of social activities
    persona["personality"] = ""
    if random.randrange(0, 51) <= 25:
        persona["personality"]="introverted"
    else:
        persona["personality"] = "extroverted"

    #print(persona)
    return (persona)


#generate_persona(FEMALE_NAMES_DB, MALE_NAMES_DB, PETS_NAMES_DB, profession_dict, HOBBIES_DB, EXERCISE_DB)

#if _name_ == "_main_":  
#   main(sys.argv[1:])
