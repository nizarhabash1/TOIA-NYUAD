
# -*- coding: utf-8 -*-

'''Libraries
'''


import string
import re
from collections import defaultdict
from fractions import Fraction
import json

#import StarMorphModules

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


#find the intersection of two lists
def intersect(a, b):

	return list(set(a) & set(b))

#preprocessing for Arabic
def preprocess(line):
	processed= line.encode('utf-8').replace("؟" , "")
	processed= processed.replace("أ" , "ا")
	processed= processed.replace("إ", "ا")
	processed= processed.replace("ى", "ي")
	processed= processed.replace("ة" , "ه")

	return processed 

def createModel(characterdict):

	f= open('static/scripts/all_characters.json', 'r')

	resp = json.load(f)

	for i in range (0, len(resp["rows"])-1, 1):

		if("question" in resp["rows"][i]["doc"].keys()):
			# remove all the special characters from both questions and answers
			question= json.dumps(resp["rows"][i]["doc"]["question"]).strip("؟،,?.")
			answer= json.dumps(resp["rows"][i]["doc"]["answer"]).strip("؟،,?.")
			video= json.dumps(resp["rows"][i]["doc"]["video"])
			character= json.dumps(resp["rows"][i]["doc"]["video"]).split("_")[0].replace('"', '')
			#do we wanna give it ID ourselves or use the JSON one?
			ID= json.dumps(resp["rows"][i]["doc"]["_id"])
			#added language to the db
			language=json.dumps(resp["rows"][i]["doc"]["language"])


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

			
			if(language=="English"):
			
				# stemming the question and answer and adding the stems into model.stemmedMap
				objStemmedList = [porterStemmer.stem(tmp) for tmp in question.split() ] + [porterStemmer.stem(tmp) for tmp in obj.answer.split() ]

				for stem in objStemmedList:

					# creates a list for objects related to the stem if the list does not exist already
					if stem not in characterdict[character].stemmedMap.keys():
						characterdict[character].stemmedMap[stem] = []

					#adds the question to the list of objects related to the stem
					characterdict[character].stemmedMap[stem].append(ID)

				# lemmatize the question and answer and adding the stems into model.lemmatizedMap
				objLemmatizedList = [lemmatizer.lemmatize(tmp) for tmp in question.split() ] + [lemmatizer.lemmatize(tmp) for tmp in answer.split() ]

				for lemma in objLemmatizedList:
					if lemma not in characterdict[character].lemmatizedMap.keys():
						characterdict[character].lemmatizedMap[lemma] = []

					#adds the question to the list of objects related to the lemma
					characterdict[character].lemmatizedMap[lemma].append(ID)
		
	            # direct strings
				objWordList = question.split() + answer.split()

				for word in objWordList:
					if word not in characterdict[character].wordMap.keys():
						characterdict[character].wordMap[word] = []

					#adds the question to the list of objects related to the direct word
					characterdict[character].wordMap[word].append(ID)

			'''elif(language=="Arabic"):

				StarMorphModules.read_config("/CALIMA-STAR/Code/StarMorph/config_lex.xml")
				StarMorphModules.initialize_from_file("/CALIMA-STAR/Code/StarMorph/almor-s31.db","analyze")
				objWordList = [preprocess(tmp) for tmp in obj.question.split()]+ [preprocess(tmp) for tmp in obj.question.split()]

				for word in objWordList:
					#direct strings
					if word not in characterdict[character].wordMap.keys():
						characterdict[character].wordMap[word] = []

					#adds the question to the list of objects related to the direct word
					characterdict[character].wordMap[word].append(ID)
					
					#analyze question and answer pair
					analyzed= StarMorphModules.analyze_word(word,False)

					#stemmed version 
					stemList=(analyzed[0].replace("stem:", ""))
					objStemmedList+=" "+stemList

					#lemmatized version
					lemmatizedList=(analyzed[0].replace("lex:", ""))
					lemmatizedList=lemmatizedList.strip("1_")
					objLemmatizedList +=" "+lemmatizedQuery
					

				for stem in objStemmedList:
					# creates a list for objects related to the stem if the list does not exist already
					if stem not in characterdict[character].stemmedMap.keys():
						characterdict[character].stemmedMap[stem] = []

					#adds the question to the list of objects related to the stem
					characterdict[character].stemmedMap[stem].append(ID)

				for lemma in objLemmatizedList:
					if lemma not in characterdict[character].lemmatizedMap.keys():
						characterdict[character].lemmatizedMap[lemma] = []

					#adds the question to the list of objects related to the lemma
					characterdict[character].lemmatizedMap[lemma].append(ID)'''




