
# -*- coding: utf-8 -*-

'''Libraries
'''


import string
import re
from collections import defaultdict
from fractions import Fraction
import json

import StarMorphModules

import nltk

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


nltk.download('wordnet')
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

'''
Global Variables
'''
porterStemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


# Dictionary of all Avatars
characterdict = {}

#encoding
str.encode('utf-8')

# The Structure for an avatar's model
class model:

	def __init__(self):
		self.stemmedMap = {}
		self.lemmatizedMap = {}
		self.wordMap = {}
		self.objectMap = {}
		self.fillers = {}
		self.greetings = {}

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


#additions to this model: weight assigned to each video if it was played (save the conversation state)

#the structure of the session
class session:

	def __init__(self, avatar):
		self.repetitions = {}
		self.currentAvatar = avatar

#find the intersection of two lists
def intersect(a, b):

	return list(set(a) & set(b))

#preprocessing for Arabic
def preprocess(line):
	processed= line.replace("؟" , "")
	processed= processed.replace("أ" , "ا")
	processed= processed.replace("إ", "ا")
	processed= processed.replace("ى", "ي")
	processed= processed.replace("ة" , "ه")

	return processed

#Initiates the model and create a new session
def createModel(characterdict, currentSession, mylanguage):
	#creates the new session

	currentSession = session('margarita')

	f= open('static/scripts/all_characters.json', 'r', encoding='utf-8')

	resp = json.load(f)

	for i in range (0, len(resp["rows"])-1, 1):

		if("question" in resp["rows"][i]["doc"].keys()):
			# remove all the special characters from both questions and answers
			if(mylanguage== "Arabic" and "arabic-question"in resp["rows"][i]["doc"].keys() and "arabic-answer"in resp["rows"][i]["doc"].keys()):
				question= json.dumps(resp["rows"][i]["doc"]["arabic-question"], ensure_ascii=False).strip("،.؟")
				answer=json.dumps(resp["rows"][i]["doc"]["arabic-answer"],ensure_ascii=False).strip(".؟،")
				#print("answer ",arabic_answer)
			elif(mylanguage=="English"):
				question= json.dumps(resp["rows"][i]["doc"]["question"]).strip(",?.")
				answer= json.dumps(resp["rows"][i]["doc"]["answer"]).strip(",?.")

			video= json.dumps(resp["rows"][i]["doc"]["video"])
			character= json.dumps(resp["rows"][i]["doc"]["video"]).split("_")[0].replace('"', '')
			#do we wanna give it ID ourselves or use the JSON one?
			ID= json.dumps(resp["rows"][i]["doc"]["_id"])
			language= json.dumps(resp["rows"][i]["doc"]["language"])

			#print(character)
			obj= videoRecording(question, answer, video, character, language)

			# Creates the chracter list in the dictionary if it does not exist already
			if character not in characterdict.keys():
				#characterdict[character] is a dictionary of the following lists of videos: silences, greetings, questions
				characterdict[character] = model()

			 	# if the video is for silence
			if (answer == '""' and video != '""'):
			 	characterdict[character].fillers[ID] = obj

			#adds to the character's questions list based on the character key; adds all videos regardless of type to questions
			characterdict[character].objectMap[ID] = obj

			# stemming the question and answer and adding the stems into model.stemmedMap
			if(mylanguage=="English"):
				objStemmedList = [porterStemmer.stem(tmp.strip(' " ?!')) for tmp in question.split() ] + [porterStemmer.stem(tmp) for tmp in obj.answer.split() ]
				#print("stemmed list: ", objStemmedList)
				for stem in objStemmedList:
					# creates a list for objects related to the stem if the list does not exist already
					if stem not in characterdict[character].stemmedMap.keys():
						characterdict[character].stemmedMap[stem] = []

					#adds the question to the list of objects related to the stem
					characterdict[character].stemmedMap[stem].append(ID)

				# lemmatize the question and answer and adding the stems into model.lemmatizedMap
				objLemmatizedList = [lemmatizer.lemmatize(tmp.strip(' " ?!')) for tmp in question.split() ] + [lemmatizer.lemmatize(tmp) for tmp in answer.split() ]
				#print("lemmatized list: ", objLemmatizedList)
				for lemma in objLemmatizedList:
					#print("adding lemmas")
					if lemma not in characterdict[character].lemmatizedMap.keys():
						characterdict[character].lemmatizedMap[lemma] = []

					#adds the question to the list of objects related to the stem
					characterdict[character].lemmatizedMap[lemma].append(ID)

	            # lemmatize the question and answer and adding the stems into model.lemmatizedMap
				objWordList = question.split() + answer.split()
				print("word list: ", objWordList)
				for word in objWordList:
					#print("adding direct words")
					word = word.strip(' " ?!')
					if word not in characterdict[character].wordMap.keys():
						characterdict[character].wordMap[word] = []

					#adds the question to the list of objects related to the stem
					characterdict[character].wordMap[word].append(ID)


			elif(mylanguage=="Arabic"):
					'''
					StarMorphModules.read_config("config_dana.xml")
					StarMorphModules.initialize_from_file("almor-s31.db","analyze")

					objStemmedList= [StarMorphModules.analyze_word(tmp.strip('؟ ، "'),False)[0].split()[1].replace("stem:", "") for tmp in obj.question.split() ] + [StarMorphModules.analyze_word(tmp.strip('؟ ، "'),False)[0].split()[1].replace("stem:", "") for tmp in obj.answer.split() ]
					print("stemmed list: ", objStemmedList)
					for stem in objStemmedList:
						# creates a list for objects related to the stem if the list does not exist already
						if stem not in characterdict[character].stemmedMap.keys():
							characterdict[character].stemmedMap[stem] = []

						#adds the question to the list of objects related to the stem
						characterdict[character].stemmedMap[stem].append(ID)

					#print(analyze)
					objLemmatizedList= [StarMorphModules.analyze_word(tmp.strip('؟ ، "'),False)[0].split()[0].replace("lex:", "").split('_', 1)[0] for tmp in obj.question.split() ] + [StarMorphModules.analyze_word(tmp.strip('؟ ، "'),False)[0].split()[0].replace("lex:", "").split('_', 1)[0] for tmp in obj.answer.split() ]
					print("lemmatized list: ", objLemmatizedList)
					for lemma in objLemmatizedList:
						#print("adding lemmas")
						if lemma not in characterdict[character].lemmatizedMap.keys():
							characterdict[character].lemmatizedMap[lemma] = []

						#adds the question to the list of objects related to the stem
						characterdict[character].lemmatizedMap[lemma].append(ID)'''

		            # lemmatize the question and answer and adding the stems into model.lemmatizedMap
					objWordList = question.split() + answer.split()
					print("word list: ", objWordList)
					for word in objWordList:
						#print("adding direct words")
						word = word.strip(' " ?!')
						if word not in characterdict[character].wordMap.keys():
							characterdict[character].wordMap[word] = []

						#adds the question to the list of objects related to the stem
						characterdict[character].wordMap[word].append(ID)


	return currentSession



