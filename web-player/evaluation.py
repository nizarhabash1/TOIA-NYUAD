import dialogue_manager4
import os
import random

#from random_words import RandomWords
import json



import StarMorphModules

oracleCharacterDict = {}
automaticCharacterDict = {}
manualCharacterDict = {}
currentAvatar = ""
currentSession = None
#.strip(',?."!')

#f= open('manual-questions.txt', 'r', encoding='utf-8')


def initiate():
	StarMorphModules.read_config("config_dana.xml")
	StarMorphModules.initialize_from_file("almor-s31.db","analyze")
	global currentSession
	global oracleCharacterDict
	# initiates the model and a new session


	currentSession = dialogue_manager4.createModel(oracleCharacterDict, currentSession, "Arabic")
	return currentSession
	
	#currentSession = dialogue_manager4.createModel(characterdict, currentSession, "English")

def preprocess(line):
	processed= line.replace("؟" , "")
	processed= processed.replace("أ" , "ا")
	processed= processed.replace("إ", "ا")
	processed= processed.replace("ى", "ي")
	processed= processed.replace("ة" , "ه")

	return processed
def readManualQuestions(characterdict):
	count = 0
	#f= open('static/scripts/manual_questions.tsv', 'r', encoding='utf-8')
	f= open('static/scripts/manual_questions_arabic.csv', 'r', encoding='utf-8')
	character = 'margarita'
	language = "Arabic"
	video = ""
	characterdict[character] = dialogue_manager4.model()
	lines = f.readlines()
	del lines[0]


	for line in lines:
		#line_split = line.split("\t")
		count = count + 1
		#print(count)
		line_split = line.split(",")
		#print(line_split)
		if line_split[2] != "":

			question1 = line_split[2].strip(',?."!')
			question2 = line_split[3].strip(',?."!')
			question3 = line_split[4].strip(',?."!')
			answer = line_split[1].strip(',?."!')
			

			obj_1= dialogue_manager4.videoRecording(question1, answer, video, character, language)
			obj_2= dialogue_manager4.videoRecording(question2, answer, video, character, language)
			obj_3= dialogue_manager4.videoRecording(question3, answer, video, character, language)
			characterdict[character].questionsMap[count + 1] = obj_1
			characterdict[character].questionsMap[count + 2] = obj_2
			characterdict[character].questionsMap[count + 3] = obj_3
			count = count + 3

			#print(line_split)
			#print(line)'''

def readAutomaticQuestions(characterdict):

	f= open('static/scripts/automatic_questions.json', 'r', encoding='utf-8')

	resp = json.load(f)
	#print(resp)

	totalQuestions = 0

	for i in range (0, len(resp["rows"])-1, 1):

		# Depending on the language, the question is parsed
		id_count=0

	for i in range (0, len(resp["rows"])-1, 1):
			
			id_count+=1

			# If object is a queastion-answer pair, the relevant information is extracted
			if "question" in resp["rows"][i]["doc"].keys():
				totalQuestions +=1
				#do we wanna give it ID ourselves or use the JSON one?
				#ID= json.dumps(resp["rows"][i]["doc"]["_id"])
				video= json.dumps(resp["rows"][i]["doc"]["video"])
				#character= json.dumps(resp["rows"][i]["doc"]["character"])
				character= json.dumps(resp["rows"][i]["doc"]["video"]).split("_")[0].replace('"', '')
				language= "English"
				ID= id_count;
			
			else:
				continue

			
			question= json.dumps(resp["rows"][i]["doc"]["question"]).strip(',?."!)')
			answer= json.dumps(resp["rows"][i]["doc"]["answer"]).strip(',?."!)')

			# Creates a new character model in the character dictionary if it does not exist already
			if character not in characterdict.keys():				
				#characterdict[character] is the model of the respective character
				characterdict[character] = dialogue_manager4.model()

			#adds to the character's questions list based on the character key; adds all videos regardless of type to questions
			obj= dialogue_manager4.videoRecording(question, answer, video, character, language)
			characterdict[character].objectMap[ID] = obj
			
			# if the video is for silence
			if (answer == '""' and video != '""'):
			 	characterdict[character].fillers[ID] = obj

			else:
				characterdict[character].questionsMap[ID] = obj

			

			
	print("Total Questions: ", str(totalQuestions))
	print("done")


