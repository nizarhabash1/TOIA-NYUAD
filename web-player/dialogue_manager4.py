
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
		self.questionsMap ={}

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
	#print(resp)

	#StarMorphModules.read_config("config_dana.xml")
	#StarMorphModules.initialize_from_file("almor-s31.db","analyze")

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
				language= json.dumps(resp["rows"][i]["doc"]["language"])
				ID= id_count;
			
			else:
				continue
			
			if(mylanguage== "Arabic" and "arabic-question"in resp["rows"][i]["doc"].keys() and "arabic-answer"in resp["rows"][i]["doc"].keys()):
				question= json.dumps(resp["rows"][i]["doc"]["arabic-question"], ensure_ascii=False).strip('،.؟"')
				answer=json.dumps(resp["rows"][i]["doc"]["arabic-answer"],ensure_ascii=False).strip('،.؟"')

			
			if(mylanguage=="English" and "question" in resp["rows"][i]["doc"].keys()):
				question= json.dumps(resp["rows"][i]["doc"]["question"]).strip(',?."!')
				answer= json.dumps(resp["rows"][i]["doc"]["answer"]).strip(',?."!')

			# Creates a new character model in the character dictionary if it does not exist already
			if character not in characterdict.keys():				
				#characterdict[character] is the model of the respective character
				characterdict[character] = model()

			#adds to the character's questions list based on the character key; adds all videos regardless of type to questions
			obj= videoRecording(question, answer, video, character, language)
			characterdict[character].objectMap[ID] = obj
			
			# if the video is for silence
			if (answer == '""' and video != '""'):
			 	characterdict[character].fillers[ID] = obj

			else:
				characterdict[character].questionsMap[ID] = obj

			# stemming the question and answer and adding the stems, their bigrams and trigrams into model.stemmedMap			
			if(mylanguage=="English"):
				question = question.lower()
				answer = answer.lower()

				objStemmedList = [porterStemmer.stem(tmp.strip(', " ?.!')) for tmp in question.split() ] + [porterStemmer.stem(tmp.strip(', " ?.!')) for tmp in obj.answer.split() ]
				totalStems = len(objStemmedList)
				
				for i in range(totalStems):

					stem = objStemmedList[i]
					if stem not in characterdict[character].stemmedMap.keys():
						characterdict[character].stemmedMap[stem] = []

					#adds the question to the list of objects related to the stem
					if (ID not in characterdict[character].stemmedMap[stem] ):
						characterdict[character].stemmedMap[stem].append(ID)

					if i < totalStems -1:
						bigram = stem + " " + objStemmedList[i+1]
						if bigram not in characterdict[character].stemmedMap.keys():
							characterdict[character].stemmedMap[bigram] = []

						if (ID not in characterdict[character].stemmedMap[bigram] ):
							characterdict[character].stemmedMap[bigram].append(ID)

					if i < totalStems -2: 
						trigram = stem + " " + objStemmedList[i+1] + " " + objStemmedList[i+2]
						if trigram not in characterdict[character].stemmedMap.keys():
							characterdict[character].stemmedMap[trigram] = []

						if (ID not in characterdict[character].stemmedMap[trigram] ):
							characterdict[character].stemmedMap[trigram].append(ID)


				# lemmatize the question and answer and adding the lemmas, their bigrams and trigramsinto model.lemmatizedMap
				objLemmatizedList = [lemmatizer.lemmatize(tmp.strip(', " ?.!')) for tmp in question.split() ] + [lemmatizer.lemmatize(tmp.strip(', " ?.!')) for tmp in answer.split() ]
				totalLemmas = len(objLemmatizedList)
				
				for i in range(totalLemmas):

					lemma = objLemmatizedList[i]
					if lemma not in characterdict[character].lemmatizedMap.keys():
						characterdict[character].lemmatizedMap[lemma] = []

					#adds the question to the list of objects related to the stem
					if (ID not in characterdict[character].lemmatizedMap[lemma] ):
						characterdict[character].lemmatizedMap[lemma].append(ID)

					if i < totalLemmas -1:
						bigram = lemma + " " + objLemmatizedList[i+1]
						if bigram not in characterdict[character].lemmatizedMap.keys():
							characterdict[character].lemmatizedMap[bigram] = []

						if (ID not in characterdict[character].lemmatizedMap[bigram] ):
							characterdict[character].lemmatizedMap[bigram].append(ID)

					if i < totalLemmas -2: 
						trigram = lemma + " " + objLemmatizedList[i+1] + " " +  objLemmatizedList[i+2]
						if trigram not in characterdict[character].lemmatizedMap.keys():
							characterdict[character].lemmatizedMap[trigram] = []

						if (ID not in characterdict[character].lemmatizedMap[trigram] ):
							characterdict[character].lemmatizedMap[trigram].append(ID)


	            # splitting the question and answer and adding the words, their bigrams and trigrams into model.WordMap
				objWordList = [tmp.strip(', " ?.!') for tmp in question.split()] + [tmp.strip(', " ?.!') for tmp in answer.split()]
				totalWords = len(objWordList)
				
				for i in range(totalWords):

					word = objWordList[i]
					if word not in characterdict[character].wordMap.keys():
						characterdict[character].wordMap[word] = []

					#adds the question to the list of objects related to the stem
					if (ID not in characterdict[character].wordMap[word] ):
						characterdict[character].wordMap[word].append(ID)

					if i < totalWords -1:
						bigram = word + " " + objWordList[i+1]
						if bigram not in characterdict[character].wordMap.keys():
							characterdict[character].wordMap[bigram] = []

						if (ID not in characterdict[character].wordMap[bigram] ):
							characterdict[character].wordMap[bigram].append(ID)

					if i < totalWords -2: 
						trigram = word + " " + objWordList[i+1] +  " " + objWordList[i+2]
						if trigram not in characterdict[character].wordMap.keys():
							characterdict[character].wordMap[trigram] = []

						if (ID not in characterdict[character].wordMap[trigram] ):
							characterdict[character].wordMap[trigram].append(ID)

			
			elif(mylanguage=="Arabic"):

				'''objLemmatizedList=[]
				objStemmedList=[]
				objWordList=[]'''
				#print(StarMorphModules.analyze_word("كيف",False)[0].split()[0].replace("lex:", "").split('_', 1)[0])
				#print(StarMorphModules.analyze_word("كيف",False)[0].split()[1].replace("stem:", "").split('d', 1)[0])
				objStemmedList = [StarMorphModules.analyze_word(tmp,False)[0].split()[1].replace("stem:", "").split('d', 1)[0] for tmp in question.split() ] + [StarMorphModules.analyze_word(tmp,False)[0].split()[1].replace("stem:", "").split('d', 1)[0]for tmp in obj.answer.split() ]


				for stem in objStemmedList:
						#print(stem)
					# creates a list for objects related to the stem if the list does not exist already
						if stem not in characterdict[character].stemmedMap.keys():
							characterdict[character].stemmedMap[stem] = []

						#adds the question to the list of objects related to the stem
						if(ID not in characterdict[character].stemmedMap[stem]): 
							characterdict[character].stemmedMap[stem].append(ID)
					#print(characterdict[character].stemmedMap)
				
				objLemmatizedList = [StarMorphModules.analyze_word(tmp,False)[0].split()[0].replace("lex:", "").split('_', 1)[0] for tmp in question.split() ] + [StarMorphModules.analyze_word(tmp,False)[0].split()[0].replace("lex:", "").split('_', 1)[0] for tmp in obj.answer.split() ]
				
				for lemma in objLemmatizedList:
						lemma=re.sub(r'[^\u0621-\u064A]', '', lemma, flags=re.UNICODE)

						if lemma not in characterdict[character].lemmatizedMap.keys():
							
							characterdict[character].lemmatizedMap[lemma] = []

						#adds the question to the list of objects related to the stem
						#print(ID)
						if(ID not in characterdict[character].lemmatizedMap[lemma]):
							characterdict[character].lemmatizedMap[lemma].append(ID)
						#print("lemma: " + lemma + "\n" )
						#print(characterdict[character].lemmatizedMap[lemma])
						#print("\n")

				objWordList = question.split() + answer.split()

				for word in objWordList:

					word = word.strip(' " ?!')
					if word not in characterdict[character].wordMap.keys():
						characterdict[character].wordMap[word] = []

					#adds the question to the list of objects related to the stem
					characterdict[character].wordMap[word].append(ID)
				#print("word list", characterdict[character].wordMap)
					#print(characterdict[character].lemmatizedMap.keys())
					#print("lemmatized list", characterdict[character].lemmatizedMap)
				'''
					try:
						for line in arabic_read:
							objLemmatizedList=[]
							objStemmedList=[]
							objWordList=[]
							for word in line.split(): 
								word= word.strip('،/')
								analysis=[StarMorphModules.analyze_word(word,False)]
								#print(analysis) 
								
								objStemmedList.append(analysis[0][0].split()[1].replace("stem:", "").split('d', 1)[0])
								objLemmatizedList.append(analysis[0][0].split()[0].replace("lex:", "").split('_', 1)[0])
								objWordList.append(word)


							for stem in objStemmedList:
								#print(character)
								#print(stem)
							# creates a list for objects related to the stem if the list does not exist already
								if stem not in characterdict[character].stemmedMap.keys():
									characterdict[character].stemmedMap[stem] = []

								#adds the question to the list of objects related to the stem
								if(ID not in characterdict[character].stemmedMap[stem]): 
									characterdict[character].stemmedMap[stem].append(ID)
							#print(characterdict[character].stemmedMap)


							for lemma in objLemmatizedList:
								lemma=re.sub(r'[^\u0621-\u064A]', '', lemma, flags=re.UNICODE)

								if lemma not in characterdict[character].lemmatizedMap.keys():
									
									characterdict[character].lemmatizedMap[lemma] = []

								#adds the question to the list of objects related to the stem
								#print(ID)
								if(ID not in characterdict[character].lemmatizedMap[lemma]):
									characterdict[character].lemmatizedMap[lemma].append(ID)
								#print("lemma: " + lemma + "\n" )
								#print(characterdict[character].lemmatizedMap[lemma])
								#print("\n")
							#print(characterdict[character].lemmatizedMap.keys())
							#print("lemmatized list", characterdict[character].lemmatizedMap)


							objWordList = line.split()
							
							for word in objWordList:

								word = word.strip(' ؟.،')
								if word not in characterdict[character].wordMap.keys():
									characterdict[character].wordMap[word] = []

								#adds the question to the list of objects related to the stem
								if(ID not in characterdict[character].wordMap[word]):
									characterdict[character].wordMap[word].append(ID)

								#print("word: " + word + "\n" )
								#print(characterdict[character].wordMap[word])
								#print("\n")
							#print("word list", characterdict[character].wordMap)
			           
						#arabic_read.close()
					except:
						#print("Exception given")
						continue
						#break;

				 	'''
				
	#print("Character: ", character) 
			#print("ID: ", str(id_count))
			#print("Question: ", str(question))
			#print("Answer: ", str(answer))
			#print("\n")


			
	print("Total Questions: ", str(totalQuestions))
	print("done")
	#print(characterdict["gabriela"].wordMap)
	return currentSession



