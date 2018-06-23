import json
import unicodedata
import codecs

data=json.load(open('margarita2.json', 'r', encoding='utf-8'))

for i in range(0, len(data["rows"])):
	if data["rows"][i]["doc"]["character"]== "katarina":
		data["rows"][i]["doc"]["length constant"]= "20"
	if data["rows"][i]["doc"]["character"]== "margarita":
		data["rows"][i]["doc"]["length constant"]= "40"
	if data["rows"][i]["doc"]["character"]== "rashid":
		data["rows"][i]["doc"]["length constant"]= "20"
	if data["rows"][i]["doc"]["character"]== "gabriela":
		data["rows"][i]["doc"]["length constant"]= "30"

	


with open('margarita3.json',"w") as outfile:
    json_data = json.dumps(data)
    outfile.write(json_data)

f = open("margarita3.json", "r")

resp = json.load(f)

with codecs.open('margarita-final.json', 'w', encoding='utf-8') as json_file:
    json.dump(resp, json_file, ensure_ascii=False,indent=4)

f.close()