def direct_intersection_match_English(query, characterModel):
	print("Finding Direct Intersection in English")
	queryList= query.split()
	responses={}
	maxVal=0
	videoResponse= ''
	#print(characterModel.wordMap.keys())
	for direct_string in queryList:
		direct_string == direct_string.strip(' " ?!').lower()
		if direct_string in characterModel.wordMap.keys():
			for vidResponse in characterModel.wordMap[direct_string]:
				if vidResponse not in responses.keys():
					responses[vidResponse]= 1
				elif vidResponse in responses.keys():
					responses[vidResponse]+=1

		# for key in characterModel.wordMap.keys():
		# 	if direct_string == key.strip(' " ?!').lower():
		# 		for vidResponse in characterModel.wordMap[key]:
		# 			print(videoResponse)
		# 			if vidResponse not in responses.keys():
		# 				responses[vidResponse]= 1
		# 			elif vidResponse in responses.keys():
		# 				responses[vidResponse]+=1


	for key, value in responses.items():
		print(key, value)
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key


	#return characterModel.objectMap[videoResponse]
	return responses



def stem_intersection_match_English(query, characterModel):
	print("Finding Stemmed Intersection Match in English")
	stemmed_query= [porterStemmer.stem(tmp.strip(' " ?!')) for tmp in query.lower().split()]
	#print("stemmed query: ", stemmed_query)
	responses={}
	maxVal=0
	videoResponse= ''
	#print(stemmed_query)
	for stem_string in stemmed_query:
		if stem_string in characterModel.stemmedMap.keys():
			for vidResponse in characterModel.stemmedMap[stem_string]:
				if vidResponse not in responses.keys():
					responses[vidResponse]= 1
				elif vidResponse in responses.keys():
					responses[vidResponse]+=1

	# for stem in stemmed_query:
	# 	for key in characterModel.stemmedMap.keys():
	# 		if stem == key.strip(' " ?!').lower():
	# 			for vidResponse in characterdict.stemmedMap[stem]:
	# 				if vidResponse not in responses.keys():
	# 					responses[vidResponse]= 1
	# 				elif vidResponse in responses.keys():
	# 					responses[vidResponse]+=1


	for key, value in responses.items():
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	#return characterModel.objectMap[videoResponse]
	return responses



