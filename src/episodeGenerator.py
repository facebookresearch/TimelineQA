from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import random
import math
import pandas as pd

from persona_generator import flip, yearly_month_date_generator, location_dict
from episodicDBUtils import *
from data import *
import settings
import re

def get_count(db, date_str, episode):
    count = 0
    if date_str in db:
        related_episodes = [k for k in db[date_str] if episode in k]
        count = len(related_episodes)
    return str(count)

def generate_model_based_text(temp_logical_rep, episode_key, prompt, all_episodes_schema):
    content = ""
    for item_index in range(len(temp_logical_rep)):
        if "date" not in all_episodes_schema[episode_key][item_index]:  # skip temporal information
            content += all_episodes_schema[episode_key][item_index]
            content += ": "
            if all_episodes_schema[episode_key][item_index] == "people":
                content += "Myself, "     
            if type(temp_logical_rep[item_index]) == list:
                temp = ",".join(temp_logical_rep[item_index])
                content += temp
            else:                                                    
                content += temp_logical_rep[item_index] 
            content += " "                                                  
    episodic_representation = f"{prompt}  {content}"
    model_output_text = generate_text_prompt(episodic_representation)                   
        
    return [model_output_text[0].replace("\n", "")]

def generateOneTrip(db, episode, destination, start_date, duration, people):
    if start_date.year > settings.current_year:
        return
    end_date = start_date + datetime.timedelta(days=duration)
    trip_start_date = start_date.strftime("%Y/%m/%d")
    trip_end_date = end_date.strftime("%Y/%m/%d")

    people_str = ""
    idx_str = ""
    if len(people) == 0:
        people = ["myself"]
        people_str = "myself"
        idx_str = "alone"
    else:
        people_str = ", ".join(people)
        idx_str = "with_company"

    # put things altogether into logical representations
    temp_logical_rep = [trip_start_date, trip_end_date, people, destination]
    format_dict = {"destination":destination, "people_str": people_str, "duration":duration, "trip_start_date":trip_start_date}

    templates = settings.template_dict[episode][idx_str]["templates"]
    num = str(getATemplate(templates))
    #check if template uses all the variables.
    #erase variables (except for date) which are not used
    not_used = format_dict.keys() - set(re.findall(r'{(.+?)}', templates[num]["txt"]))
    for v in not_used:
        if 'date' not in v:
            format_dict[v] = ''
    #record in travel dataframe, key is (start date, end date, city)
    df_dict = pd.DataFrame([{'eid':'e'+str(settings.eid), 'start_date':format_dict['trip_start_date'], 'end_date':trip_end_date, 'city':format_dict['destination'], 'people':format_dict['people_str']}])
    settings.travel = pd.concat([df_dict, settings.travel])
    template_based = templates[num]["txt"].format(**format_dict)
    qa_list = formatQAList(templates[num]["questions"], format_dict)

    #use a language model to generate text or not. not implemented now
    if settings.model:  
        content = "trip information: "
        model_output_text = generate_model_based_text(content, temp_logical_rep, episode, prompt)
    else: 
        model_output_text = []

    #initialize an empty dictionary with the various fields
    trip_dict = initDictionary()
    addEid(trip_dict, settings.eid)
    settings.eid += 1
    addLogicalRepresentation(trip_dict, temp_logical_rep)
    addTextTemplate(trip_dict, template_based)
    addTextFromModel(trip_dict, model_output_text)
    addAtomicQAPairs(trip_dict, qa_list)
    if trip_start_date not in db:
        db[trip_start_date] = {}
    count = get_count(db, trip_start_date, episode)
    db[trip_start_date][episode+count] = trip_dict

    #return this dictionary for subepisodes
    return {'start_date':start_date, 'end_date':end_date, 'city':destination}

#TODO: activities can be placed in a data file instead of putting it directly into the code
def generateDestinationsVisited(db, episode_list, destination, start_date, duration, people, key_dict):
    places_to_visit = []
    for p in travel_db[destination]['places_to_visit']:
        places_to_visit.append(p)
    temp_date = start_date
    while len(places_to_visit) > 0:
        for i in range(min(duration, len(places_to_visit))):
            if random.random() <= settings.visit_a_place and len(places_to_visit) > 0:
                temp_date = temp_date + datetime.timedelta(days=1)
                temp_date_str = temp_date.strftime("%Y/%m/%d")
                tourist_action = flip(settings.tourist_actions, settings.tourist_actions_prob)
                emotion = flip(settings.tourist_emotions, settings.tourist_emotions_prob)
                temp_location = random.choice(places_to_visit)
                places_to_visit.remove(temp_location)

                temp_logical_rep = [temp_date_str, people, temp_location, tourist_action, emotion]
                shorten_date = temp_date.strftime("%Y/%m")
                people_str = ", ".join(people)
                alone_str = ""
                if len(people) == 0:
                    alone_str = "alone"
                else:
                    alone_str = "with_company"
                format_dict = {"destination":destination, "temp_location":temp_location, "shorten_date": shorten_date, "people_str": people_str, "tourist_action":tourist_action, "temp_date_str":temp_date_str, "emotion":emotion}
                #record in travel_places_visited dataframe
                key_dict['place_visit_date'] = temp_date_str
                key_dict['place']=temp_location
                key_dict['people']=people_str
                key_dict['action']=tourist_action
                key_dict['emotion']=emotion
                key_dict['eid']='e'+str(settings.eid)
                df_dict = pd.DataFrame([key_dict])
                settings.travel_places_visited = pd.concat([settings.travel_places_visited,df_dict])

                templates = settings.template_dict[episode_list[0]][episode_list[1]][alone_str]["templates"]
                num = str(getATemplate(templates))
                #check if template uses all the variables.
                #erase variables (except for date) which are not used
                not_used = format_dict.keys() - set(re.findall(r'{(.+?)}', templates[num]["txt"]))
                for v in not_used:
                    if 'date' not in v:
                        format_dict[v] = ''
                template_based = templates[num]["txt"].format(**format_dict)
                qa_list = formatQAList(templates[num]["questions"], format_dict)

                #TODO
                if settings.model:  
                    content = "places that visited for the trip: "
                    model_output_text = generate_model_based_text(content, temp_logical_rep, "visiting_places", prompt)
                else:  
                    model_output_text = []

                if temp_date_str not in db:
                    db[temp_date_str] = {}

                #initialize an empty dictionary with the various fields
                visit_dict = initDictionary()
                addEid(visit_dict, settings.eid)
                settings.eid += 1
                addLogicalRepresentation(visit_dict, temp_logical_rep)
                addTextTemplate(visit_dict, template_based)
                addTextFromModel(visit_dict, model_output_text)
                addAtomicQAPairs(visit_dict, qa_list)
                count = get_count(db, temp_date_str, episode_list[1])
                db[temp_date_str][episode_list[1]+count] = visit_dict