def direct_intersection_match_English(query, characterdict):
	print("Finding Direct Intersection in English")
	queryList= query.split()
	responses={}
	maxVal=0
	videoResponse= ''


	for direct_string in queryList:
		if direct_string in characterdict.wordMap.keys():
			for vidResponse in characterdict.wordMap[direct_string]:
				print(videoResponse)
				if vidResponse not in responses.keys():
					responseList[vidResponse]= 0
				elif vidResponse in responses.keys():
					responseList[vidResponse]+=1
			

	for key, value in responses.items():
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	
	return characterdict[character].objectMap[videoResponse]



def stem_intersection_match_English(query, characterdict):
	print("Finding Stemmed Intersection Match in English")
	stemmed_query= [porterStemmer.stem(tmp) for tmp in query.split()]
	responses={}
	maxVal=0
	videoResponse= ''

	for stem in stemmed_query:
		if stem in characterdict.stemmedMap.keys():
			for vidResponse in characterdict.stemmedMap[stem]:
				if vidResponse not in responses.keys():
					responseList[vidResponse]= 0
				elif vidResponse in responses.keys():
					responseList[vidResponse]+=1
			

	for key, value in responses.items():
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	return characterdict[character].objectMap[videoResponse]


def lemma_intersection_match_English(query, characterdict):
	print("Finding Lemmatized intersection match in English")
	lemmatized_query= [lemmatizer.lemmatize(tmp) for tmp in query.split()]
	responses={}
	maxVal=0
	videoResponse= ''

	for lemma in lemmatized_query:
		if lemma in characterdict.lemmatizedMap.keys():
			for vidResponse in characterdict.lemmatizedMap[lemma]:
				if vidResponse not in responses.keys():
					responseList[vidResponse]= 0
				elif vidResponse in responses.keys():
					responseList[vidResponse]+=1
			

	for key, value in responses.items():
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	return characterdict[character].objectMap[videoResponse]

def direct_intersection_match_Arabic(query, characterdict):
	print("Finding Direct Intersection in Arabic")
	queryList= query.encode('utf-8').strip('؟').split()
	#queryList.encode('utf-8')

	responses={}
	maxVal=0
	videoResponse= ''

	for direct_string in queryList:
		if direct_string in characterdict.wordMap.keys():
			for vidResponse in characterdict.wordMap[direct_string]:
				if vidResponse not in responses.keys():
					responseList[vidResponse]= 0
				elif vidResponse in responses.keys():
					responseList[vidResponse]+=1
			

	for key, value in responses.items():
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	return characterdict[character].objectMap[videoResponse]
def stem_intersection_match_Arabic(query, characterdict):
	
	print("Finding stem Intersection in Arabic")
	queryList = query.encode('utf-8').strip('؟').split()
	#queryList.encode('utf-8')


	responses={}
	maxVal=0
	videoResponse= ''

	StarMorphModules.read_config("/CALIMA-STAR/Code/StarMorph/config_lex.xml")
	StarMorphModules.initialize_from_file("/CALIMA-STAR/Code/StarMorph/almor-s31.db","analyze")

	output = "".join(c for c in queryList if c not in ('!','.',':', '’' , '“', '”', '?'))
	
	queryList= preprocess(output)

	stemmed_query= ""
	for word in queryList.split():
		analyzedQuery=StarMorphModules.analyze_word(word,False)
		stemQuery=(analyzedQuery[0].replace("stem:", ""))
		stemmed_query+=" "+stemQuery
	print(stemmed_query)

	for stem in stemmed_query:
		if stem in characterdict.stemmedMap.keys():
			for vidResponse in characterdict.stemmedMap[stem]:
				if vidResponse not in responses.keys():
					responseList[vidResponse]= 0
				elif vidResponse in responses.keys():
					responseList[vidResponse]+=1
			

	for key, value in responses.items():
		if int (value) > maxVal:
			maxVal= int(value)
        	videoResponse= key

	return characterdict[character].objectMap[videoResponse]
