# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


import json

#TODO: Need real databases in place of the ones below
HOBBIES_DB = ["working out", "arts and crafts", "board games", "diy", "yoga", "baking", "gardening", "video games", "meditation", "audiobooks and podcasts", "writing", "learning a language", "learning an instrument"]
EXERCISE_DB = [ "soccer", "basketball", "tennis", "baseball", "golf", "running", "volleyball", "badminton", "swimming", "boxing", "table tennis", "skiing", "ice skating", "roller skating", "cricket", "rugby", "pool", "darts", "football", "bowling", "ice hockey", "surfing", "karate", "horse racing", "snowboarding", "skateboarding", "cycling", "archery", "fishing", "gymnastics", "figure skating", "rock climbing", "sumo wrestling", "taekwondo", "fencing", "water skiing", "jet skiing", "weight lifting", "scuba diving", "judo", "wind surfing", "kickboxing", "sky diving", "hang gliding", "bungee jumping", "running", "swimming", "weight lifting", "golfing", "playing soccer", "running", "jogging", "weight lifting", "biking", "hiking", "HIIT" ]
MALE_NAMES_DB = ["Liam", "Noah", "Oliver", "Elijah", "William", "James", "Benjamin", "Lucas", "Henry", "Alexander", "Mason", "Michael", "Ethan", "Daniel", "Jacob", "Logan", "Jackson", "Levi", "Sebastian", "Mateo", "Jack", "Owen", "Theodore", "Aiden", "Samuel", "Joseph", "John", "David", "Wyatt", "Matthew", "Luke", "Asher", "Carter", "Julian", "Grayson", "Leo", "Jayden", "Gabriel", "Isaac", "Lincoln", "Anthony", "Hudson", "Dylan", "Ezra", "Thomas", "Charles", "Christophe", "Jaxon", "Maverick", "Josiah", "Isaiah", "Andrew", "Elias", "Joshua", "Nathan", "Caleb", "Ryan", "Adrian", "Miles", "Eli", "Nolan", "Christian", "Aaron", "Cameron", "Ezekiel", "Colton", "Luca", "Landon", "Hunter", "Jonathan", "Santiago ", "Axel", "Easton", "Cooper", "Jeremiah", "Angel", "Roman", "Connor", "Jameson", "Robert", "Greyson", "Jordan", "Ian", "Carson", "Jaxson", "Leonardo", "Nicholas", "Dominic", "Austin", "Everett", "Brook", "Xavier", "Kai", "Jose", "Parker", "Adam", "Jace", "Wesley", "Kayden", "Silas", "Lambert", "Nathan", "Alon", "Chris", "Mike", "Richard"]
FEMALE_NAMES_DB = ["Olivia","Emma","Charlotte","Amelia","Ava","Sophia","Isabella","Mia","Evelyn","Harper","Luna","Camila","Gianna","Elizabeth","Eleanor","Ella","Abigail","Sofia","Avery","Scarlett","Emily","Aria","Penelope","Chloe","Layla","Mila","Nora","Hazel","Madison","Ellie","Lily","Nova","Isla","Grace","Violet","Aurora","Riley","Zoey","Willow","Emilia","Stella","Zoe","Victoria","Hannah","Addison","Leah","Lucy","Eliana","Ivy","Everly","Lillian","Paisley","Elena","Naomi","Maya","Natalie","Kinsley","Delilah","Claire","Audrey","Aaliyah","Ruby","Brooklyn","Alice","Aubrey","Autumn","Leilani","Savannah","Valentina","Kennedy","Madelyn","Josephine","Bella","Skylar","Genesis","Sophie","Hailey","Sadie","Natalia","Quinn","Caroline","Allison","Gabriella","Anna","Serenity","Nevaeh","Cora","Ariana","Emery","Lydia","Jade","Sarah","Eva","Adeline","Madeline","Piper","Rylee","Athena","Peyton","Everleigh", "Marzieh", "Jane", "Wang-Chiew", "Lily", "Emily", "Claire"]
PETS_NAMES_DB = ["Max", "Bella", "Charlie", "Cooper", "Lucy", "Buddy", "Daisy", "Rocky", "Lily", "Milo", "Zoe", "Jack", "Lola", "Bear", "Molly", "Duke", "Sadie", "Teddy", "Bailey", "Dakota", "Luka", "Mario", "Mokah", "Jupyter", "Torch", "Lucy"]
EXCUR_ACTIVITIES = ["academic", "academic competitive teams", "art", "cultural and language", "community", "government", "leadership", "media", "military", "music", "performance art", "religious", "roleplaying/fantasy", "social activism", "special interest", "speech and political interest", "sports and recreation", "technology", "volunteer"]