def direct_intersection_match_English(query, characterModel):

	queryList= [tmp.strip(', " ?.!') for tmp in query.split()]
	responses={}
	maxVal=0
	videoResponse= ''

	for direct_string in queryList:
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

	stemmed_query= [porterStemmer.stem(tmp.strip(', " ?.!')) for tmp in query.split()]

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

	lemmatized_query= [lemmatizer.lemmatize(tmp.strip(', " ?.!')) for tmp in query.split()]

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


def direct_intersection_match_Arabic(query, characterModel):
	print("Finding Direct Intersection in Arabic")
	queryList= query.strip('؟').split()
	#queryList.encode('utf-8')

	responses={}
	maxVal=0
	videoResponse= ''

	for direct_string in queryList:
		#print(direct_string)
		if direct_string in characterModel.wordMap.keys():
			for vidResponse in characterModel.wordMap[direct_string]:
				if vidResponse not in responses.keys():
					responses[vidResponse]= 0
				elif vidResponse in responses.keys():
					responses[vidResponse]+=1



	for key, value in responses.items():
		#print(key, value)
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	#print(responses)
	return responses

def stem_intersection_match_Arabic(query, characterModel):

	#StarMorphModules.read_config("config_stem.xml")
	#StarMorphModules.initialize_from_file("almor-s31.db","analyze")

	print("Finding stem Intersection in Arabic")
	queryList = query.strip('؟!،"').split()
	responses={}
	maxVal=0
	videoResponse= ''
	stemmed_query= []

	for word in queryList:

		
		analysis=StarMorphModules.analyze_word(word,False)	

		stemmed_query.append(analysis[0].split()[1].replace("stem:", "").split('d', 1)[0])

	for stem in stemmed_query:

		if stem in characterModel.wordMap.keys():

			for vidResponse in characterModel.wordMap[stem]:

				if vidResponse not in responses.keys():

					responses[vidResponse]= 0
				
				elif vidResponse in responses.keys():

					responses[vidResponse]+=1

	for key, value in responses.items():

		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key
	
	return responses