def generateDiningPlaces(db, episode_list, destination, start_date, duration, people, key_dict):
    restaurant_list = []
    for p in travel_db[destination]['restaurants']['dining']:
        restaurant_list.append(p)
    dining_date = start_date
    # check whether there is a restaurant reservation 
    for num in range(duration):              
        dining_date = dining_date + datetime.timedelta(days=1)            
        dining_date_str = dining_date.strftime("%Y/%m/%d")
        if random.random() <= settings.dining_probability:
            food_type = random.choice(settings.food_type)
            food_location = random.choice(restaurant_list)
            temp_logical_rep = [dining_date_str, people, food_type, food_location]
            shorten_date = dining_date.strftime("%Y/%m")
            people_str = ", ".join(people)                                      
            alone_str = ""
            if len(people) == 0:
                alone_str = "alone"
            else:
                alone_str = "with_company"
            format_dict = {"shorten_date":shorten_date, "food_type":food_type, "food_location":food_location, "people_str":people_str, "destination":destination, "date":dining_date_str}
            #record in travel_dining dataframe
            key_dict['dining_date']=dining_date_str
            key_dict['food_type']=food_type
            key_dict['food_location']=food_location
            key_dict['eid']='e'+str(settings.eid)

            templates = settings.template_dict[episode_list[0]][episode_list[1]][alone_str]["templates"]
            num = str(getATemplate(templates))
            #check if template uses all the variables.
            #erase variables (except for date) which are not used
            not_used = format_dict.keys() - set(re.findall(r'{(.+?)}', templates[num]["txt"]))
            for v in not_used:
                if 'date' not in v:
                    format_dict[v] = ''
            df_dict = pd.DataFrame([key_dict])
            settings.travel_dining = pd.concat([settings.travel_dining, df_dict])

            template_based = templates[num]["txt"].format(**format_dict)
            qa_list = formatQAList(templates[num]["questions"], format_dict)
                
            model_output_text = ""
            #TODO
            if settings.model:  
                content = "restaurants visited during the trip: "
                model_output_text = generate_model_based_text(content, temp_logical_rep, "eating", prompt)
            else:  # no model based generated results
                model_output_text = []

            if dining_date_str not in db:
                db[dining_date_str] = {}
            #initialize an empty dictionary with the various fields
            visit_dict = initDictionary()
            addEid(visit_dict, settings.eid)
            settings.eid += 1
            addLogicalRepresentation(visit_dict, temp_logical_rep)
            addTextTemplate(visit_dict, template_based)
            addTextFromModel(visit_dict, model_output_text)
            addAtomicQAPairs(visit_dict, qa_list)
            count = get_count(db, dining_date_str, episode_list[1])
            db[dining_date_str][episode_list[1]+count] = visit_dict


def generateTripEpisodes(db, persona, episode, year):
    people_dict = get_people(persona)
    people_group = flip(settings.people_group, settings.people_group_prob)
    if len(people_dict[people_group]) == 0:
        people_dict[people_group] = ["myself"]
    people = random.sample(people_dict[people_group], random.randint(1, minimumOf(3, len(people_dict[people_group]))))

    # for tracking to avoid visiting the same city 
    city_list = list(travel_db.keys())  
    count = persona["trips_per_year"]

    # heuristic: start the trip at the beginning of the year as there may be more trips to come
    m = random.randint(1,5) 
    d = getDay()
    start_date = datetime.datetime(year, m, d)
    while count and len(city_list) > 0:
        destination = random.choice(city_list)
        # remove destination from the candidate list so as not to visit it again this year
        city_list.remove(destination)  

        #length of travel in days
        duration = random.randint(3, 15)
        key_dict = generateOneTrip(db, episode, destination, start_date, duration, people)
        if settings.verbose:
            print("Added one trip...")

        generateDestinationsVisited(db, [episode, "places_visited"], destination, start_date, duration, people, key_dict)
        if settings.verbose:
            print("---Added destinations visited...")

        #TODO: there should be consistency between the dining locations and where you are at the day of travel
        generateDiningPlaces(db, [episode, "dining"], destination, start_date, duration, people, key_dict)
        if settings.verbose:
            print("---Added dining places...")
        # shorter duration between trips if there are many trips per year
        if persona["trips_per_year"] > 2:
            gap_duration = random.randint(30, 90)
        else:
            gap_duration = random.randint(60, 120)
        start_date = start_date + datetime.timedelta(days=gap_duration)
        count = count - 1


def formatQAList(qa_dict, format_dict):
    qa_list = []
    for k in qa_dict.keys():
        qa_pair = qa_dict[k]
        qa = []
        qa.append(qa_pair[0].format(**format_dict))
        qa.append(qa_pair[1].format(**format_dict))
        qa_list.append(qa)
    return qa_list
    

