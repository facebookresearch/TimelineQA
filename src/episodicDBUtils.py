import datetime
import numpy as np
import random
import math
import string

from persona_generator import flip, yearly_month_date_generator, location_dict

verbose = False

#initialize dictionary
def initDictionary():
    dictionary = {}
    dictionary["eid"] = ""
    dictionary["logical_representation"] = []
    dictionary["text_template_based"] = [""] 
    dictionary["text_model_based"] = [""] #TODO: not used now. for generating text from LM
    dictionary["atomic_qa_pairs"] = []
    dictionary["multihop_qa_pairs"] = []
    return dictionary

def addEid(dictionary, eid):
    dictionary["eid"] = "e"+str(eid)

def addLogicalRepresentation(dictionary, lr):
    dictionary["logical_representation"] = lr

def addTextTemplate(dictionary, t):
    dictionary["text_template_based"] = t

def addTextFromModel(dictionary, t):
    dictionary["text_model_based"] = t

def addAtomicQAPairs(dictionary, ql):
    dictionary["atomic_qa_pairs"] = ql

def addMultiHopQAPairs(dictionary, ql):
    dictionary["multihop_qa_pairs"] = ql

def getMonth():
    return random.randint(low=1, high=12)

def getDay():
    # does not consider 29, 30, 31
    return random.randint(low=1, high=28)

def getATemplate(template_dict):
    size = len(template_dict.keys())
    random_num = random.randint(0, size-1)
    return random_num

# generate people who will be there with you for events
def get_people(persona):
    people_dict = {}
    people_dict["parents"] = [persona["biological_mom_name"]] + [persona["biological_dad_name"]] + persona[
        "sibling_names"]
    people_dict["friends"] = persona["close_friends_names"]
    people_dict["family"] = persona["partners_names"] + persona["kids_names"]

    return people_dict

