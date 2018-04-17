# -*- coding: UTF-8 -*-

import json

def add_english_entries():
    all_characters_file = open('all_characters.json', 'r', encoding='utf-8')
    rashid_file = open('rashid_with_english.json', 'r', encoding='utf-8')

    all_response = json.load(all_characters_file)
    rashid_response = json.load(rashid_file)
    all_obj = all_response['rows']



    for rashid_i in range(0,len(rashid_response)):
        if "index" in rashid_response[rashid_i]["doc"].keys():
            #rashid_index = rashid_response[rashid_i]["doc"]["index"] - 3000
            if "english-answer" not in rashid_response[rashid_i]["doc"].keys():
                print(rashid_response[rashid_i]["doc"]["index"])
            # for other_character_i in range(0, len(all_obj)):

                # if "index" in all_obj[other_character_i]["doc"].keys():
                #     other_character_index = all_obj[other_character_i]["doc"]["index"]-1000
                #     if other_character_index == rashid_index:
                #         english_question = all_obj[other_character_i]["doc"]["english-question"]
                #         english_answer = all_obj[other_character_i]["doc"]["english-answer"]
                #         rashid_response[rashid_i]["doc"]["english-question"] = english_question
                #         rashid_response[rashid_i]["doc"]["english-answer"] = english_answer

                        # print(all_obj[other_character_i]["doc"]["english-answer"])

    #open('rashid_with_english.json', 'w', encoding='utf-8').write(json.dumps(rashid_response,sort_keys=True,indent=4,separators=(',', ': ')))


add_english_entries()