def generateBirthEpisode(db, persona, episode):
    birth_date = datetime.datetime(persona["birth_year"], persona["birth_month"], persona["birth_day"]).strftime("%Y/%m/%d")
    if not (birth_date in db):
        db[birth_date] = {}

    event = "birth_info"
    location = [persona["birth_city"], persona["birth_country"]]
    parents = [persona["biological_mom_name"], persona["biological_dad_name"]]
    
    temp_logical_rep = [birth_date, parents, location]
    format_dict = {"birth_date": birth_date, "location0": location[0], "location1": location[1], "parent0":parents[0], "parent1": parents[1] }

    templates = settings.template_dict[episode]["templates"]
    num = str(getATemplate(templates))
    template_based = templates[num]['txt'].format(**format_dict)

    birth_dict = initDictionary()
    addEid(birth_dict, settings.eid)
    settings.eid += 1
    addLogicalRepresentation(birth_dict, temp_logical_rep)
    addTextTemplate(birth_dict, template_based)
    question_list = formatQAList(templates[num]['questions'], format_dict)
    addAtomicQAPairs(birth_dict, question_list)

    db[birth_date][episode] = birth_dict 
    return db

#TODO: to reconcile with getMonth method in episodicDBUtils.py
def getMonth():
    return random.randint(1, 12)

#TODO: to reconcile with getDay method in episodicDBUtils.py
def getDay():
    # does not consider 29, 30, 31
    return random.randint(1, 28)

def generateSchoolMove(db, persona, move_date, college_or_gradschool):
    move_date_obj = datetime.datetime.strptime(move_date, '%Y/%m/%d').date()
    if move_date_obj.year > settings.current_year:
        return
    if move_date not in db:
        db[move_date] = {}

    people_candidate = [persona["biological_mom_name"]] + [persona["biological_dad_name"]] + persona["sibling_names"]
    people_coming = random.randint(1, len(people_candidate))
    people = random.sample(people_candidate, people_coming)
    school_name = persona["college_location"][0]
    location = persona["college_location"][1]
    temp_logical_rep = [move_date, location, people, "relocating to attend "+school_name]
    people_str = ", ".join(people)
    transportation = flip(settings.transportation, settings.transportation_prob)

    format_dict = {"people_str": people_str, "location": location, "date": move_date, "college_or_gradschool": college_or_gradschool, "school":school_name}


    alone_str = ""
    if len(people_str) == 0:
        alone_str = "with_company"
    else:
        alone_str = "alone"

    templates = settings.template_dict["school_move"][alone_str]["templates"]
    num = str(getATemplate(templates))        

    dict1 = {'eid':'e'+str(settings.eid), 'date':move_date, 'type_of_move':college_or_gradschool, 'destination': school_name}
    df_dict = pd.DataFrame([dict1])
    settings.moves = pd.concat([settings.moves, df_dict])

    template_based = templates[num]["txt"].format(**format_dict)
    move_qas = formatQAList(templates[num]["questions"], format_dict)

    move_dict = initDictionary()
    addEid(move_dict, settings.eid)
    settings.eid += 1
    addLogicalRepresentation(move_dict, temp_logical_rep)
    addTextTemplate(move_dict, template_based)
    addAtomicQAPairs(move_dict, move_qas)
    count = get_count(db, move_date, college_or_gradschool)
    db[move_date][college_or_gradschool+count] = move_dict

    #add graduation event 
    #if college, graduate 4 years later. if grad school, graduate 5-6 years later
    graduation = ""
    complete_date_obj = ""
    if college_or_gradschool == "college move":
        complete_date_obj = move_date_obj + relativedelta(years = 4)
        graduation = "college graduation"
        if complete_date_obj.month < 6:
            #move it to june graduation
            complete_date_obj = complete_date_obj + relativedelta(months=(6-complete_date_obj.month))
            
        elif complete_date_obj.month > 10:
            #move it to next june graduation
            complete_date_obj = complete_date_obj + relativedelta(months=(12-complete_date_obj.month))
    else:
        complete_date_obj = move_date_obj + relativedelta(years = 5)
        graduation = "graduate school graduation"

    howlong = complete_date_obj - move_date_obj
    complete_date_str = complete_date_obj.strftime("%Y/%m/%d")
    howlong_str = str(howlong.days) + " days"
    format_dict = {"school": school_name, "location":location, "date": complete_date_str, "howlong":howlong_str}
    templates = settings.template_dict[graduation]["templates"]
    num = str(getATemplate(templates))
    template_based = templates[num]["txt"].format(**format_dict)
    move_qas = formatQAList(templates[num]["questions"], format_dict)
    graduate_dict = initDictionary()
    temp_logical_rep = [complete_date_str, location]
    addEid(graduate_dict, settings.eid)
    settings.eid += 1
    addLogicalRepresentation(graduate_dict, temp_logical_rep)
    addTextTemplate(graduate_dict, template_based)
    addAtomicQAPairs(graduate_dict, move_qas)
    if complete_date_str not in db:
        db[complete_date_str] = {}
    count = get_count(db, complete_date_str, graduation)
    db[complete_date_str][graduation+count] = graduate_dict

def generateJobMove(db, persona, move_date, num):
    move_date_obj = datetime.datetime.strptime(move_date, '%Y/%m/%d').date()
    if move_date_obj.year > settings.current_year:
        return
    location = random.choice(settings.cities)
    people = []
    candidate_people = []
    priority_queue=[]
    kids_queue = []

    if move_date not in db:
        db[move_date] = {}
    # bring the current partner
    if len(persona["married"])>0:
        if min(persona["married"]) <= persona["started_job"][num]:
            for married_index in range(len(persona["married"])):
                if persona["married"][married_index]<=persona["started_job"][num]:
                    priority_queue.append(persona["partners_names"][married_index])
            candidate_people.append(priority_queue[-1])
            
    # always bring the child 
    if len(persona["kids"])>0:
        if min(persona["kids"]) <= persona["started_job"][num]:
            for kids_index in range(len(persona["kids"])):
                if persona["kids"][kids_index]<=persona["started_job"][num]:
                    kids_queue.append(persona["kids_names"][ kids_index])
    people = kids_queue + candidate_people

    event_desc = f"moving to {location} for a new job"
    temp_logical_rep = [move_date, location, people, event_desc]
    people_str = ", ".join(people)
    transportation =  flip(settings.transportation, settings.transportation_prob)

    format_dict = {"event_desc": event_desc, "people_str": people_str, "location": location, "date": move_date, "transportation": transportation}

    alone_str = ""
    if len(people)>0:
        alone_str = "with_company"
    else:
        alone_str = "alone"

    templates = settings.template_dict["job_move"][alone_str]["templates"]
    num = str(getATemplate(templates))

    df_dict = pd.DataFrame([{'eid':'e'+str(settings.eid), 'date':move_date, 'type_of_move':event_desc, 'destination': location}])
    settings.moves = pd.concat([settings.moves, df_dict])

    template_based = templates[num]["txt"].format(**format_dict)
    move_qas = formatQAList(templates[num]["questions"], format_dict)

    move_dict = initDictionary()
    addEid(move_dict, settings.eid)
    settings.eid += 1
    addLogicalRepresentation(move_dict, temp_logical_rep)
    addTextTemplate(move_dict, template_based)
    addAtomicQAPairs(move_dict, move_qas)
    episode = "job_move"
    count = get_count(db, move_date, episode)
    db[move_date][episode+count] = move_dict