def lemma_intersection_match_English(query, characterModel):
	print("Finding Lemmatized intersection match in English")

	lemmatized_query= [lemmatizer.lemmatize(tmp.strip(' " ?!')) for tmp in query.lower().split()]
	#print("lemmatized query: ", lemmatized_query)
	responses={}
	maxVal=0
	videoResponse= ''

	for lemma_string in lemmatized_query:
		if lemma_string in characterModel.lemmatizedMap.keys():
			for vidResponse in characterModel.lemmatizedMap[lemma_string]:
				if vidResponse not in responses.keys():
					responses[vidResponse]= 1
				elif vidResponse in responses.keys():
					responses[vidResponse]+=1

	# for lemma in lemmatized_query:
	# 	for key in characterModel.lemmatizedMap.keys():
	# 		if lemma == key.strip(' " ?!').lower():
	# 			for vidResponse in characterdict.lemmatizedMap[lemma]:
	# 				if vidResponse not in responses.keys():
	# 					responses[vidResponse]= 1
	# 				elif vidResponse in responses.keys():
	# 					responses[vidResponse]+=1


	for key, value in responses.items():
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	#return characterModel.objectMap[videoResponse]
	return responses


def direct_intersection_match_Arabic(query, characterdict):
	print("Finding Direct Intersection in Arabic")
	queryList= query.strip('؟').split()
	#queryList.encode('utf-8')

	responses={}
	maxVal=0
	videoResponse= ''


	print(characterdict.wordMap.keys())
	for direct_string in queryList:
		print(direct_string)
		if direct_string in characterdict.wordMap.keys():
			for vidResponse in characterdict.wordMap[direct_string]:
				if vidResponse not in responses.keys():
					responses[vidResponse]= 0
				elif vidResponse in responses.keys():
					responses[vidResponse]+=1


	for key, value in responses.items():
		print(key, value)
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	#return characterdict[character].objectMap[videoResponse]
	return responses
def stem_intersection_match_Arabic(query, characterdict):

	print("Finding stem Intersection in Arabic")
	queryList = query.strip('؟').split()
	#queryList.encode('utf-8')


	responses={}
	maxVal=0
	videoResponse= ''

	StarMorphModules.read_config("config_stem.xml")
	StarMorphModules.initialize_from_file("almor-s31.db","analyze")

	stemmed_query= ""
	for word in queryList:
		print(word)
		analyzedQuery=StarMorphModules.analyze_word(word,False)
		stemQuery=(analyzedQuery[0].replace("stem:", ""))
		#print(stemQuery)
		stemmed_query+=stemQuery
	print(preprocess(stemmed_query))

	for stem in stemmed_query:
		if stem in characterdict.wordMap.keys():
			for vidResponse in characterdict.wordMap[stem]:
				if vidResponse not in responses.keys():
					responses[vidResponse]= 0
				elif vidResponse in responses.keys():
					responses[vidResponse]+=1

	for key, value in responses.items():
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key
	#return characterdict[character].objectMap[videoResponse]
	return responses

def lemma_intersection_match_Arabic(query, characterdict):

	print("Finding stem Intersection in Arabic")
	queryList = query.strip('؟').split()
	#queryList.encode('utf-8')


	responses={}
	maxVal=0
	videoResponse= ''

	StarMorphModules.read_config("config_lex.xml")
	StarMorphModules.initialize_from_file("almor-s31.db","analyze")


	lemmatized_query= ""
	for word in queryList:
		analyzedQuery=StarMorphModules.analyze_word(word,False)
		#print(analyzedQuery)
		lexQuery=(analyzedQuery[0].replace("lex:", ""))
		lexQuery=lexQuery.strip("1_")
		lemmatized_query+=lexQuery

	print(lemmatized_query)

	for lemma in lemmatized_query:
		if lemma in characterdict.lemmatizedMap.keys():
			for vidResponse in characterdict.lemmatizedMap[lemma]:
				if vidResponse not in responses.keys():
					responses[vidResponse]= 0
				elif vidResponse in responses.keys():
					responses[vidResponse]+=1


	for key, value in responses.items():
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	#return characterdict[character].objectMap[videoResponse]
	print(responses)
	return responses

