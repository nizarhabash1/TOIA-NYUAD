import json
import unicodedata
import codecs

data=json.load(open('gabriela1.json', 'r', encoding='utf-8'))

for i in range(0, len(data["rows"])):
	data["rows"][i]["doc"]["playing frequency"]= "multiple"
	data["rows"][i]["doc"]["minimum required accuracy"]= "low"
	data["rows"][i]["doc"]["length constant"]= "40"


with open('gabriela2.json',"w") as outfile:
    json_data = json.dumps(data)
    outfile.write(json_data)

f = open("gabriela2.json", "r")

resp = json.load(f)

with codecs.open('gabriela-final.json', 'w', encoding='utf-8') as json_file:
    json.dump(resp, json_file, ensure_ascii=False,indent=4)

f.close()