def generateMoveEpisodes(db, persona, episode):
    m = getMonth()
    d = getDay()
    if persona["college"]:
        if settings.verbose:
            print("Added college move episode...")
        move_date = datetime.datetime(persona["college_graduation"]-4, m, d).strftime("%Y/%m/%d")
        generateSchoolMove(db, persona, move_date, "college move")

    if persona["graduate_school"]:
        if settings.verbose:
            print("Added graduate school move episode...")
        move_date = datetime.datetime(persona["graduate_school_graduation"]-5, m, d).strftime("%Y/%m/%d")
        generateSchoolMove(db, persona, move_date, "graduate school move")

    if persona["started_job"]:
        if settings.verbose:
            print("Added job move episode...")
        for num in range(len(persona["started_job"])):
            move_date = datetime.datetime(persona["started_job"][num]+persona["birth_year"], m, d).strftime("%Y/%m/%d")
            generateJobMove(db, persona, move_date, num)


def generateMarriageEpisode(db, persona, episode, marriage_index):
    married_date = yearly_month_date_generator(persona["birth_year"] + persona["married"][marriage_index])
    married_date_obj = datetime.datetime.strptime(married_date, '%Y/%m/%d').date()
    if married_date_obj.year > settings.current_year:
        return
    if married_date not in db:
        db[married_date] = {}

    # add marriage episode
    temp_logical_rep = [[married_date, random.choice(location_dict["engagement"]), persona["partners_names"][marriage_index]]]                                                                   
    partner_name = persona["partners_names"][marriage_index]                            
    location = random.choice(location_dict["marriage"]) 
    format_dict = {"eid":'e'+str(settings.eid), "partner_name":partner_name, "married_date":married_date, "location":location}
    templates = settings.template_dict[episode]["templates"]
    num = str(getATemplate(templates))
    #check if template uses all the variables.
    #erase variables (except for date) which are not used
    not_used = format_dict.keys() - set(re.findall(r'{(.+?)}', templates[num]["txt"]))
    for v in not_used:
        if 'date' not in v:
            format_dict[v] = ''

    template_based = templates[num]["txt"].format(**format_dict)
    qa_list = templates[num]["questions"]

    marriage_dict = initDictionary()
    addEid(marriage_dict, settings.eid)
    settings.eid += 1
    addLogicalRepresentation(marriage_dict, temp_logical_rep)
    addTextTemplate(marriage_dict, template_based)
    addAtomicQAPairs(marriage_dict, qa_list)
    count = get_count(db, married_date, episode)
    db[married_date][episode+count] = marriage_dict

    df_dict = pd.DataFrame([format_dict])
    settings.marriages = pd.concat([settings.marriages, df_dict])

# check whether there is a mutually exclusive event for episode happening on the same day
# mutually exclusive items are defined in data.py
def passMutualExclusiveCheck(date_str, episode, db):
    if date_str in db:
        for item in mutual_exclusive_dict[episode]:
            if item in db[date_str]:
                return False
    return True

def generateAnnualMedicalCare(db, persona, episode, k, category, context):
    m = getMonth()
    d = getDay()
    start_date = datetime.datetime(settings.current_year, m, d)   
    if start_date.year > settings.current_year:
        return
    date_str = start_date.strftime("%Y/%m/%d")
    year_str = start_date.strftime("%Y")                     
    if passMutualExclusiveCheck(date_str, episode, db):
        location = random.choice(settings.medical_care_locations)
        format_dict = {"name": context, "purpose":k,  "date": date_str, "year":year_str, "location":location}
        df_dict = pd.DataFrame([{'eid':'e'+str(settings.eid), 'date':date_str, 'for_whom':episode, 'type_of_care':k}])
        settings.annual_medical_care = pd.concat([df_dict, settings.annual_medical_care])
        templates = settings.template_dict["medical_care"][category]["templates"]
        num = str(getATemplate(templates))
        template_based = templates[num]["txt"].format(**format_dict)
        qa_list = formatQAList(templates[num]["questions"], format_dict)
        if date_str not in db:
            db[date_str] = {}
        logical_care_rep = [date_str, template_based, location]
        care_dict = initDictionary()
        addEid(care_dict, settings.eid)
        settings.eid += 1
        addLogicalRepresentation(care_dict, logical_care_rep)
        addTextTemplate(care_dict, template_based)
        addAtomicQAPairs(care_dict, qa_list)

        count = get_count(db, date_str, episode)
        db[date_str][episode + count] = care_dict
         
def generateAnnualEpisodes(db, persona):
    #TODO: need to check that all logical rep are capturing the fields correctly

    #personal medical care
    for k in settings.medical_care_type:
        if random.random() < settings.medical_care_type[k]:
            context = ""
            generateAnnualMedicalCare(db, persona, "personal_medical_care", k, "personal", context)

    #parents
    for k in settings.medical_care_type:
        if random.random() < settings.medical_care_type[k]:
            context = "my parents for their"
            generateAnnualMedicalCare(db, persona, "parent_medical_care", k, "others", context)

    # kids annual medical care
    if persona['num_kids'] > 0:
        for idx in range(0, len(persona['kids'])):
            context = name = persona['kids_names'][idx] + " for his/her "
            if settings.current_age > persona['kids'][idx]:
                for k in settings.medical_care_type:
                    if random.random() < settings.medical_care_type[k]:
                        generateAnnualMedicalCare(db, persona, "child_medical_care", k, "others", context)