def noisify(inputString, percentage, noiseType):
	# random word generator
	#rw = RandomWords()
	# breaks the query down to different words



	queryList= [tmp.strip(', " ?.!)') for tmp in inputString.lower().split()]

	queryLength = len(queryList)

	#the number of words in the inputString which will be changed based on the percentage
	#changes = round(percentage * queryLength/100)
	changes= round((1/4)*queryLength)
	#print(changes)	
	# if noise is added by replacing the words in the original query with random words
	if noiseType == "replace":
		#keeps track of all the indexes of words which are replaced to make sure that the same index is not replaced more than once
		indexReplaced = []

		for i in range(changes):
			randomWord= "مرحبا"
			#randomWord = rw.random_word()
			index = 0
			# runs until an index is identified which has not been changed yet
			while (True):
				index = random.randint(0,queryLength-1)
				#checks if the index has already been replaced
				if (index not in indexReplaced):
					indexReplaced.append(index)
					break
			#the word at the index is replaced by the new random word
			queryList[index] = randomWord
		#joins the noisified query back into a string
		return " ".join(queryList)
	
	#dropping
	else:
		#keeps track of all the indexes of words which are to be removed. Makes sure that the same word is not dropped more than once
		indexDeleted = []
		for i in range(changes):
			index = 0
			while (True):
				index = random.randint(0,queryLength-1)
				
				#makes sure that the same index
				if (index not in indexDeleted):
					indexDeleted.append(index)
					break
		newList = []
		for index in range(queryLength):
			#skips the words at the indexes which are to be dropped
			if index not in indexDeleted:
				newList.append(queryList[index])
		#retuns the noisified query with the changed words.

		return " ".join(newList)		

def test_questions(characterdict, language):
	global currentSession
	global oracleCharacterDict
	incorrect = 0
	correct = 0
	for avatar in characterdict.keys():
		print(avatar)
		if avatar == "gabriela" or avatar == "margarita" or avatar == "katarina":
			currentSession = dialogue_manager4.create_new_session(avatar, language)
			for question_id in characterdict[avatar].questionsMap.keys():
				#print(question_id)

				question = characterdict[avatar].questionsMap[question_id].question
				noisifiedq= noisify(question, 0.25, "replace")
				#print("regular", question)
				#print("noisified", noisifiedq)
				
				#print("Question: ",question)

				#answer = characterdict[avatar].questionsMap[question_id].answer
				

				#response = dialogue_manager4.findResponse(question, characterModel[avatar], currentSession)

				#response = dialogue_manager4.findResponse(question, oracleCharacterDict[avatar], currentSession)

				#question = characterdict[avatar].questionsMap[question_id].question
				#replaced = noisify(question, 50, "replace")
				#print("Question: ",question)
				if question != " ":
					answer = characterdict[avatar].questionsMap[question_id].answer


				answer = characterdict[avatar].questionsMap[question_id].answer


				response = dialogue_manager4.findResponse(question, oracleCharacterDict[avatar], currentSession)

				answer_list = [tmp.strip(',?."!)') for tmp in answer.lower().split()]
				response_answer = response.answer
				response_list = [tmp.strip(',?."!)') for tmp in response_answer.lower().split()]
				response_answer = " ".join(response_list).replace("'","")
				response_answer= preprocess(response_answer)
				answer = " ".join(answer_list).replace("’","")
				answer= preprocess(answer)
				response.question= preprocess(response.question)
				question= preprocess(question)
				if(answer == response_answer or response.question == question):
					correct += 1
					#print("Question: ",question)
					#print("Actual Answer: ",answer)
					#print("Response: ",response.answer, "\n")
				else:
					incorrect += 1
					print("Question: ",question)
					print("Actual Answer: ",answer)
					print("Response: ",response.answer, "\n")

					

	print(correct*100/(correct+incorrect))				
	#print("correct: ", correct)
	#print("incorrect: ", incorrect)

def repeating_question(characterdict):
	global currentSession
	new_line = False
	for avatar in characterdict.keys():
		mentioned_question = {}
		for question_id in characterdict[avatar].objectMap.keys():
			
			ori_question = characterdict[avatar].objectMap[question_id].question
			
			for tmp_question_id in characterdict[avatar].objectMap.keys():	
				
				tmp_question = characterdict[avatar].objectMap[tmp_question_id].question
				if tmp_question == ori_question and tmp_question_id != question_id:

					if question_id not in mentioned_question.keys():
						mentioned_question[question_id] = True
						print(question_id)
					if tmp_question_id not in mentioned_question.keys():
						mentioned_question[tmp_question_id] = True
						print(tmp_question_id)
						new_line = True
			
			if new_line:
				print("\n")
				new_line= False

if __name__ == '__main__':
	
	session = initiate()
	#readAutomaticQuestions(automaticCharacterDict)
	#test_questions(oracleCharacterDict, "English")
	test_questions(oracleCharacterDict, "Arabic")
	#test_questions(automaticCharacterDict)
	#readManualQuestions(manualCharacterDict)

	#print(manualCharacterDict["margarita"].objectMap)

	#print(oracleCharacterDict["margarita"].lemmatizedMap.keys())
	#test_questions(manualCharacterDict, "Arabic")


	#characterdict["katarina"].objectMap['"cdc6248b097f84b68b97bc341f149911"'].toString()
	#repeating_question(oracleCharacterDict)
