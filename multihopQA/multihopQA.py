import csv
import getopt
import json
import os
import random
import re
import sys

import pandas as pd
from numpyencoder import NumpyEncoder
from pandasql import sqldf

df = ""
df1 = ""
df2 = ""
df3 = ""
query = ""
datafile = ""
directories = ""
queryfile = ""
queryid = ""

mysql = lambda q: sqldf(q, globals())


def processDataFiles(datafiles, d):
    global df
    global df1
    global df2
    global df3

    df = pd.read_csv(d + "/" + datafiles[0])
    df1 = pd.read_csv(d + "/" + datafiles[0])
    df, df1 = processDataFile(datafiles[0], df, df1)
    # df1 is a flattened version of df

    df2 = ""
    df3 = ""
    if len(datafiles) > 1:
        df2 = pd.read_csv(d + "/" + datafiles[1])
        df3 = pd.read_csv(d + "/" + datafiles[1])
        df2, df3 = processDataFile(datafiles[1], df2, df3)
    # df2 is a flattened version of df3

    return df, df1, df2, df3


def processDataFile(datafile, f0, f1):
    if datafile == 'daily_chat-log.csv':
        # f1 contains a flatten version of f0
        f1['friends'] = list(f1['friends'].str.split(","))
        f1 = f1.explode('friends')
        if len(f1['friends']) > 0:
            f1['friends'] = f1['friends'].str.strip()
    elif datafile == 'daily_meal-log.csv':
        f1['people_string'] = list(f1['people_string'].str.split(","))
        f1 = f1.explode('people_string')
        if len(f1['people_string']) > 0:
            f1['people_string'] = f1['people_string'].str.strip()
    elif datafile == 'weekly_bakeorcook-log.csv':
        f1['cuisine'] = list(f1['cuisine'].str.split(","))
        f1 = f1.explode('cuisine')
        if len(f1['cuisine']) > 0:
            f1['cuisine'] = f1['cuisine'].str.strip()
    elif datafile == 'weekly_grocery-log.csv':
        f1['fruits'] = list(f1['fruits'].str.split(","))
        f1 = f1.explode('fruits')
        if len(f1['fruits']) > 0:
            f1['fruits'] = f1['fruits'].str.strip()
    elif datafile == 'weekly_hobby-log.csv':
        f1['people_string'] = list(f1['people_string'].str.split(","))
        f1 = f1.explode('people_string')
        if len(f1['people_string']) > 0:
            f1['people_string'] = f1['people_string'].str.strip()

    # preprocessing dates
    if datafile == 'marriages-log.csv':
        f0['married_date'] = pd.to_datetime(f0['married_date'])
        f0['year'] = f0['married_date'].dt.year
        f0['month'] = f0['married_date'].dt.month
    elif datafile == 'travel-log.csv':
        f0['start_date'] = pd.to_datetime(f0['start_date'])
        f0['end_date'] = pd.to_datetime(f0['end_date'])
        f0['start_year'] = f0['start_date'].dt.year
        f0['start_month'] = f0['start_date'].dt.month
    elif datafile == 'travel_dining-log.csv':
        f0['start_date'] = pd.to_datetime(f0['start_date'])
        f0['end_date'] = pd.to_datetime(f0['end_date'])
        f0['dining_date'] = pd.to_datetime(f0['dining_date'])
        f0['place_visit_date'] = pd.to_datetime(f0['place_visit_date'])
    elif datafile == 'travel_places_visited-log.csv':
        f0['start_date'] = pd.to_datetime(f0['start_date'])
        f0['end_date'] = pd.to_datetime(f0['end_date'])
        f0['place_visit_date'] = pd.to_datetime(f0['place_visit_date'])
    else:
        f0['date'] = pd.to_datetime(f0['date'])
        f0['year'] = f0['date'].dt.year
        f0['month'] = f0['date'].dt.month
        f1['date'] = pd.to_datetime(f1['date'])
        f1['year'] = f1['date'].dt.year
        f1['month'] = f1['date'].dt.month

    return f0, f1


