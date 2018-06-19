import json
import unicodedata
import codecs

data=json.load(open('katarina-new.json', 'r', encoding='utf-8'))



for i in range(0, len(data["rows"])):
	if "playing frequency" not in data["rows"][i]["doc"].keys():
		data["rows"][i]["doc"]["playing frequency"]= "multiple"
		print("missing frequency in index", data["rows"][i]["doc"]["index"])

	if "minimum required accuracy" not in data["rows"][i]["doc"].keys():
	 	data["rows"][i]["doc"]["minimum required accuracy"]= "low"
	 	print("missing minimum accuracy in index", data["rows"][i]["doc"]["index"])

	if "length constant" not in data["rows"][i]["doc"].keys():
	 	data["rows"][i]["doc"]["length constant"]= "40"
	 	print("missing length constant in index", data["rows"][i]["doc"]["index"])
	

	if "arabic-question" not in data["rows"][i]["doc"].keys():
		data["rows"][i]["doc"]["arabic-question"]= ""
		print("missing arabic question in index", data["rows"][i]["doc"]["index"])

	if "arabic-answer" not in data["rows"][i]["doc"].keys():
		data["rows"][i]["doc"]["arabic-answer"]= ""
		print("missing arabic answer in index", data["rows"][i]["doc"]["index"])

	if "english-question" not in data["rows"][i]["doc"].keys():
		data["rows"][i]["doc"]["english-question"]= ""
		print("missing English question in index", data["rows"][i]["doc"]["index"])

	if "english-answer" not in data["rows"][i]["doc"].keys():
		data["rows"][i]["doc"]["english-answer"]= ""
		print("missing English answer in index", data["rows"][i]["doc"]["index"])

	if "character" not in data["rows"][i]["doc"].keys():
		data["rows"][i]["doc"]["character"]= ""
		print("missing character in index", data["rows"][i]["doc"]["index"])

	if "language" not in data["rows"][i]["doc"].keys():
		data["rows"][i]["doc"]["language"]= ""
		print("missing language in index", data["rows"][i]["doc"]["index"])

	if "video-type" not in data["rows"][i]["doc"].keys():
		data["rows"][i]["doc"]["video-type"]= ""
		print("missing video type in index", data["rows"][i]["doc"]["index"])

	if "video" not in data["rows"][i]["doc"].keys():
		data["rows"][i]["doc"]["video"]= ""
		print("missing video in index", data["rows"][i]["doc"]["index"])




with open('katarina3.json',"w") as outfile:
    json_data = json.dumps(data)
    outfile.write(json_data)

f = open("katarina3.json", "r")

resp = json.load(f)

with codecs.open('katarina-checked.json', 'w', encoding='utf-8') as json_file:
    json.dump(resp, json_file, ensure_ascii=False,indent=4)

f.close()