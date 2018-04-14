
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

	#arabic_txt= open('arabic.txt', 'w', encoding='utf-8')
	arabic_read= open('arabic.txt', 'r', encoding='utf-8')

	resp = json.load(f)

	StarMorphModules.read_config("config_dana.xml")
	StarMorphModules.initialize_from_file("almor-s31.db","analyze")

	totalQuestions = 0

	for i in range (0, len(resp["rows"])-1, 1):

			# Depending on the language, the question is parsed
			if(mylanguage== "Arabic" and "arabic-question"in resp["rows"][i]["doc"].keys() and "arabic-answer"in resp["rows"][i]["doc"].keys()):
				question= json.dumps(resp["rows"][i]["doc"]["arabic-question"], ensure_ascii=False).strip('،.؟"')
				answer=json.dumps(resp["rows"][i]["doc"]["arabic-answer"],ensure_ascii=False).strip('،.؟"')

			
			if(mylanguage=="English" and "question" in resp["rows"][i]["doc"].keys()):
				question= json.dumps(resp["rows"][i]["doc"]["question"]).strip(',?."!')
				answer= json.dumps(resp["rows"][i]["doc"]["answer"]).strip(',?."!')	

			# If object is a queastion-answer pair, the relevant information is extracted
			if "question" in resp["rows"][i]["doc"].keys():
				totalQuestions +=1
				#do we wanna give it ID ourselves or use the JSON one?
				ID= json.dumps(resp["rows"][i]["doc"]["_id"])
				video= json.dumps(resp["rows"][i]["doc"]["video"])
				character= json.dumps(resp["rows"][i]["doc"]["video"]).split("_")[0].replace('"', '')
				language= json.dumps(resp["rows"][i]["doc"]["language"])
				obj= videoRecording(question, answer, video, character, language)

			# Creates a new character model in the character dictionary if it does not exist already
			if character not in characterdict.keys():
				#characterdict[character] is the model of the respective character
				characterdict[character] = model()

			 	# if the video is for silence
			if (answer == '""' and video != '""'):
			 	characterdict[character].fillers[ID] = obj

			#adds to the character's questions list based on the character key; adds all videos regardless of type to questions
			characterdict[character].objectMap[ID] = obj

			# stemming the question and answer and adding the stems into model.stemmedMap
			
			if(mylanguage=="English"):
				objStemmedList = [porterStemmer.stem(tmp.strip(' " ?!')) for tmp in question.split() ] + [porterStemmer.stem(tmp) for tmp in obj.answer.split() ]
				for stem in objStemmedList:
					# creates a list for objects related to the stem if the list does not exist already
					if stem not in characterdict[character].stemmedMap.keys():
						characterdict[character].stemmedMap[stem] = []

					#adds the question to the list of objects related to the stem
					if (ID not in characterdict[character].stemmedMap[stem] ):
						characterdict[character].stemmedMap[stem].append(ID)

				# lemmatize the question and answer and adding the stems into model.lemmatizedMap
				objLemmatizedList = [lemmatizer.lemmatize(tmp.strip(' " ?!')) for tmp in question.split() ] + [lemmatizer.lemmatize(tmp) for tmp in answer.split() ]
				
				for lemma in objLemmatizedList:
					if lemma not in characterdict[character].lemmatizedMap.keys():
						characterdict[character].lemmatizedMap[lemma] = []

					#adds the question to the list of objects related to the stem
					if (ID not in characterdict[character].lemmatizedMap[lemma] ):
						characterdict[character].lemmatizedMap[lemma].append(ID)

	            # lemmatize the question and answer and adding the stems into model.lemmatizedMap
				objWordList = question.split() + answer.split()

				for word in objWordList:

					word = word.strip(' " ?!')
					if word not in characterdict[character].wordMap.keys():
						characterdict[character].wordMap[word] = []

					#adds the question to the list of objects related to the stem
					if (ID not in characterdict[character].wordMap[word] ):
						characterdict[character].wordMap[word].append(ID)
			
			elif(mylanguage=="Arabic"):
				
					try:
						for line in arabic_read:
							objLemmatizedList=[]
							objStemmedList=[]
							objWordList=[]
							for word in line.split(): 
								
								analysis=[StarMorphModules.analyze_word(word,False)] 
								
								objStemmedList.append(analysis[0][0].split()[1].replace("stem:", ""))
								objLemmatizedList.append(analysis[0][0].split()[0].replace("lex:", "").split('_', 1)[0])
								objWordList.append(word)


							for stem in objStemmedList:
							# creates a list for objects related to the stem if the list does not exist already
								if stem not in characterdict[character].stemmedMap.keys():
									characterdict[character].stemmedMap[stem] = []

								#adds the question to the list of objects related to the stem
								characterdict[character].stemmedMap[stem].append(ID)


							for lemma in objLemmatizedList:

								if lemma not in characterdict[character].lemmatizedMap.keys():
									characterdict[character].lemmatizedMap[lemma] = []

								#adds the question to the list of objects related to the stem
								characterdict[character].lemmatizedMap[lemma].append(ID)

							for word in objWordList:

								word = word.strip(' " ?!')
								if word not in characterdict[character].wordMap.keys():
									characterdict[character].wordMap[word] = []

								#adds the question to the list of objects related to the stem
								characterdict[character].wordMap[word].append(ID)

			           
						arabic_read.close()
					except:
						print("file closed")
						break;
				 
					
					'''
					for tmp in obj.question.split():
						#print(tmp)
						tmp = tmp.strip('؟ ، "')
						analysis=StarMorphModules.analyze_word(tmp,False)
						#print("stem", analysis[1].split()[1].replace("stem:", ""))
						#print("lemma",analysis[0].split()[0].replace("lex:", "").split('_', 1)[0])

						objStemmedList.append(analysis[1].split()[1].replace("stem:", ""))
						objLemmatizedList.append(analysis[0].split()[0].replace("lex:", "").split('_', 1)[0])
	

					
					for tmp2 in obj.answer.split():
						tmp2 = tmp2.strip('؟ ، "')
						analysis2= StarMorphModules.analyze_word(tmp2.strip('؟ ، "'),False)
						print("stem", analysis2[1].split()[1].replace("stem:", ""))
						print("lemma",analysis2[0].split()[0].replace("lex:", "").split('_', 1)[0])
						objStemmedList.append(analysis2[1].split()[1].replace("stem:", ""))
						objLemmatizedList.append(analysis2[0].split()[0].replace("lex:", "").split('_', 1)[0])
					

					#print("answer stemmed list: ", objStemmedList)
					#print("answer lemmatized list: ", objLemmatizedList)
					#objStemmedList= [StarMorphModules.analyze_word(tmp.strip('؟ ، "'),False)[1].split()[1].replace("stem:", "") for tmp in obj.question.split() ] + [StarMorphModules.analyze_word(tmp.strip('؟ ، "'),False)[1].split()[1].replace("stem:", "") for tmp in obj.answer.split() ]
					print("stemmed list: ", objStemmedList)'''
				
					
	print("Total Questions: ", str(totalQuestions))
	print("done")
	return currentSession



