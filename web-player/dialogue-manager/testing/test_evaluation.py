import test_dm
import os
import random

#from random_words import RandomWords
import json

import sys



sys.path.insert(0, '../../CalimaStar_files/')


import StarMorphModules

oracleCharacterDict = {}
automaticCharacterDict = {}
manualCharacterDict = {}
currentAvatar = ""
currentSession = None
#.strip(',?."!')

#f= open('manual-questions.txt', 'r', encoding='utf-8')

class test_parameters:
	def __init__(self, unigram_par, bigram_par, trigram_par, tfidf_par, synonym_par, testSet_par, noise_par, automatic_par):
		self.unigram = unigram_par
		self.bigram = bigram_par
		self.trigram = trigram_par
		self.tfidf = tfidf_par
		self.synonym = synonym_par
		self.testSet = testSet_par
		self.noise = noise_par
		self.automatic = automatic_par

	def toString(self):
		tmp = str(self.unigram) + " , " + str(self.bigram) + " , "  + str(self.trigram)  + " , "+ str(self.tfidf) + " , "+ str(self.synonym)   + " , " + self.testSet + " , "+ str(self.noise)  + " , "  +  str(self.automatic)
		return tmp

def run_test(mylanguage, test_par):
	global currentSession
	global oracleCharacterDict

	test_dm.createModel(oracleCharacterDict, currentSession, mylanguage, "margarita", test_par)

	if test_par.testSet == "manual":
		test_results = test_questions(manualCharacterDict, mylanguage, test_par)
		return test_results

	if test_par.testSet == "oracle":
		test_results = test_questions(oracleCharacterDict, mylanguage, test_par)
		return test_results


def test_wrapper(mylanguage):

	unigram_mode = [True]
	bigram_mode = [False]
	trigram_mode = [False]
	synonym_mode = [True, False]
	tfidf_mode = [True, False]
	automatic_mode = [True, False]
	noise_mode = ["None", "replace", "drop"]
	testSet_mode = ["manual", "oracle"]

	#unigram_par, bigram_par, trigram_par, tfidf_par, synonym_par, testSet_par, noise_par, automatic_par)
	#test_par = test_parameters(True, False, False, True, False, "manual", "None", False)
	#test_results = run_test(mylanguage, test_par)
	#print(test_results)

	f = open("test_results_final.csv" , "a")
	count = 1
	f.write("Unigram, Bigram, Trigram, TFIDF, Synonym Expansion, Test Set, Noise, Automatic Questions, Result\n")
	for testSet_par in testSet_mode:
		for unigram_par in unigram_mode:
			for bigram_par in bigram_mode:
				for trigram_par in trigram_mode:
					for synonym_par in synonym_mode:
						for tfidf_par in tfidf_mode:
							for automatic_par in automatic_mode:
								for noise_par in noise_mode:
									count += 1
									test_par = test_parameters(unigram_par, bigram_par, trigram_par, tfidf_par, synonym_par, testSet_par, noise_par, automatic_par)
									initiate(mylanguage)
									test_result = run_test(mylanguage, test_par)
									new_line = test_par.toString() + "," + str(test_result) + "\n"
									f.write(new_line)

	f.close()
def initiate(mylanguage):
	global oracleCharacterDict

	if mylanguage == "Arabic":
		readManualQuestions(manualCharacterDict, "Arabic")

	else:
		readManualQuestions(manualCharacterDict, "English")
	
	# initiates the model and a new session
	#test_dm.createModel(oracleCharacterDict, currentSession, mylanguage, test_par)

def preprocess(line):
	processed= line.replace("؟" , "")
	processed= processed.replace("أ" , "ا")
	processed= processed.replace("إ", "ا")
	processed= processed.replace("ى", "ي")
	processed= processed.replace("ة" , "ه")

	return processed
def readManualQuestions(characterdict, mylanguage):
	count = 0
	#f= open('static/scripts/manual_questions.tsv', 'r', encoding='utf-8')
	if mylanguage == "Arabic":
		f= open('../../static/scripts/miscellaneous/manual_questions_arabic.csv', 'r', encoding='utf-8')
	else:
		f= open('../../static/scripts/miscellaneous/manual_questions.tsv', 'r', encoding='utf-8')
	character = 'margarita'
	language = mylanguage
	video = ""
	characterdict[character] = test_dm.model()
	lines = f.readlines()
	del lines[0]


	for line in lines:

		count = count + 1
		#print(count)
		if mylanguage == "English":
			line_split = line.split("\t")
		if mylanguage == "Arabic":
			line_split = line.split(",")
		#print(line_split)
		if line_split[2] != "":

			question1 = line_split[2].strip(',?."!')
			question2 = line_split[3].strip(',?."!')
			question3 = line_split[4].strip(',?."!')
			answer = line_split[1].strip(',?."!')
			

			obj_1= test_dm.databaseEntry(question1, answer, video, character, language, "multiple")
			obj_2= test_dm.databaseEntry(question2, answer, video, character, language, "multiple")
			obj_3= test_dm.databaseEntry(question3, answer, video, character, language, "multiple")
			characterdict[character].questionsMap[count + 1] = obj_1
			characterdict[character].questionsMap[count + 2] = obj_2
			characterdict[character].questionsMap[count + 3] = obj_3
			count = count + 3

			#print(line_split)
			#print(line)'''

