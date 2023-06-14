# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


def init():
    global final_year 
    global current_year
    global duration
    global current_age
    global verbose
    global template_dict
    global model
    global seed 
    global category

    global marriages # date, partner_name
    global moves # date, type of move
    global travel # date, end_date, city, people
    global travel_places_visited # date, end_date, city, people, place_visit_date, place, action, emotion
    global travel_dining # date, end_date, city, dining_date, food_type, food_location 
    global annual_medical_care # date, for whom, type of care
    global monthly_pet_care # date, pet_care_type
    global weekly_grocery  # date, fruits, drinks, toiletries, people
    global weekly_bakecook  # date, bake_or_cook, cuisine, people, location
    global weekly_dating # date, people_string, location
    global weekly_hobby # date, hobby, people
    global daily_exercise # date, health_device, heart_rate
    global daily_read # date, readtype, howlong
    global daily_watchtv # date, watchtype, howlong
    global daily_meal # date,mealtype,foodtype,people
    global daily_chat # date,people,chat_time,howlong


    global transportation
    global cities
    global people_group
    global tourist_actions
    global tourist_emotions
    global food_type
    global self_care_list
    global pet_care_list
    global medical_care_type
    global medical_care_locations

    global transportation_prob
    global people_group_prob 
    global tourist_actions_prob
    global tourist_emotions_prob
    global exercise_prob
    global exercise_list
    global body_metric_list
    global body_metric_source_list
    global visit_a_place
    global dining_probability
    global cooking_probability
    global daily_exercise_probability
    global daily_meal_probability
    global daily_chat_probability 
    global chat_time_list
    global weekly_bakecook_probability
    global weekly_dating_probability
    global weekly_hobby_probability
    global weekly_grocery_shopping_probability
    global daily_read_prob
    global daily_read_list
    global daily_watch_tv_probability
    global daily_watch_list
    global breakfast_list
    global fruit_list
    global drink_list
    global toiletry_list
    global lunchdinner_list
    global city_country_list
    global college_list
    global major_list 
    global eid #episode id