def lemma_intersection_match_Arabic(query, characterModel):

	print("Finding lemma Intersection in Arabic")
	queryList = query.strip('؟').split()
	#queryList.encode('utf-8')


	responses={}
	maxVal=0
	videoResponse= ''




	lemmatized_query= []
	for word in queryList:
		#print(word)
		analysis=StarMorphModules.analyze_word(word,False)
		lemmatized_query.append(analysis[0].split()[0].replace("lex:", "").split('_', 1)[0])

	

	for lemma in lemmatized_query:
		if lemma in characterModel.lemmatizedMap.keys():
			for vidResponse in characterModel.lemmatizedMap[lemma]:
				if vidResponse not in responses.keys():
					responses[vidResponse]= 0
				elif vidResponse in responses.keys():
					responses[vidResponse]+=1


	for key, value in responses.items():
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	#print(responses)
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
	
	#StarMorphModules.read_config("config_lex.xml")
	#StarMorphModules.initialize_from_file("almor-s31.db","analyze")

	themax=0
	best_response=''
	query = query.lower().strip(',?."!')

	#different modes of matching	
	# stem_match_english_responses= stem_intersection_match_English(query, characterModel)
	# lemma_match_english_responses= lemma_intersection_match_English(query, characterModel)
	# direct_match_english_responses= direct_intersection_match_English(query, characterModel)

	# if(len(stem_match_english_responses)>themax):
	# 	themax= len(stem_match_english_responses)
	# 	best_response=stem_match_english_responses

	# 	print("stem max", themax)

	

	# if(len(lemma_match_english_responses)>themax):
	# 	themax= len(lemma_match_english_responses)
	# 	best_response=lemma_match_english_responses

	# 	print("lemma max", themax)



	# if(len(direct_match_english_responses)>themax):
	# 	themax= len(direct_match_english_responses)
	# 	best_response=direct_match_english_responses


	# 	print("direct max", themax)


	best_response= lemma_intersection_match_English(query, characterModel)

	# if the responses are empty, play "I can't answer that response"
	if bool(best_response) == False:
		if currentSession.currentAvatar == "gabriela":
			final_answer = 798
		elif currentSession.currentAvatar == "margarita":
			final_answer = 618
		else:
			final_answer = 746


	else:
		final_answer = rankAnswers(best_response, currentSession)
		if final_answer in currentSession.repetitions.keys():
			currentSession.repetitions[final_answer] += 1
		else:
			currentSession.repetitions[final_answer] = 1

	#print(characterModel.objectMap[final_answer].answer)

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
	currentSession = createModel(characterdict, currentSession, "Arabic" )

	for i in range(4):
		user_input = input("What do you have to ask\n")
		currentSession = determineAvatar(user_input, currentSession)
		response = findResponse(user_input, characterdict[currentSession.currentAvatar], currentSession)
		print(response.answer)

if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()
