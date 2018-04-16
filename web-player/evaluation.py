import dialogue_manager4
import os
import random
#from random_words import RandomWords


import StarMorphModules

characterModel = {}
currentAvatar = ""
currentSession = None

#f= open('manual-questions.txt', 'r', encoding='utf-8')

def initiate():
	StarMorphModules.read_config("config_dana.xml")
	StarMorphModules.initialize_from_file("almor-s31.db","analyze")
	global currentSession
	global characterModel
	# initiates the model and a new session


	currentSession = dialogue_manager4.createModel(characterModel, currentSession, "Arabic")

	#currentSession = dialogue_manager4.createModel(characterModel, currentSession, "English")


def noisify(inputString, percentage, noiseType):
	# random word generator
	#rw = RandomWords()
	# breaks the query down to different words
	queryList= [tmp.strip(', " ?.!') for tmp in inputString.lower().split()]

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

def test_oracle_questions():
	global currentSession
	incorrect = 0
	correct = 0
	for avatar in characterModel.keys():
		if avatar == "gabriela" or avatar == "margarita" or avatar == "katarina":
			#print("\n\n\n\n")
			currentSession = dialogue_manager4.create_new_session(avatar)
			for question_id in characterModel[avatar].questionsMap.keys():
				#print(avatar)
				question = characterModel[avatar].objectMap[question_id].question
				noisifiedq= noisify(question, 0.25, "replace")
				print("regular", question)
				print("noisified", noisifiedq)
				
				#print("Question: ",question)

				answer = characterModel[avatar].objectMap[question_id].answer
				

				#response = dialogue_manager4.findResponse(question, characterModel[avatar], currentSession)

				response= dialogue_manager4.findResponse(noisifiedq, characterModel[avatar], currentSession)

				if answer == response.answer or response.question == question:
					correct += 1
					#print("Question: ",question)
					#print("Actual Answer: ",answer)
					#print("Response: ",response.answer, "\n")
				else:
					incorrect += 1

					print("Question: ",question)
					print("Actual Answer: ",answer)
					print("Response: ",response.answer, "\n")

					
	print("correct: ", correct)
	print("incorrect: ", incorrect)

def repeating_question():
	global currentSession
	new_line = False
	for avatar in characterModel.keys():
		mentioned_question = {}
		for question_id in characterModel[avatar].objectMap.keys():
			
			ori_question = characterModel[avatar].objectMap[question_id].question
			
			for tmp_question_id in characterModel[avatar].objectMap.keys():	
				
				tmp_question = characterModel[avatar].objectMap[tmp_question_id].question
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
	
	initiate()
	test_oracle_questions()
	#characterModel["katarina"].objectMap['"cdc6248b097f84b68b97bc341f149911"'].toString()
	#repeating_question()
