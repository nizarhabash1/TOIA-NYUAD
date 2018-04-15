import dialogue_manager4
import os
import random
from random_words import RandomWords


characterModel = {}
currentAvatar = ""
currentSession = None

def initiate():
	global currentSession
	global characterModel
	# initiates the model and a new session
	currentSession = dialogue_manager4.createModel(characterModel, currentSession, "English")

def noisify(inputString, percentage, noiseType):
	rw = RandomWords()
	queryList= [tmp.strip(', " ?.!') for tmp in inputString.lower().split()]
	queryLength = len(queryList)
	changes = round(percentage * queryLength/100)
	
	#replacing	
	if noiseType == "replace":
		indexReplaced = []
		for i in range(changes):
			index = 0
			while (True):
				randomWord = rw.random_word()
				index = random.randint(0,queryLength-1)
				if (index not in indexReplaced):
					print(index)
					indexReplaced.append(index)
					break
			queryList[index] = randomWord
		return " ".join(queryList)
	
	#dropping
	else:
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
			if index not in indexDeleted:
				newList.append(queryList[index])
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
				replaced = noisify(question, 50, "drop")
				#print("Question: ",question)
				#print("Replace: ",replaced, "\n")

				answer = characterModel[avatar].objectMap[question_id].answer

				response = dialogue_manager4.findResponse(replaced, characterModel[avatar], currentSession)
				if answer == response.answer or response.question == question:
					correct += 1
					print("Question: ",question)
					print("Replace: ",replaced)
					print("Actual Answer: ",answer)
					print("Response: ",response.answer, "\n")
				else:
					incorrect += 1
					# print("Question: ",question)
					# print("Replace: ",replaced, "\n")
					# print("Actual Answer: ",answer)
					# print("Response: ",response.answer, "\n")

					
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