def generateMonthlyEpisodes(db, persona):
    #TODO: currently there is only petcare for monthly episodes
    #self_care is missing

    start_date = datetime.datetime(settings.current_year, 1, getDay())
    if start_date.year > settings.current_year:
        return

    count = 0               
                                
    #TODO: need to fix the logic. random pets are taken for pet care each month. 
    episode = 'pet_care'
    while count <= 12:                               
        if persona["num_pets"] > 0:
            pet_care_item = random.choice(settings.pet_care_list)
            pet_care_date_str = start_date.strftime("%Y/%m/%d")

            if passMutualExclusiveCheck(pet_care_date_str, episode, db):
                pet_care_logical_rep = [pet_care_date_str, pet_care_item]
                format_dict = {"pet_care_item":pet_care_item, "date":pet_care_date_str}
                df_dict = pd.DataFrame([{'eid':'e'+str(settings.eid), 'date':pet_care_date_str, 'pet_care_type':pet_care_item}])
                settings.monthly_pet_care = pd.concat([settings.monthly_pet_care, df_dict])
                templates = settings.template_dict["pet_care"]["templates"]
                num = str(getATemplate(templates))
                template_based = templates[num]["txt"].format(**format_dict)
                qa_list = formatQAList(templates[num]["questions"], format_dict)


                if pet_care_date_str not in db:
                    db[pet_care_date_str] = {}
                pet_care_dict = initDictionary()
                addEid(pet_care_dict, settings.eid)
                settings.eid += 1
                addLogicalRepresentation(pet_care_dict, pet_care_logical_rep)
                addTextTemplate(pet_care_dict, template_based)
                addAtomicQAPairs(pet_care_dict, qa_list)
                episode = 'pet_care'
                episode_count = get_count(db, pet_care_date_str, episode)
                db[pet_care_date_str][episode+episode_count] = pet_care_dict
        count += 1
        if count <=12:
            start_date = datetime.datetime(settings.current_year, count, getDay())


def generateBakeOrCookEpisode(db, persona, item_list, bake_or_cook, date_str):
    start_date = datetime.datetime.strptime(date_str , '%Y/%m/%d').date()
    if start_date.year > settings.current_year:
        return
    people_dict = get_people(persona)
    baked_or_cooked = ""
    baking_or_cooking = ""
    if bake_or_cook == "cook":
        baking_or_cooking = "cooking"
        baked_or_cooked = "cooked"
    else:
        baking_or_cooking = "baking"
        baked_or_cooked = "baked"
    if passMutualExclusiveCheck(date_str, bake_or_cook, db):
        if 22 <= settings.current_age <= 75 and random.random() <= 0.1:
            people_group = flip(settings.people_group, settings.people_group_prob)
            if len(people_dict[people_group]) == 0:
                people_dict[people_group] = ["myself"]
            people = random.sample(people_dict[people_group], random.randint(1,minimumOf(4, len(people_dict[people_group])))) 

            people_str = ", ".join(people)
            cooked_item_number = random.randint(1, 3)
            cooked_list = random.sample(item_list, cooked_item_number)
            cuisine_string = ", ".join(cooked_list)
            location = random.choice(["my place"])

            template_based = []

            alone_str = ""
            if people_str == "myself" or len(people) == 0:
                alone_str = "alone"
            else:
                alone_str = "with_company"

            format_dict = {"bake_or_cook":bake_or_cook, "baked_or_cooked":baked_or_cooked, "baking_or_cooking":baking_or_cooking, "date": date_str, "cuisine_string":cuisine_string, "location":location, "people_str":people_str}
            templates = settings.template_dict["cooking"][alone_str]["templates"]
            num = str(getATemplate(templates))
            #check if template uses all the variables.
            #erase variables (except for date) which are not used
            not_used = format_dict.keys() - set(re.findall(r'{(.+?)}', templates[num]["txt"]))
            for v in not_used:
                if 'date' not in v:
                    format_dict[v] = ''
            df_dict = pd.DataFrame([{'eid':'e'+str(settings.eid), 'date':date_str, 'cuisine':format_dict['cuisine_string'], 'location':format_dict['location'], 'people':format_dict['people_str']}])
            settings.weekly_bakeorcook = pd.concat([settings.weekly_bakeorcook, df_dict])

            template_based = templates[num]["txt"].format(**format_dict)
            qa_list = formatQAList(templates[num]["questions"], format_dict)

            temp_logical_cooking_rep = [date_str, template_based, bake_or_cook, cuisine_string, people_str, location]

            if date_str not in db:
                db[date_str] = {}
            cooking_dict = initDictionary()
            addEid(cooking_dict, settings.eid)
            settings.eid += 1
            addLogicalRepresentation(cooking_dict, temp_logical_cooking_rep)
            addTextTemplate(cooking_dict, template_based)
            addAtomicQAPairs(cooking_dict, qa_list)
            count = get_count(db, date_str, bake_or_cook)
            db[date_str][bake_or_cook+count] = cooking_dict