def rankAnswers(videoResponses, currentSession):
	#each repition is a given a weight of 2 e.g if a video has been played once 2 points will be subtracted from its matching score

	# for each possible answer, checks if it has been played it already, and subtract points from its score if has been played already.
	for res in videoResponses:
		if res in currentSession.repetitions.keys():
			negativePoints = currentSession.repetitions[res] * 2
			videoResponses[res] -= negativePoints

	ranked_list = sorted(videoResponses, key = lambda i:videoResponses[i], reverse = True)
	#print(videoResponses)
	#print(ranked_list)
	# print("Answer's score: ")
	# print(videoResponses[ranked_list[0]])
	# print('\n')
	#print(ranked_list[0])
	return ranked_list[0]

def findResponse(query, characterModel, currentSession):
	themax=0
	best_response=''
	#different modes of matching
	print("My repititions")
	print(currentSession.repetitions)
	'''
	stem_match_english_responses= stem_intersection_match_English(query, characterModel)
	lemma_match_english_responses= lemma_intersection_match_English(query, characterModel)
	direct_match_english_responses= direct_intersection_match_English(query, characterModel)

	#print("stem match: \n",stem_match_english_responses)
	#print("lemma match: \n",lemma_match_english_responses)
	#print("direct match: \n", direct_match_english_responses)
	if(len(stem_match_english_responses)>themax):
		themax= len(stem_match_english_responses)
		best_response=stem_match_english_responses
		print("stem max", themax)

	if(len(lemma_match_english_responses)>themax):
		themax= len(lemma_match_english_responses)
		best_response=lemma_match_english_responses
		print("lemma max", themax)

	if(len(direct_match_english_responses)>themax):
		themax= len(direct_match_english_responses)
		best_response=direct_match_english_responses

		print("direct max", themax)'''


	print("direct max", themax)




	# if the responses are empty, play "I can't answer that response"
	best_response= lemma_intersection_match_Arabic(query, characterModel)
	if bool(best_response) == False:
		if currentSession.currentAvatar == "gabriela":
			final_answer = '"f85983fc8978aa97dec2132b47cff20c"'
		elif currentSession.currentAvatar == "margarita":
			final_answer = '"cc28b6feb31c6d808ca0586a1fd25745"'
		else:
			final_answer = '"ef1374bdef2fc36054292623a39bf9bf"'

	else:
		final_answer = rankAnswers(best_response, currentSession)
		if final_answer in currentSession.repetitions.keys():
			currentSession.repetitions[final_answer] += 1
		else:
			currentSession.repetitions[final_answer] = 1
		print("Number of repetitions: ")
		print(currentSession.repetitions[final_answer])


	print(characterModel.objectMap[final_answer].answer)
	return characterModel.objectMap[final_answer]

	#stem_match_english= stem_intersection_match_English(query, model)
	#lemma_match_english= lemma_intersection_match_English(query, model)

	'''direct_match_arabic= direct_intersection_match_Arabic(query, model)
	stem_match_arabic= stem_intersection_match_Arabic(query, model)
	lemma_match_arabic= lemma_intersection_match_Arabic(query, model)'''

	'''right now we have different modes of matching,
	but we need to change that to getting top 3 matches
	from each mode and getting their intersection
	'''

	#print("This is a direct match in findResponse", direct_match_english)
	#return direct_match_english

def determineAvatar(query, currentSession):
	if currentSession.currentAvatar == "":
		currentSession = session("margarita")

    #Changes the avatar

	if query == "toya toya can i talk to margarita":
		currentSession = session("margarita")

	if query == "toya toya can i talk to katarina":
		print("you are switching to katarina")
		currentSession = session("katarina")

	if query == "toya toya can i talk to gabriela":
		currentSession = session("gabriela")


	if query == "toya toya can i talk to gabriella":
		currentSession = session("gabriela")


	if query == "toya toya can i talk to someone else":
		print("you are switching to gabriela")
		currentSession = session("gabriela")

	return currentSession

# the player calls the following functions for greetings and silentVideos, using calls such as dialogue-manager3.sayHi(characterdict[avatar])

def silentVideos(corpus):
		return corpus["silences"]

def sayHi(corpus):
		return corpus["greetings"][0]

def sayBye(corpus):
		return corpus["greetings"][-1]

def main():
	currentSession = None

	currentSession = createModel(characterdict, currentSession, "Arabic" )
	#print(characterdict["margarita"].lemmatizedMap['speak'])
	while True:
		user_input = input("What do you have to ask\n")
		currentSession = determineAvatar(user_input, currentSession)
		findResponse(user_input, characterdict[currentSession.currentAvatar], currentSession)





if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()
