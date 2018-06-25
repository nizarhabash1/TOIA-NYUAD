import StarMorphModules
import json

StarMorphModules.read_config("config_dana.xml")
StarMorphModules.initialize_from_file("almor-s31.db","analyze")
'''
f= open("katarina-answers-arabic.txt", "r")

for line in f:
	for word in line.split():
		#word=word.strip('"؟ ،')
		print(word)
		analysis=StarMorphModules.analyze_word(word,False)
		if( analysis != None and len(analysis)>1):
			print("stem", analysis[1].split()[1].replace("stem:", ""))
			print("lemma",analysis[0].split()[0].replace("lex:", "").split('_', 1)[0])
'''

data = []
with open('static/scripts/all_characters.json', encoding="utf-8") as f:
    for line in f:
        data.append(json.loads(line))
print(data)

#The Structure for a video Object
class videoRecording:
	def __init__(self, question, answer, video, character, language):

		self.character = character
		self.question = question
		self.answer = answer
		self.videoLink = video
		self.language= language


	def toString(self):
		print(self.id, ": ", self.character, "\n",self.question,"\n", self.answer, "\n", self.language, "\n")

f= open('static/scripts/all_characters.json', 'r', encoding='utf-8')

f1= open('arabic-script.txt', 'w', encoding='utf-8')
resp = json.load(f)


for i in range (0, len(resp["rows"])-1, 1):
		#print(resp['rows'][i])
	if("question" in resp["rows"][i]["doc"].keys()):
		# remove all the special characters from both questions and answers
		if("arabic-question"in resp["rows"][i]["doc"].keys() and "arabic-answer"in resp["rows"][i]["doc"].keys()):
			question= json.dumps(resp["rows"][i]["doc"]["arabic-question"], ensure_ascii=False).strip("،.؟")
			question_str= str(question)
			f1.write(question_str)
			
		'''for tmp in question_str.split():
				tmp = tmp.strip('؟ ، "')
				analysis=StarMorphModules.analyze_word(tmp,False)
				#print(analysis)'''
		answer=json.dumps(resp["rows"][i]["doc"]["arabic-answer"],ensure_ascii=False).strip(".؟،")
		
		'''
		elif(mylanguage=="English"):
			question= json.dumps(resp["rows"][i]["doc"]["question"]).strip(",?.")
			answer= json.dumps(resp["rows"][i]["doc"]["answer"]).strip(",?.")'''

		video= json.dumps(resp["rows"][i]["doc"]["video"])
		character= json.dumps(resp["rows"][i]["doc"]["video"]).split("_")[0].replace('"', '')
		#do we wanna give it ID ourselves or use the JSON one?
		ID= json.dumps(resp["rows"][i]["doc"]["_id"])
		language= json.dumps(resp["rows"][i]["doc"]["language"])

		#print(character)
		obj= videoRecording(question, answer, video, character, language)

		'''

		# Creates the chracter list in the dictionary if it does not exist already
		if character not in characterdict.keys():
			#characterdict[character] is a dictionary of the following lists of videos: silences, greetings, questions
			characterdict[character] = model()

		 	# if the video is for silence
		if (answer == '""' and video != '""'):
		 	characterdict[character].fillers[ID] = obj

		#adds to the character's questions list based on the character key; adds all videos regardless of type to questions
		characterdict[character].objectMap[ID] = obj'''

		# stemming the question and answer and adding the stems into model.stemmedMap


				
		objLemmatizedList=[]
		objStemmedList=[]
		StarMorphModules.read_config("config_dana.xml")
		StarMorphModules.initialize_from_file("almor-s31.db","analyze")
		#print(obj.question)
		
		for tmp in question.split():
			#print(tmp)
			tmp = tmp.strip('؟ ، "')
			analysis=StarMorphModules.analyze_word(tmp,False)
			#print("stem", analysis[1].split()[1].replace("stem:", ""))
			#print("lemma",analysis[0].split()[0].replace("lex:", "").split('_', 1)[0])

			#objStemmedList.append(analysis[1].split()[1].replace("stem:", ""))
			#objLemmatizedList.append(analysis[0].split()[0].replace("lex:", "").split('_', 1)[0])


		
		for tmp2 in answer.split():
			tmp2 = tmp2.strip('؟ ، "')
			analysis2= StarMorphModules.analyze_word(tmp2.strip('؟ ، "'),False)
			#print("stem", analysis2[1].split()[1].replace("stem:", ""))
			#print("lemma",analysis2[0].split()[0].replace("lex:", "").split('_', 1)[0])