def generateDatingEpisode(db, persona, episode, date_str):
    start_date = datetime.datetime.strptime(date_str , '%Y/%m/%d').date()
    if start_date.year > settings.current_year:
        return
    threshold = 0
    if 30 >= settings.current_age >= 16:
        threshold = 0.7
    elif 60 >= settings.current_age >= 26:
        threshold = 0.5
    else:
        threshold = 0

    if random.random() < threshold:
        people_string = "date"
        priority_queue = []
        if len(persona["married"]) > 0:
            if min(persona["married"]) <= settings.current_age:
                for married_index in range(len(persona["married"])):
                    if persona["married"][married_index] <= settings.current_age:
                        priority_queue.append(persona["partners_names"][married_index])
                        people_string = priority_queue[-1]
        if people_string == "date":
            #pick a random name from FEMALE_NAMES_DB and MALE_NAMES_DB
            i = random.sample([0,1], 1)[0]
            if i == 0:
                people_string = random.sample(FEMALE_NAMES_DB, 1)[0]
            else:
                people_string = random.sample(MALE_NAMES_DB, 1)[0]

        location = random.choice(support_db['date_location_list'])

        # no mutual exclusive check for dating. one can date anytime anywhere 
        temp_dating_rep = [date_str, people_string, location]    
        format_dict = {"eid":'e'+str(settings.eid), "people_string":people_string, "date":date_str, "location":location}

        df_dict = pd.DataFrame([format_dict])
        settings.weekly_dating = pd.concat([settings.weekly_dating, df_dict])
        templates = settings.template_dict[episode]["templates"]
        num = str(getATemplate(templates))
        template_based = templates[num]["txt"].format(**format_dict)
        qa_list = formatQAList(templates[num]["questions"], format_dict)
        if date_str not in db:
            db[date_str] = {}

        dating_dict = initDictionary()
        addEid(dating_dict, settings.eid)
        settings.eid += 1
        addLogicalRepresentation(dating_dict, temp_dating_rep)
        addTextTemplate(dating_dict, template_based)
        addAtomicQAPairs(dating_dict, qa_list)
        count = get_count(db, date_str, episode)
        db[date_str][episode + count] = dating_dict

def generateHobbyEpisode(db, persona, episode, date_str):
    start_date = datetime.datetime.strptime(date_str , '%Y/%m/%d').date()
    if start_date.year > settings.current_year:
        return
    people_dict = get_people(persona)
    if passMutualExclusiveCheck(date_str, episode, db):
        if settings.current_age >= 12 and random.random()<0.5:
            people_group = flip(settings.people_group, settings.people_group_prob)
            if len(people_dict[people_group]) == 0:
                people_dict[people_group] = ["myself"]
            people = random.sample(people_dict[people_group], random.randint(1, minimumOf(3, len(people_dict[people_group]))))

            people_string = ", ".join(people)
            hobbies = random.choice(persona["hobbies"])

            format_dict = {"people_string":people_string, "hobbies":hobbies, "date":date_str}
            templates = settings.template_dict[episode]["templates"]
            num = str(getATemplate(templates))
            #check if template uses all the variables.
            #erase variables (except for date) which are not used
            not_used = format_dict.keys() - set(re.findall(r'{(.+?)}', templates[num]["txt"]))
            for v in not_used:
                if 'date' not in v:
                    format_dict[v] = ''
            format_dict['eid'] = 'e'+str(settings.eid)
            df_dict = pd.DataFrame([format_dict])
            settings.weekly_hobby = pd.concat([settings.weekly_hobby, df_dict])

            template_based = templates[num]["txt"].format(**format_dict)
            qa_list = formatQAList(templates[num]["questions"], format_dict)
            temp_logical_hobbies_rep = [date_str, template_based, hobbies, people_string]

            hobbies_dict = initDictionary()
            if date_str not in db: 
                db[date_str] = {}

            addEid(hobbies_dict, settings.eid)
            settings.eid += 1
            addLogicalRepresentation(hobbies_dict, temp_logical_hobbies_rep)
            addTextTemplate(hobbies_dict, template_based)
            addAtomicQAPairs(hobbies_dict, qa_list)
            count = get_count(db, date_str, episode)
            db[date_str][episode+count] = hobbies_dict

def generateGroceryShoppingEpisode(db, persona, episode, date_str):
    start_date = datetime.datetime.strptime(date_str , '%Y/%m/%d').date()
    if start_date.year > settings.current_year:
        return
    if passMutualExclusiveCheck(date_str, episode, db):
        people_dict = get_people(persona)
        people_group = flip(settings.people_group, settings.people_group_prob)
        if len(people_dict[people_group]) == 0:
            people_dict[people_group] = ["myself"]
        people = random.sample(people_dict[people_group], random.randint(1, len(people_dict[people_group])))
        people_string = ", ".join(people)

        fruits_l = random.sample(settings.fruit_list, random.randint(1,4))
        fruits = ", ".join(fruits_l)

        drinks_l = random.sample(settings.drink_list, random.randint(1,4))
        drinks = ", ".join(drinks_l)
        toiletries_l = random.sample(settings.toiletry_list, random.randint(1,4))
        toiletries = ", ".join(toiletries_l)

        format_dict = {"fruits":fruits, "drinks":drinks, "toiletries":toiletries, "date":date_str, "people_string":people_string}
        templates = settings.template_dict[episode]["templates"]
        num = str(getATemplate(templates))
        #check if template uses all the variables.
        #erase variables (except for date) which are not used
        not_used = format_dict.keys() - set(re.findall(r'{(.+?)}', templates[num]["txt"]))
        for v in not_used:
            if 'date' not in v:
                format_dict[v] = ''
        format_dict['eid'] = 'e'+str(settings.eid)
        df_dict = pd.DataFrame([format_dict])
        settings.weekly_grocery = pd.concat([settings.weekly_grocery, df_dict])

        template_based = templates[num]["txt"].format(**format_dict)
        qa_list = formatQAList(templates[num]["questions"], format_dict)
        temp_logical_rep = [date_str, template_based, fruits, drinks, toiletries, people_string]

        grocery_dict = initDictionary()
        if date_str not in db: 
            db[date_str] = {}
        addEid(grocery_dict, settings.eid)
        settings.eid += 1
        addLogicalRepresentation(grocery_dict, temp_logical_rep)
        addTextTemplate(grocery_dict, template_based)
        addAtomicQAPairs(grocery_dict, qa_list)
        count = get_count(db, date_str, episode)
        db[date_str][episode + count] = grocery_dict

