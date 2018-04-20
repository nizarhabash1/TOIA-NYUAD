# -*- coding: utf-8 -*-

# This file modifies the read and setting of json files so
# the json file displays in Arabic form instead of unicode

import json
import codecs

f = open("all_characters.json", "r")

resp = json.load(f)

with codecs.open('all_characters-new.json','w',encoding='utf-8') as json_file:
    json.dump(resp, json_file, ensure_ascii=False)

f.close()