def readAutomaticQuestions(characterdict):

	f= open('../../../static/scripts/miscellaneous/automatic_questions.json', 'r', encoding='utf-8')

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
				ID= id_count
			
			else:
				continue

			
			question= json.dumps(resp["rows"][i]["doc"]["question"]).strip(',?."!)')
			answer= json.dumps(resp["rows"][i]["doc"]["answer"]).strip(',?."!)')

			# Creates a new character model in the character dictionary if it does not exist already
			if character not in characterdict.keys():				
				#characterdict[character] is the model of the respective character
				characterdict[character] = test_dm.model()

			#adds to the character's questions list based on the character key; adds all videos regardless of type to questions
			obj= test_dm.videoRecording(question, answer, video, character, language)
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
			randomWord= "random"
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

def test_questions(characterdict, language, test_par):
	global currentSession
	global oracleCharacterDict
	incorrect = 0
	correct = 0
	counter=0
	questionsAsked=[]
	for avatar in characterdict.keys():
		print(avatar)
		if avatar == "gabriela" or avatar == "margarita" or avatar == "katarina":
			currentSession = test_dm.create_new_session(avatar, language)
			for question_id in characterdict[avatar].questionsMap.keys():

				question = characterdict[avatar].questionsMap[question_id].question

				if question == " ":
					continue
				if question in questionsAsked:
					continue

				answer = characterdict[avatar].questionsMap[question_id].answer

				question_list = [tmp.strip(',?."!)') for tmp in question.lower().split()]
				answer_list = [tmp.strip(',?."!)') for tmp in answer.lower().split()]
				answer = " ".join(answer_list).replace("’","").replace(",", "").replace("'","").replace("”","")
				question = " ".join(question_list).replace("’","").replace(",", "").replace("'","").replace("”","")
				questionsAsked.append(question)

				if (language == "Arabic"):
					question= preprocess(question)
					answer= preprocess(answer)

				if test_par.noise == "replace":
					noisifiedq= noisify(question, 0.25, "replace")

				elif test_par.noise == "drop":
					noisifiedq= noisify(question, 0.25, "drop")
				
				else:
					noisifiedq= question

				#print(noisifiedq)	
				response = test_dm.findResponse(noisifiedq, oracleCharacterDict[avatar], currentSession, test_par, counter)
				
				#print(response.answer)
				response_answer = response.answer
				response_list = [tmp.strip(',?."!)') for tmp in response_answer.lower().split()]
				response_answer = " ".join(response_list).replace("'","").replace("’","").replace(",", "").replace("'","").replace("”","")
				
				if(answer.lower() == response_answer.lower() or response.question.lower() == question.lower()):
					correct += 1
					#print("Question: ",question)
					#print("Actual Answer: ",answer)
					#print("Response: ",response.answer, "\n")
				else:
					incorrect += 1
					print("Question: ",question)
					print("Actual Answer: ",answer)
					print("Response: ",response.answer, "\n")
				counter +=1

					

	percentage_correct  = correct*100/(correct+incorrect)
	return percentage_correct
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
						#print(question_id)
					if tmp_question_id not in mentioned_question.keys():
						mentioned_question[tmp_question_id] = True
						#print(tmp_question_id)
						new_line = True
			
			if new_line:
				#print("\n")
				new_line= False

if __name__ == '__main__':
	#StarMorphModules.read_config("config_dana.xml")
	#StarMorphModules.initialize_from_file("almor-s31.db", "analyze")

	#readManualQuestions(manualCharacterDict, "Arabic")
	initiate("English")
	test_wrapper("English")
	#for character in oracleCharacterDict.keys():
	#print(oracleCharacterDict["rashid"].objectMap)
	#readAutomaticQuestions(automaticCharacterDict)
	#test_questions(oracleCharacterDict, "English")
	#test_questions(oracleCharacterDict, "Arabic")
	#test_questions(automaticCharacterDict)
	#readManualQuestions(manualCharacterDict, "Arabic")

	#print(oracleCharacterDict["margarita"].lemmatizedMap.keys())
	#test_questions(manualCharacterDict, "Arabic")


	#characterdict["katarina"].objectMap['"cdc6248b097f84b68b97bc341f149911"'].toString()
	#repeating_question(oracleCharacterDict)