#some weekly episodes can occur more than once a week
def generateWeeklyEpisodes(db, persona):
    bakecook_prob_list = settings.weekly_bakecook_probability[settings.category]
    dating_prob_list = settings.weekly_dating_probability[settings.category]
    hobby_prob_list = settings.weekly_hobby_probability[settings.category]
    grocery_shopping_prob_list = settings.weekly_grocery_shopping_probability[settings.category]

    count = 0
    curr_date = datetime.datetime(settings.current_year, 1, 1)

    cuisine_list = support_db["cusine_list"]
    baking_list = support_db["baking_list"]

    while count <= 365:
        # bake or cook
        delta1 = random.randint(0,2)
        delta2 = random.randint(3,6)
        delta_list = [delta1, delta2]
        for i in range(0, len(bakecook_prob_list)):
            if random.random() < bakecook_prob_list[i]:
                date = curr_date + datetime.timedelta(days=delta_list[i])
                date_str = date.strftime("%Y/%m/%d")
                generateBakeOrCookEpisode(db, persona, cuisine_list, "cook", date_str)

        delta1 = random.randint(0,2)
        delta2 = random.randint(3,6)
        delta_list = [delta1, delta2]
        for i in range(0, len(bakecook_prob_list)):
            if random.random() < bakecook_prob_list[i]:
                date = curr_date + datetime.timedelta(days=delta_list[i])
                date_str = date.strftime("%Y/%m/%d")
                generateBakeOrCookEpisode(db, persona, baking_list, "bake", date_str)

        delta1 = random.randint(0,2)
        delta2 = random.randint(3,6)
        delta_list = [delta1, delta2]
        for i in range(0, len(dating_prob_list)):
            if random.random() < dating_prob_list[i]:
                date = curr_date + datetime.timedelta(days=delta_list[i])
                date_str = date.strftime("%Y/%m/%d")
                generateDatingEpisode(db, persona, "dating", date_str)

        delta1 = random.randint(0,2)
        delta2 = random.randint(3,6)
        delta_list = [delta1, delta2]
        for i in range(0, len(hobby_prob_list)):
            if random.random() < hobby_prob_list[i]:
                date = curr_date + datetime.timedelta(days=delta_list[i])
                date_str = date.strftime("%Y/%m/%d")
                generateHobbyEpisode(db, persona, "hobbies", date_str)


        delta1 = random.randint(0,2)
        delta2 = random.randint(3,6)
        delta_list = [delta1, delta2]
        for i in range(0, len(grocery_shopping_prob_list)):
            if random.random() < grocery_shopping_prob_list[i]:
                date = curr_date + datetime.timedelta(days=delta_list[i])
                date_str = date.strftime("%Y/%m/%d")
                generateGroceryShoppingEpisode(db, persona, "grocery", date_str)
        count = count + 7
        curr_date = curr_date + datetime.timedelta(days=7)

def generateExerciseEpisode(db, persona, episode, date_str):
    start_date = datetime.datetime.strptime(date_str , '%Y/%m/%d').date()
    if start_date.year > settings.current_year:
        return
    if settings.current_age + persona["birth_year"] >= 2005 and settings.current_age >= 18:
        if bool(persona["body_metric"]):
            exercise_prob = settings.daily_exercise_probability[settings.category]
            if passMutualExclusiveCheck(date_str, "exercise", db):
                # while doing exercise, the heart rate will be a bit higher
                health_device = random.choice(settings.body_metric_source_list)
                start_number = random.randint(90, 150)
                temp_heart_rate = random.randint(start_number, 165)

                # randomly choose an exercise from the persona
                exercise = random.choice(settings.exercise_list)
                temp_logical_rep = [date_str, "myself", health_device, "exercise", temp_heart_rate]
                format_dict = {"eid":'e'+str(settings.eid), "exercise":exercise, "date":date_str, "heart_rate": temp_heart_rate}
                df_dict = pd.DataFrame([format_dict])
                settings.daily_exercise = pd.concat([settings.daily_exercise, df_dict])
                templates = settings.template_dict[episode]["templates"]
                num = str(getATemplate(templates))
                template_based = templates[num]["txt"].format(**format_dict)
                qa_list = formatQAList(templates[num]["questions"], format_dict)
                temp_logical_exe_rep = [date_str, exercise]
                exercise_dict = initDictionary()
                if date_str not in db: 
                    db[date_str] = {}
                addEid(exercise_dict, settings.eid)
                settings.eid += 1
                addLogicalRepresentation(exercise_dict, temp_logical_exe_rep)
                addTextTemplate(exercise_dict, template_based)
                addAtomicQAPairs(exercise_dict, qa_list)
                count = get_count(db, date_str, episode)
                db[date_str][episode+count] = exercise_dict

def generateMealEpisode(db, persona, episode, mealtype, date_str):
    start_date = datetime.datetime.strptime(date_str , '%Y/%m/%d').date()
    if start_date.year > settings.current_year:
        return
    people_dict = get_people(persona)
    people_group = flip(settings.people_group, settings.people_group_prob)
    if len(people_dict[people_group]) == 0:
        people_dict[people_group] = ["myself"]
    people = random.sample(people_dict[people_group], random.randint(1, len(people_dict[people_group])))
    people_string = ", ".join(people)

    if settings.current_age + persona["birth_year"] >= 2005 and settings.current_age >= 13:
        meal_prob = settings.daily_meal_probability[settings.category]
        foodtype = ""
        if mealtype == "breakfast":
            foodtype = random.choice(settings.breakfast_list)
        else:
            foodtype = random.choice(settings.lunchdinner_list)

        format_dict = {"mealtype":mealtype, "foodtype":foodtype, "date":date_str, "people_string":people_string}
        templates = settings.template_dict[episode]["templates"]
        num = str(getATemplate(templates))
        #check if template uses all the variables.
        #erase variables (except for date) which are not used
        not_used = format_dict.keys() - set(re.findall(r'{(.+?)}', templates[num]["txt"]))
        for v in not_used:
            if 'date' not in v:
                format_dict[v] = ''
        format_dict['eid'] = 'e'+str(settings.eid)
        df_dict = pd.DataFrame([format_dict])
        settings.daily_meal = pd.concat([settings.daily_meal, df_dict])

        template_based = templates[num]["txt"].format(**format_dict)
        qa_list = formatQAList(templates[num]["questions"], format_dict)
        temp_logical_meal_rep = [date_str, mealtype, foodtype, people_string]
        meal_dict = initDictionary()
        if date_str not in db: 
            db[date_str] = {}
        addEid(meal_dict, settings.eid)
        settings.eid += 1
        addLogicalRepresentation(meal_dict, temp_logical_meal_rep)
        addTextTemplate(meal_dict, template_based)
        addAtomicQAPairs(meal_dict, qa_list)
        count = get_count(db, date_str, mealtype)
        db[date_str][mealtype+count] = meal_dict