def lemma_intersection_match_Arabic(query, characterdict):
	
	print("Finding stem Intersection in Arabic")
	queryList = query.encode('utf-8').strip('؟').split()
	#queryList.encode('utf-8')
	

	responses={}
	maxVal=0
	videoResponse= ''

	StarMorphModules.read_config("/CALIMA-STAR/Code/StarMorph/config_lex.xml")
	StarMorphModules.initialize_from_file("/CALIMA-STAR/Code/StarMorph/almor-s31.db","analyze")

	output = "".join(c for c in queryList if c not in ('!','.',':', '’' , '“', '”', '?'))
	queryList= preprocess(output)

	lemmatized_query= ""
	for word in queryList.split():
		analyzedQuery=StarMorphModules.analyze_word(word,False)
		lexQuery=(analyzedQuery[0].replace("lex:", ""))
		lexQuery=lexQuery.strip("1_")
		lemmatized_query+=" "+llexQuery
	
	print(lemmatized_query)

	for lemma in lemmatized_query:
		if lemma in characterdict.lemmatizedMap.keys():
			for vidResponse in characterdict.lemmatizedMap[lemma]:
				if vidResponse not in responses.keys():
					responseList[vidResponse]= 0
				elif vidResponse in responses.keys():
					responseList[vidResponse]+=1
			

	for key, value in responses.items():
		if int (value) > maxVal:
			maxVal= int(value)
			videoResponse= key

	return characterdict[character].objectMap[videoResponse]

def findResponse(query, model):

	#different modes of matching
	direct_match_english= direct_intersection_match_English(query, model)
	#stem_match_english= stem_intersection_match_English(query, model)
	#lemma_match_english= lemma_intersection_match_English(query, model)
	
	'''direct_match_arabic= direct_intersection_match_Arabic(query, model)
	stem_match_arabic= stem_intersection_match_Arabic(query, model)
	lemma_match_arabic= lemma_intersection_match_Arabic(query, model)'''

	'''right now we have different modes of matching, 
	but we need to change that to getting top 3 matches 
	from each mode and getting their intersection 
	'''
	
	print("This is a direct match in findResponse", direct_match_english)
	return direct_match_english

def determineAvatar(query, avatar):
	if avatar == "":
		avatar = "margarita"
        
    #Changes the avatar

	if query == "toya toya can i talk to margarita":
		avatar = "margarita"

	if query == "toya toya can i talk to katarina":
		print("you are switching to katarina")
		avatar = "katarina"

	if query == "toya toya can i talk to gabriela":
		avatar = "gabriela"


	if query == "toya toya can i talk to gabriella":
		avatar = "gabriela"


	if query == "toya toya can i talk to someone else":
		print("you are switching to gabriela")
		avatar = "gabriela"

	return avatar

# the player calls the following functions for greetings and silentVideos, using calls such as dialogue-manager3.sayHi(characterdict[avatar])

def silentVideos(corpus):
		return corpus["silences"]

def sayHi(corpus):
		return corpus["greetings"][0]

def sayBye(corpus):
		return corpus["greetings"][-1]

def main():
	createModel(characterdict)
	print(characterdict["margarita"].lemmatizedMap['speak'])





if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()


