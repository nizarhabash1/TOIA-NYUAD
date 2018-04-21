import json
import StarMorphModules

StarMorphModules.read_config("config_dana.xml")
StarMorphModules.initialize_from_file("almor-s31.db","analyze")

f = open('static/scripts/all_characters.json', 'r', encoding='utf-8')

resp = json.load(f)

glossDict={}
synonymDict={}

for i in range(0, len(resp["rows"]) - 1, 1):
	if ("arabic-question" in resp["rows"][i]["doc"].keys() and "arabic-answer" in resp["rows"][i]["doc"].keys()):
		question = json.dumps(resp["rows"][i]["doc"]["arabic-question"], ensure_ascii=False).strip('،.؟"')
		answer = json.dumps(resp["rows"][i]["doc"]["arabic-answer"], ensure_ascii=False).strip('،.؟"')

		pair= question.split()+answer.split()
		
		for tmp in pair:

			gloss=StarMorphModules.analyze_word(tmp, False)[0].split()[4].split(";")[0].replace("gloss:", "")
			if gloss not in glossDict.keys() and gloss != "NO_ANALYSIS":
				glossDict[gloss]= []
				glossDict[gloss].append(tmp)
			elif gloss in glossDict.keys() and gloss != "NO_ANALYSIS":
				if tmp not in glossDict[gloss]:
					glossDict[gloss].append(tmp)

for key in glossDict.keys():
	if len(glossDict[key])>1:
		for i in glossDict[key]:
			if i not in synonymDict.keys():
				synonymDict[i]=[j for j in glossDict[key]]

print(synonymDict['تعلم'])


