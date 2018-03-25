import json

f= open("all_characters.json", "r")

fw= open('all_characters-new.json', 'w')

resp = json.load(f)

data= ' "language": "English" , '



for i in range (0, len(resp["rows"])-1, 1):
    if("question" in resp["rows"][i]["doc"].keys()):
        resp["rows"][i]["doc"]["language"]= "English"

json.dump(resp, fw)

#f.close()