#TODO: add more categories and subcategories
profession_dict = {}
profession_dict["Astrophysics"] = ["Research", "Writing", "Education", "Consulting", "Public relations"]
profession_dict["CS"] = ["Research and development", "Application systems", "Operating systems", "Maintenance"]
profession_dict["English"] = ["Creative Writing", "Journalism", "Professional writing"] 
profession_dict["Others"] = ["Startups", "self-employed"]

location_dict = {'engagement': ['restaurants','my place', 'our home', 'Disney Land','Street'], 'marriage': ['restaurants', 'my place', 'our home', 'Disney Land', 'Street'], 'buying_groceries': ['Costco', "Trader Joe's", 'Ranch 99','HMart','Food Cellar', 'Safeway', 'Whole Foods', 'T&T'], 'walking_pets':['backyard', 'dog park', 'along the river', 'neighboring streets', 'play ground'], 'visiting_tourist_places': [], 'buying_gifts': [], 'spending_time_with_friends':[], 'spending_time_with_family':[], 'driving_liscence':['DMV'], 'special_kids_moments': ['at home', 'at school'], 'visiting_denstists': [], 'visiting_optometrist': [], 'exercise': ["gym", "play ground", "home", "garage", "outside"], 'health_care_insurance': ["online", "making a phone call", "insurance company"], 'reading': ["at home", "library", "reading group"], 'doing_house_work': ['at home'], 'property_investment': ['at home', 'at consultant\'s office'], 'body_metric': ['apple watch', 'iphone', 'fitness apps'], 'pet_care': ['vet', 'animal service center', 'at home', 'at Lounge','at my place'], 'self_care':['relaxing center', 'outside'], 'shopping': ['shopping centers'], 'doing_house_work': [''], 'vaccination': ['pharmacy', 'hosptial', 'community center'], 'bring_a_child_to_school':[], 'attending_support_groups': [], 'k_graduation': ['kindergarten'], 'e_graduation': ['elementary school'], 'm_graduation': ['middle school'], 'h_graduation':['high school'], 'trips': ["Paris, France", "New York, USA", "Rome, Italy",  "London, UK", "Tokyo, Japan",  "Lisbon, Portugal", "Barcelona, Spain", "Honolulu, Hawaii", "Bangkok, Thailand", "Hong Kong, China", "Dubai, United Arab Emirates", "Singapore, Singapore", "Rome, Italy"] }