def minimumOf(x,y):
    if x < y:
        return x
    else:
        return y

def generateChatEpisode(db, persona, episode, chat_time, date_str):
    start_date = datetime.datetime.strptime(date_str , '%Y/%m/%d').date()
    if start_date.year > settings.current_year:
        return
    friends_list = get_people(persona)['friends']
    people = random.sample(friends_list, random.randint(1, minimumOf(4, len(friends_list))))
    people_string = ", ".join(people)

    howlong = random.randint(5, 55) 

    format_dict = {"eid":'e'+str(settings.eid), "friends":people_string, "timeofday":chat_time, "date":date_str, "howlong":howlong}
    df_dict = pd.DataFrame([format_dict])
    settings.daily_chat = pd.concat([settings.daily_chat, df_dict])
    templates = settings.template_dict[episode]["templates"]
    num = str(getATemplate(templates))
    template_based = templates[num]["txt"].format(**format_dict)
    qa_list = formatQAList(templates[num]["questions"], format_dict)
    temp_logical_chat_rep = [date_str, people_string, chat_time, str(howlong)+" minutes"]
    chat_dict = initDictionary()
    if date_str not in db: 
        db[date_str] = {}
    addEid(chat_dict, settings.eid)
    settings.eid += 1
    addLogicalRepresentation(chat_dict, temp_logical_chat_rep)
    addTextTemplate(chat_dict, template_based)
    addAtomicQAPairs(chat_dict, qa_list)
    count = get_count(db, date_str, episode)
    db[date_str][episode+count] = chat_dict

def generateReadEpisode(db, persona, episode, date_str):
    howlong = random.randint(5, 55) 
    readtype = random.sample(settings.daily_read_list, 1)[0]
    idx = ""
    if readtype == "social media":
        idx = "social media"
    else:
        idx = "read"

    format_dict = {"eid":'e'+str(settings.eid), "readtype":readtype, "date":date_str, "howlong":howlong}
    df_dict = pd.DataFrame([format_dict])
    settings.daily_read = pd.concat([settings.daily_read, df_dict])
    templates = settings.template_dict[episode]["templates"]
    num = str(getATemplate(templates))
    template_based = templates[num]["txt"].format(**format_dict)
    qa_list = formatQAList(templates[num]["questions"], format_dict)
    temp_logical_read_rep = [date_str, readtype, str(howlong)+" minutes"]
    read_dict = initDictionary()
    if date_str not in db: 
        db[date_str] = {}
    addEid(read_dict, settings.eid)
    settings.eid += 1
    addLogicalRepresentation(read_dict, temp_logical_read_rep)
    addTextTemplate(read_dict, template_based)
    addAtomicQAPairs(read_dict, qa_list)
    count = get_count(db, date_str, idx)
    db[date_str][idx+count] = read_dict
    

def generateWatchTVEpisode(db, persona, episode, date_str):
    start_date = datetime.datetime.strptime(date_str , '%Y/%m/%d').date()
    if start_date.year > settings.current_year:
        return
    howlong = random.randint(5, 55) 
    watchtype = random.sample(settings.daily_watch_list, 1)[0]

    format_dict = {"eid":'e'+str(settings.eid), "watchtype":watchtype, "date":date_str, "howlong":howlong}
    df_dict = pd.DataFrame([format_dict])
    settings.daily_watchtv = pd.concat([settings.daily_watchtv, df_dict])
    templates = settings.template_dict[episode]["templates"]
    num = str(getATemplate(templates))
    template_based = templates[num]["txt"].format(**format_dict)
    qa_list = formatQAList(templates[num]["questions"], format_dict)
    temp_logical_rep = [date_str, watchtype, str(howlong)+" minutes"]
    watch_dict = initDictionary()
    if date_str not in db: 
        db[date_str] = {}
    addEid(watch_dict, settings.eid)
    settings.eid += 1
    addLogicalRepresentation(watch_dict, temp_logical_rep)
    addTextTemplate(watch_dict, template_based)
    addAtomicQAPairs(watch_dict, qa_list)
    count = get_count(db, date_str, episode)
    db[date_str][episode + count] = watch_dict
    

def generateDailyEpisodes(db, persona):
    if settings.current_year > settings.current_year:
        return
    start_date = datetime.datetime(settings.current_year, 1, 1)

    exercise_prob = settings.daily_exercise_probability[settings.category]
    meal_prob = settings.daily_meal_probability[settings.category]
    chat_prob_list = settings.daily_chat_with_friends_probability[settings.category]
    read_prob = settings.daily_read_probability[settings.category]
    watch_prob = settings.daily_watch_tv_probability[settings.category]
    count = 0
    while count <= 365:
        start_date_str = start_date.strftime("%Y/%m/%d")
        if random.random() < exercise_prob:
            generateExerciseEpisode(db, persona, "exercise", start_date_str)
        if random.random() < meal_prob:
            generateMealEpisode(db, persona, "meal", "breakfast", start_date_str)
        if random.random() < meal_prob:
            generateMealEpisode(db, persona, "meal", "lunch", start_date_str)
        if random.random() < meal_prob:
            generateMealEpisode(db, persona, "meal", "dinner", start_date_str)
        for i in range(0, len(chat_prob_list)):
            chat_time_list = settings.chat_time_list.copy()
            if random.random() < chat_prob_list[i]:
                chat_time = random.sample(chat_time_list, 1)[0]
                chat_time_list.remove(chat_time)
                generateChatEpisode(db, persona, "chat", chat_time, start_date_str)
        if random.random() < read_prob:
            generateReadEpisode(db, persona, "read", start_date_str)
        if random.random() < watch_prob:
            generateWatchTVEpisode(db, persona, "watch tv", start_date_str)

        count = count + 1
        start_date = start_date + datetime.timedelta(days=1)
