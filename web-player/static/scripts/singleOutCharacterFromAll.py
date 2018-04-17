# -*- coding: UTF-8 -*-

import subprocess
import json
import os
import math
import sys


# The function singles out a character from multiple other characters


def single_out_character():
    f= open('all_with_rashid.json', 'r', encoding="utf-8")

    resp = json.load(f)
    obj = resp["rows"]
    arr = []
    for i in range(0, len(obj)):
        if "character" in obj[i]["doc"].keys():
            index_number = obj[i]["doc"]["index"]
            # If the character is not Rashid
            if index_number < 3000:
                arr.append(i)
    obj = pop_useless_entries(arr, obj)
    #open("rashid.json", "w",encoding="utf-8").write(json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))


def pop_useless_entries(arr,obj):
    arr.sort(reverse=True)
    for i in arr:
        del obj[i]
    return obj


single_out_character()