support_db = {'cusine_list': ['macaroni and cheese',
                              'favorite chicken potpie',
                              'contest-winning broccoli chicken casserole',
                              'traditional meat loaf',
                              'cream of celery soup recipe',
                              'hungarian chicken paprikash',
                              'shrimp quesadilla',
                              'chicken and gravy',
                              'salmon chowder',
                              'broccoli-stuffed chicken',
                              'turkey shepherd’s pie',
                              'ground turkey vegetable soup',
                              'slow-cooker pork loin',
                              'swedish meatball recipe',
                              'crockpot spareribs',
                              'chicken parmesan spaghetti',
                              'healthy turkey chili',
                              'instant pot whole chicken',
                              'hamburger stroganoff',
                              'creamed garden potatoes and peas',
                              'air-fryer brats',
                              'so-easy sloppy joes',
                              'cube steak and gravy',
                              'tender salsa beef',
                              'au gratin peas and potatoes',
                              'split pea soup with ham & jalapeno',
                              'rigatoni with sausage & peas',
                              'cheesy ham chowder',
                              'chicken cordon bleu skillet',
                              'general tso’s chicken',
                              'beef and broccoli',
                              'asian slaw',
                              'chinese noodle soup',
                              'gado gado',
                              'chinese vegetable stir-fry',
                              'chinese broccoli with oyster sauce',
                              'thai noodle salad',
                              'lo mein',
                              'chow mein',
                              'chinese chicken wings',
                              'ramen noodle stir-fry',
                              'thai green curry paste',
                              'vietnamese coffee',
                              'wonton soup',
                              'scallion pancake',
                              'naan bread',
                              'indian red lentil',
                              'cashew chicken ',
                              'sushi',
                              'poke'],
              'baking_list': ['vegan sugar cookies',
                              'brownies',
                              'peanut butter cookies',
                              'pistachio oat squares',
                              'carrot cake',
                              'blackberry jam pie-crust straws',
                              'cream-filled bundt cake',
                              'chocolate skillet cake',
                              'gluten-free apple rose tart',
                              'chrissy teigen’s 3-ingredient chocolate mousse',
                              'blackberry-raspberry skillet cobbler',
                              'easy cherry skillet cake',
                              'chocolate chip cookie in a mug',
                              'birthday cupcakes with white wine buttercream',
                              'homemade toaster pastries',
                              'dessert nachos',
                              'chocolate-chip mug brownie',
                              'lemon meringue cookies',
                              'cheater’s mini rhubarb galettes',
                              'easy peanut butter fudge',
                              'cranberry apple danish',
                              'fig tarte tatin',
                              'giant cinnamon roll',
                              'brown sugar-pear puff pastries',
                              'cinnamon sheet cake with cider frosting',
                              'easy chocolate marshmallow cups'],
              'date_location_list': ['a park',
                                     'a restaurant',
                                     'a coffee Shop',
                                     'a boba shop'],
              'self_entertainment_list ': ['reading a book',
                                           'listening to an audio book',
                                           'doing meditation',
                                           'watching a movie',
                                           'listen to music'],
              'self_entertainment_type_dict': {'reading a book': ['Science Fiction'],
                                               'listening to an audio book': ['Science Fiction'],
                                               'doing meditation': ['mindfulness',
                                                                    'spiritual',
                                                                    'focused',
                                                                    'movement',
                                                                    'mantra'],
                                               'watching a movie': ['Science Fiction'],
                                               'listen to music': ['Classic']}}

mutual_exclusive_dict = {'relocation': ['marriage', 'travel', 'dining', 'places_visited', 'personal_medical_care', 'parent_medical_care', 'child_medical_care', 'pet_care', 'bake', 'cook', 'exercise', 'travel'],
                         'travel': ['parent_medical_care', 'child_medical_care', 'personal_medical_care', 'pet_care', 'exercise', 'job_move', 'college move', 'graduate school move', 'hobbies', 'cook', 'bake'],
                         'exercise': ['travel', 'dining', 'places_visited'],
                         'cook': ['travel', 'dining', 'places_visited'],
                         'bake': ['travel', 'dining', 'places_visited'],
                         'hobbies': ['travel', 'job_move', 'dining', 'places_visited'],
                         'pet_care': ['travel', 'job_move', 'graduate school move', 'college move', 'marriage'],
                         'grocery': ['travel', 'relocation', 'marriage'],
                         'personal_medical_care': ['travel',
                                             'job_move',
                                             'college move',
                                             'graduate school move',
                                             'child_medical_care',
                                             'parent_medical_care'],
                                             
                         'child_medical_care': ['travel',
                                                'job_move',
                                                'college move',
                                                'graduate school move',
                                                'parent_medical_care',
                                                'personal_medical_care'],
                         'parent_medical_care': ['travel',
                                                    'job_move',
                                                    'college move',
                                                    'graduate school move',
                                                    'child_medical_care',
                                                    'personal_medical_care']}

all_episodes_schema = {'trips': ['start_date', 'end_date', 'people', 'location'],
                       'transportation': ['date', 'carrier', 'people', 'location'],
                       'accomodation': ['date', 'carrier', 'people', 'location'],
                       'places_visited': ['date', 'people', 'location', 'events', 'feeling'],
                       'eating_outside': ['date', 'people', 'location', 'food_type'],
                       'buying_souvenirs': ['date', 'people', 'location', 'souvenirs'],
                       'birth_information': ['date', 'location', 'parents'],
                       'celebrating_holidays': ['date', 'people', 'location'],
                       'high_school': ['date', 'people', 'location'],
                       'college': ['date', 'people', 'location'],
                       'graduate_school': ['date', 'people', 'location'],
                       'married': ['date', 'people', 'location'],
                       'engagement': ['date', 'people', 'location'],
                       'moving': ['date', 'location', 'people', 'event'],
                       'started_job': ['date', 'people'],
                       'quit_job': ['date', 'people']}