def direct_intersection_match_English(query, characterModel):

	queryList= query.split()
	responses={}
	maxVal=0
	videoResponse= ''

	for direct_string in queryList:
		direct_string == direct_string.strip(' " ?!').lower()
		if direct_string in characterModel.wordMap.keys():
			for vidResponse in characterModel.wordMap[direct_string]:
				if vidResponse not in responses.keys():
					responses[vidResponse]= 1
				elif vidResponse in responses.keys():
					responses[vidResponse]+=1


	for key, value in responses.items():

		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	return responses



def stem_intersection_match_English(query, characterModel):

	stemmed_query= [porterStemmer.stem(tmp.strip(' " ?!')) for tmp in query.lower().split()]

	responses={}
	maxVal=0
	videoResponse= ''

	for stem_string in stemmed_query:
		if stem_string in characterModel.stemmedMap.keys():
			for vidResponse in characterModel.stemmedMap[stem_string]:
				if vidResponse not in responses.keys():
					responses[vidResponse]= 1
				elif vidResponse in responses.keys():
					responses[vidResponse]+=1

	for key, value in responses.items():
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	return responses



def lemma_intersection_match_English(query, characterModel):

	lemmatized_query= [lemmatizer.lemmatize(tmp.strip(' " ?!')) for tmp in query.lower().split()]

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

	for key, value in responses.items():
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	return responses


