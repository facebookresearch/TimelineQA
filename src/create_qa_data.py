# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


import json
import os
import random

import pandas as pd


def create_atomic_training(path='epi_data'):
    os.makedirs(os.path.join(path, 'QA'), exist_ok=True)
    databases = []
    sub_dirs = ['benchmark']  # , 'dense', 'medium']
    for sub_dir in sub_dirs:
        all_dirs = [direc for direc in os.listdir(os.path.join(path, sub_dir)) if
                    os.path.isdir(os.path.join(path, sub_dir, direc))]
        for direc in all_dirs:
            data_path = f'{path}/{sub_dir}/{direc}/{direc}.json'
            data = json.load(open(data_path))
            dates = sorted(list(data.keys()))
            text_db = []
            questions = []
            multi_hop_questions = create_multi_hop_training(path, sub_dir, direc)
            for i, date in enumerate(dates):
                events = data[date]
                for event_name in events.keys():
                    event = events[event_name]
                    text = event['text_template_based']
                    text_db.append((date, event_name, event['eid'], text))
                    atomic_qa_pairs = event['atomic_qa_pairs']
                    for qa_pair in atomic_qa_pairs:
                        q = qa_pair[0]
                        a = qa_pair[1]
                        questions.append(
                            {"question": q, "answer": [[a]], "evidence_list": [(date, event_name, event['eid'], text)]})
            sampled_questions = random.sample(questions, 100)
            database = {
                'name': direc,
                'text': text_db,
                'atomic-questions': sampled_questions,
                'multihop-questions': multi_hop_questions
            }
            databases.append(database)
            json.dump(database, open(os.path.join(path, f'QA/db-{direc}.json'), "w"), indent=True)
    return databases


def split_date(list_dates):
    splits = [d.split('/') for d in list_dates]
    years = [d[0] for d in splits]
    months = [str(int(d[1])) for d in splits]
    days = [int(d[2]) for d in splits]

    return years, months, days


def create_multi_hop_training(path, sub_dir, direc):
    questions = []
    data_path = f'{path}/{sub_dir}/{direc}/queries.csv'
    json_data = json.load(open(f'{path}/{sub_dir}/{direc}/{direc}.json'))
    query_df = pd.read_csv(data_path)
    for ind, row in query_df.iterrows():
        q_id = row['q_id']
        question = row['question']
        # getting the answer
        if row['answer_column'] == '?':
            continue
        if ind == 0:
            print()
        answer_col = row['answer_column'].split(',')
        ans_col = [int(answer_col[0])]
        answer_rows = open(f'{path}/{sub_dir}/{direc}/{q_id}-result.csv').read().splitlines()[1:]
        if len(answer_col) > 1:
            if answer_col[-1] != ':':
                ans_col.append(int(answer_col[-1]))
        answer = [r.split(',')[ans_col[0]:ans_col[-1] + 1] for r in answer_rows]
        # getting evidence
        params = json.loads(row['params'])
        evidence_list = []
        datafile = row['datafiles'].split(',')[0]

        df_file = pd.read_csv(f'{path}/{sub_dir}/{direc}/{datafile}')
        date_column = 'date'
        if 'date' not in set(df_file.columns):
            if datafile == 'travel_dining-log.csv' and 'dining_date' in set(df_file.columns):
                date_column = 'dining_date'
            elif 'place_visit_date' in set(df_file.columns):
                date_column = 'place_visit_date'
            elif 'start_date' in set(df_file.columns) or 'start_year' in set(params.keys()):
                date_column = 'start_date'
            else:
                print(datafile, ' does not have existing date columns')
        dates_str = list(df_file[date_column])
        years, months, days = split_date(dates_str)
        df_file['year'] = years
        df_file['month'] = months
        df_file['day'] = days
        columns = set(df_file.columns)
        df_file_filtered = df_file
        for param in params:
            if param in columns or param == 'start_year':
                param_value = str(params[param])
                if param == 'start_year':
                    param = 'year'
                if '%' in str(param_value) or 'friend' in param or 'people' in param:
                    df_file_filtered = df_file_filtered[df_file_filtered[param].str.contains(param_value, na=False)]
                else:
                    if (' since ' in question or ' after ' in question) and param == 'year':
                        df_file_filtered = df_file_filtered[df_file_filtered[param] >= param_value]
                    else:
                        df_file_filtered = df_file_filtered[df_file_filtered[param] == param_value]
        relevant_dates = list(df_file_filtered[date_column])
        event_ids = set(df_file_filtered['eid'])
        for rel_date in relevant_dates:
            date_json = json_data[rel_date]

            for event_name in date_json:
                event = date_json[event_name]  # and event in set(params.values()):
                if event['eid'] in event_ids:
                    evidence_list.append((rel_date, event_name, event['eid'], event['text_template_based']))
        print(data_path, ind, q_id, datafile, question)
        assert len(evidence_list) >= len(df_file_filtered)
        questions.append({"question": question, "answer": answer, "evidence_list": evidence_list})

    return questions


dbs = create_atomic_training(path=os.getcwd())
print()