travel_db = {"Rome, Italy": {"restaurants": {"dining": ["Trapizzino", "Dar Filettaro", "Mozao", "Pizzarium", "Panificio Bonci"], "street food": ["La Pergola", "Marco Martini Restaurant", "Aroma", "Glass Hostaria", "Pipero"], "local food": ["Pasta alla Carbonara", "Tonnarelli Cacio e Pepe", "Trippa alla Romana", "Bucatini all'Amatriciana & Pasta alla Gricia", "Cicoria ripassata"]}, "places_to_visit": ["The Colosseum and the Arch of Constantine", "Vatican City", "The Pantheon", "Roman Forum", "Trevi Fountain"]}, "Paris, France": {"restaurants": {"dining": ["Panificio Bonci", "Man\u2019Ouch\u00e9", "Breizh Cafe", "Le Food Market"], "street food": ["Le Meurice Alain Ducasse", "Pavillon Ledoyen", "Epicure", "Le Jules Verne", "Le Meurice", "Restaurant Guy Savoy, Monnaie de Paris"], "local food": ["Croissants", "Macarons", "Onion soup", "Escargots", "Jambon-beurre"]}, "places_to_visit": ["Eiffel Tower", "Notre Dame Cathedral", "Louvre Museum", "Champs Elys\u00e9es", "Montmartre"]}, "New York, US": {"restaurants": {"dining": ["The Cinnamon Snail", "Korilla BBQ", "The Halal Guys", "Melt Bakery", "Nuts 4 Nuts"], "street food": ["Jean-Georges", "Le Bernardin", "Per Se", "Scalini Fedeli", "Sushi Noz", "Shuko"], "local food": ["Cheesecake", "Bagel", "Cronut", "Egg Cream", "General Tso's Chicken"]}, "places_to_visit": ["Central Park", "Empire State Building", "Times Square", "Brooklyn Bridge", "Statue of Liberty", "Rockefeller Center", "Metropolitan Museum of Art"]}, "Los Angeles, US": {"restaurants": {"dining": ["Guatemalan Night Market", "Es Todo Vegan Street Food", "Corporation Food Hall"], "street food": ["Providence", "M\u00e9lisse", "Hayato", "Phenakite", "Pasjoli"], "local food": ["Birria tacos", "Strawberry donuts", "Ice cream sandwich"]}, "places_to_visit": ["Hollywood Walk of Fame", "Universal Studios Hollywood", "Santa Monica Pier", "Getty Center", "Griffith Park and Observatory"]}, "Sydney, Australia": {"restaurants": {"dining": ["Bombay Street Kitchen", "Thievery Chicken & Charcoal", "Love Crepe"], "street food": ["Sixpenny", "Bennelong", "Automata"], "local food": ["Barramundi", "Sydney rock oyster", "Australian prawns"]}, "places_to_visit": ["Sydney Opera House", "Bondi Beach", "Sydney Harbour Bridge"]}, "Seoul, South Korea": {"restaurants": {"dining": ["Gwangjang Market", "Seoul Bamdokkaebi Night Market", "Myeongdong Street Food Alley", "Common Ground"], "street food": ["Doore Yoo", "Dining in Space", "Balwoo Gongyang", "Cheong Jin Ok", "Imun Seolnongtang"], "local food": ["TTEOKBOKKI", "Fish cake", "Hotteok"]}, "places_to_visit": ["N Seoul Tower", "National Museum Of Korea", "Lotte World Tower"]}, "Miami, US": {"restaurants": {"dining": ["El Zambo Street Food", "Ms. Cheezious", "Miami Street Food Court"], "street food": ["The Surf Club Restaurant", "L'Atelier de Jo\u00ebl Robuchon", "MILA Restaurant", "Forte dei Marmi", "Zuma Miami"], "local food": ["Chicharr\u00f3n", "Stone Crabs", "Arepas", "Mofongo", "Key Lime Pie", "Ceviche"]}, "places_to_visit": ["Miami Beach", "Art Deco Historic District", "South Beach", "Vizcaya Museum and Gardens"]}, "Rio, Brazil": {"restaurants": {"dining": ["Tapioca", "P\u00e3o de queijo", "Bolinho de bacalhau"], "street food": ["Confeitaria Colombo", "Iraj\u00e1 Gastr\u00f4", "Olympe"], "local food": ["Feijoada", "Churrascaria", "P\u00e3o de queijo with Requeijao", "Coxinha de Galinha", "Brigadeiro"]}, "places_to_visit": ["Cristo Redentor", "Sugarloaf", "Copacabana", "Ipanema", "Carnaval"]}, "Philadelphia, US": {"restaurants": {"dining": ["High Street Philly", "Lunch Street", "Wokworks City Hall Food Cart", "South Street Diner", "Wood Street Pizza"], "street food": ["Lacroix", "Jean-Georges Philadelphia", "Barclay Prime", "Vetri Cucina", "Laurel"], "local food": ["Philly Cheesesteaks", "Roast Pork Sandwich", "Philly Soft Pretzels"]}, "places_to_visit": ["Liberty Bell", "Independence Hall", "Philadelphia Museum of Art", "Ipanema", "Carnaval"]}, "Shanghai, China": {"restaurants": {"dining": ["Fangbang Xi Lu", "Wanhangdu Lu junction", "Yuyuan Lu junction", "South Bund Fabric Market"], "street food": ["Ultraviolet by Paul Pairet", "8\u00bd Otto e Mezzo", "T\u2019ang Court", "Jean-Georges Shanghai", "Sh\u00e0ng-X\u00ed"], "local food": ["Xiaolongbao", "Steamed Crab", "Smoked Fish Sliceso", "Beggar's Chicken", "Braised eggplant"]}, "places_to_visit": []}, "Barcelona, Spain": {"restaurants": {"dining": ["Pizza Del Born", "Bar Bo de B", "Maoz", "Pizza Market", "Ciutat Comtal"], "street food": ["UCon Gracia", "LAB Restaurant", "La Dama", "Els Pescadors"], "local food": ["Patatas Bravas", "Croquetas", "Tortilla de Patatas", "Entrep\u00e1"]}, "places_to_visit": []}, "London, UK": {"restaurants": {"dining": ["Bang Bang Oriental", "Berwick Street Market", "Brixton Village", "Broadway Market", "Buck Street Market"], "street food": ["Amaya", "Angler", "Barrafina", "Benares", "Chez Bruce"], "local food": ["Fish and Chips", "Bangers and Mash", "Sunday Roast", "Shepherd's Pie"]}, "places_to_visit": ["Hyde Park", "Westminster", "Camden", "London Eye", "Tower of London"]}, "New Delhi, India": {"restaurants": {"dining": ["Chawri Bazar", "Moolchand", "Connaught Place", "Yashwant Place", "Chandni Chowk"], "street food": ["Spring", "Dilli 32", "Tamra", "Mosaic"], "local food": ["Paranthas", "Chaat", "Butter Chicken", "Kebabs", "Chole Bhature"]}, "places_to_visit": ["The Red Fort", "Qutub Minar", "Lodi Gardens", "Gurudwara Bangla Sahib", "The Lotus Temple"]}, "Bangkok, Thailand": {"restaurants": {"dining": ["Victory Monument", "Yaowarat", "Ratchawat Market"], "street food": ["Benihana", "Akira Back", "The Silk Road", "Elements, Inspired by Ciel Bleu", "Sra Bua by Kiin Kiin"], "local food": ["Papaya Salad", "Tom Yum Goong", "Pad Thai", "Kao Niew Mamuang", "Khao Soi"]}, "places_to_visit": ["Grand Palace", "Wat Arun", "Wat Traimit", "Wat Suthat", "National Museum & Wang Na Palace"]}, "Dubai, UAE": {"restaurants": {"dining": ["Falafel Alzaeem", "Sind Punjab", "Hor Al Anz Bakery"], "street food": ["Zengo", "Social by Heinz Beck", "Buddha-Bar", "eBombay Brasserie", "Indego by Vineet"], "local food": ["Stuffed Camel", "Shawarma", "Matchbous"]}, "places_to_visit": ["Burj Khalifa", "Dubai Aquarium & Underwater Zoo", "Miracle Garden"]}}