def direct_intersection_match_Arabic(query, characterdict):
	print("Finding Direct Intersection in Arabic")
	queryList= query.strip('؟').split()
	#queryList.encode('utf-8')

	responses={}
	maxVal=0
	videoResponse= ''


	#print(characterdict.wordMap.keys())
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

	return responses

def stem_intersection_match_Arabic(query, characterdict):

	StarMorphModules.read_config("config_stem.xml")
	StarMorphModules.initialize_from_file("almor-s31.db","analyze")

	print("Finding stem Intersection in Arabic")
	queryList = query.strip('؟').split()
	responses={}
	maxVal=0
	videoResponse= ''
	stemmed_query= []

	for word in queryList:

		StarMorphModules.read_config("config_stem.xml")
		StarMorphModules.initialize_from_file("almor-s31.db","analyze")
		analysis=StarMorphModules.analyze_word(word,False)		
		stemmed_query.append(analysis[0].split()[1].replace("stem:", ""))

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
	
	return responses

def lemma_intersection_match_Arabic(query, characterdict):

	print("Finding lemma Intersection in Arabic")
	queryList = query.strip('؟').split()
	#queryList.encode('utf-8')


	responses={}
	maxVal=0
	videoResponse= ''

	StarMorphModules.read_config("config_lex.xml")
	StarMorphModules.initialize_from_file("almor-s31.db","analyze")


	lemmatized_query= []
	for word in queryList:
		#print(word)
		StarMorphModules.read_config("config_stem.xml")
		StarMorphModules.initialize_from_file("almor-s31.db","analyze")
		analysis=StarMorphModules.analyze_word(word,False)

		lemmatized_query.append(analysis[0].split()[0].replace("lex:", "").split('_', 1)[0])

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

	return responses

def calculateTFIDF(token, characterModel):
	totalDocs = len(characterModel.objectMap)

def rankAnswers(videoResponses, currentSession):
	#each repition is a given a weight of 2 e.g if a video has been played once 2 points will be subtracted from its matching score

	# for each possible answer, checks if it has been played it already, and subtract points from its score if has been played already.
	for res in videoResponses:
		if res in currentSession.repetitions.keys():
			negativePoints = currentSession.repetitions[res] * 2
			videoResponses[res] -= negativePoints

	ranked_list = sorted(videoResponses, key = lambda i:videoResponses[i], reverse = True)
	return ranked_list[0]

def findResponse(query, characterModel, currentSession):
	themax=0
	best_response=''
	query = query.strip(',?."!')

	#different modes of matching	
	# stem_match_english_responses= stem_intersection_match_English(query, characterModel)
	# lemma_match_english_responses= lemma_intersection_match_English(query, characterModel)
	# direct_match_english_responses= direct_intersection_match_English(query, characterModel)

	# if(len(stem_match_english_responses)>themax):
	# 	themax= len(stem_match_english_responses)
	# 	best_response=stem_match_english_responses
	# 	#print("stem max", themax)

	# if(len(lemma_match_english_responses)>themax):
	# 	themax= len(lemma_match_english_responses)
	# 	best_response=lemma_match_english_responses
	# 	#print("lemma max", themax)

	# if(len(direct_match_english_responses)>themax):
	# 	themax= len(direct_match_english_responses)
	# 	best_response=direct_match_english_responses

		#print("direct max", themax)

	#print("direct max", themax)

	best_response= direct_intersection_match_English(query, characterModel)
	
	# if the responses are empty, play "I can't answer that response"
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

	return characterModel.objectMap[final_answer]


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

def create_new_session(avatar):
	return session(avatar)

def main():
	global characterdict
	global currentSession
	currentSession = None
	currentSession = createModel(characterdict, currentSession, "English" )

	for i in range(4):
		user_input = input("What do you have to ask\n")
		currentSession = determineAvatar(user_input, currentSession)
		response = findResponse(user_input, characterdict[currentSession.currentAvatar], currentSession)
		print(response.answer)

if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()