def main(argv):
    global df
    global df1
    global df2
    global df3
    global query
    global datafiles
    global directories
    global queryfile
    global queryid
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    try:
        opts, args = getopt.getopt(argv, "hq:d:", ["query=", "directories="])
    except getopt.GetoptError:
        print("python multihopQA.py -h -q <queryfile> -d <directories>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print()
            print("python multihopQA.py -h -q <queryfile> -d <directories>")
            print("query file contains (sqlquery, inputfilename) pairs. assumed to be in current directory")
            print("directories is a list of directories relative to the current directory where the sqlquery will be executed against the inputfilename")
            sys.exit()
        elif opt == "-q":
            queryfile = arg
        elif opt == "-d":
            directories = list(arg.split(" "))

        queryfile = 'queryfile.csv'
        for d in directories:
            queries_data = {
                'q_id': [],
                'query': [],
                'params': [],
                'question': [],
                'datafiles': [],
                'answer_column' :[]
            }
            with open(queryfile, "r") as f:
                obj = csv.reader(f, delimiter=",")
                # execute every row in f
                for row in obj:
                    queryid = row[0]
                    if queryid == 'q33':
                        print()
                    query = row[1]
                    datafiles = row[2]
                    variables = row[3].split(",")
                    question = row[4]
                    answer_col = row[6]
                    predefined_params = {}
                    if row[5].strip() != '':
                        predefined_params = json.loads(row[5])
                    tem_list = []
                    for v in variables:
                        v = v.strip()
                        if len(v) > 0:
                            tem_list.append(v)
                    variables = tem_list

                    # check if multiple data files are used
                    datafiles = list(map(lambda x: x.strip(), datafiles.split(",")))

                    print(" ")
                    print(queryid)
                    df, df1, df2, df3 = processDataFiles(datafiles, d)

                    if df.size > 0:
                        format_dict = {}
                        if queryid in ['q2', 'q3', 'q4', 'q6', 'q10', 'q16', 'q18', 'q23', 'q24', 'q25']:
                            print("*** df1 ***")
                            print(df1)
                            if len(variables) > 0:
                                x = df1.sample(1)
                                for v in variables:
                                    format_dict[v] = x.iat[0, df1.columns.get_loc(v)]
                                query = query.format(**format_dict)
                        elif queryid in ['q7', 'q8', 'q9', 'q11', 'q12', 'q13', 'q14', 'q15', 'q19', 'q26', 'q28',
                                         'q29', 'q30', 'q31', 'q32', 'q39', 'q40', 'q41']:
                            if len(variables) > 0:
                                x = df.sample(1)
                                for v in variables:
                                    value = x.iat[0, df.columns.get_loc(v)]
                                    if v == 'people' and len(value.split(",")) > 1:
                                        value = random.sample(value.split(","), 1)[0]
                                    format_dict[v] = value
                                query = query.format(**format_dict)

                        if len(format_dict) > 0:
                            q_params = re.findall(r'\{[a-z_]*\}', question, flags=0)
                            for qp in q_params:
                                key = qp[1:-1]
                                value = format_dict[key]
                                if key == 'month' and len(str(value)) < 3:
                                    value = months[value - 1]
                                question = question.replace(qp, str(value))
                        format_dict.update(predefined_params)
                        queries_data['q_id'].append(queryid)
                        queries_data['query'].append(query)
                        queries_data['params'].append(json.dumps(format_dict, ensure_ascii=False, cls=NumpyEncoder))
                        queries_data['question'].append(question)
                        queries_data['answer_column'].append(answer_col)
                        queries_data['datafiles'].append(','.join(datafiles))
                        print(query)

                        result = mysql(query)
                    else:
                        result = pd.DataFrame()
                    print("Result:")
                    print(result)
                    result.to_csv(os.path.join(d, queryid + "-result.csv"))

            querylog_path = os.path.join(d, 'queries.csv')
            query_df = pd.DataFrame(data=queries_data)
            query_df.to_csv(querylog_path, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
