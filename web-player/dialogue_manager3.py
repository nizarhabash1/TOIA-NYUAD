# -*- coding: utf-8 -*-

'''Libraries
'''
import string
import re
from collections import defaultdict
from fractions import Fraction
import json

import nltk
nltk.download('wordnet')
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
'''
Global Variables
'''
analysis= open("static/scripts/arabicQuestions.txt.analysis", "r+")

sourceFile= "static/scripts/arabicQuestions.txt"
matches=[]

questionCorpus = []
porterStemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

#assign encoding for Arabic
str.encode('utf-8')


#create the video object

class videoRecording:
	def __init__(self, question, answer, video, character):

		self.character = character
		self.question = question
		self.answer = answer
		self.videoLink = video

	def toString(self):
		print(self.id, ": ", self.character, "\n",self.question,"\n", self.answer, "\n")

def readJsonFile( characterdict):

	####################################################

	# Structure of Character Dict:
	#characterdict[character] = {"greetings": [], "questions": [], "silences": []}

	####################################################

	#f= open('all_characters.json', 'r',encoding = 'utf-8')
	f= open('static/scripts/all_characters.json', 'r')

	resp = json.load(f)
	for i in range (0, len(resp["rows"])-1, 1):
		if("question" in resp["rows"][i]["doc"].keys()):
			# remove all the special characters from both questions and answers
			question= json.dumps(resp["rows"][i]["doc"]["question"]).strip(",?.")
			answer= json.dumps(resp["rows"][i]["doc"]["answer"]).strip(",?.")
			video= json.dumps(resp["rows"][i]["doc"]["video"])
			character= json.dumps(resp["rows"][i]["doc"]["video"]).split("_")[0].replace('"', '')
			#do we wanna give it ID ourselves or use the JSON one?
			ID= json.dumps(resp["rows"][i]["doc"]["_id"])


			#print(character)
			obj= videoRecording(question, answer, video, character)

			# Creates the chracter list in the dictionary if it does not exist already
			if character not in characterdict.keys():
				#characterdict[character] is a dictionary of the following lists of videos: silences, greetings, questions
			 	characterdict[character] = {}
			 	characterdict[character]["silences"] = []
			 	characterdict[character]["greetings"] = []
			 	characterdict[character]["questions"] = []

			 	# if the video is for silence
			if (answer == '""' and video != '""'):
			 	characterdict[character]["silences"].append(obj)

			#adds to the character's questions list based on the character key; adds all videos regardless of type to questions
			characterdict[character]["questions"].append(obj)
    # adding the list of greeting videos to the characterdict[chracter] dictionary
	for key in characterdict.keys():
		characterdict[key]["greetings"].append(characterdict[key]["questions"][0])
		characterdict[key]["greetings"].append(characterdict[key]["questions"][-1])

def readFile(fileName):

	f= open(sourceFile, "r+", encoding='utf8')

	lines= f.readlines()

	question = ""
	answer = ""
	count = 0

	lineCounter=0;

	for line in lines:
		output = "".join(c for c in line if c not in ('!','.',':', '’' , '“', '”', '?'))
		if (lineCounter%2==0):
			if(isArabic(output)==True):
				question= preprocess(output)


		else:
			count = count + 1
			answer = output[:-2].lower()
			#adds the newly created object in the qestions corput
			questionCorpus.append(videoRecording(count, question, answer))

		lineCounter+=1;



def intersect(a, b):

    return list(set(a) & set(b))


def preprocess(line):
	processed= line.replace("؟" , "")
	processed= processed.replace("أ" , "ا")
	processed= processed.replace("إ", "ا")
	processed= processed.replace("ى", "ي")
	processed= processed.replace("ة" , "ه")

	return processed

def isArabic(line):

	for string in line:
		for char in string:
			if ord(u'\u0600') <= ord(char) <= ord(u'\u0669'):
				return True
			else:
				return False


def direct_intersection_match_Arabic(query, corpus):
	print("Finding Direct Intersection in Arabic")
	maximumSize = 0
	matchedObject = corpus[0]
	queryList = query.split()
	queryList.encode('utf-8')
	queryList.strip('؟')

	for obj in corpus:
		# finds the intersection between the words in query and the set of words in each object's question and answer
		objectList = obj.question.split()
		output = "".join(c for c in objectList if c not in ('!','.',':', '’' , '“', '”', '؟'))
		if(isArabic(output)==True):
			objectList= preprocess(output)

		intersection = intersect(queryList, objectList)

		if len(intersection) > maximumSize:
			maximumSize = len(intersection)
			matchedObject = obj


	return matchedObject


def stem_intersection_match_Arabic(query, corpus):

	print("Finding stem Intersection in Arabic")
	maximumSize = 0
	matchedObject = corpus[0]
	queryList = query.split()
	queryList.encode('utf-8')
	queryList.strip('؟')

	#StarMorphModules.read_config("/Users/student/Desktop/Senior year/Capstone/January 2017/CALIMA-STAR/Code/StarMorph/config_stem.xml")
	#StarMorphModules.initialize_from_file("/Users/student/Desktop/Senior year/Capstone/January 2017/CALIMA-STAR/Code/StarMorph/almor-s31.db","analyze")

	output = "".join(c for c in queryList if c not in ('!','.',':', '’' , '“', '”', '?'))
	if(isArabic(output)==True):
		queryList= preprocess(output)

	stemmedQuery= ""
	for word in queryList.split():
		analyzedQuery=StarMorphModules.analyze_word(word,False)
		stemQuery=(analyzedQuery[0].replace("stem:", ""))
		stemmedQuery+=" "+stemQuery
	print(stemmedQuery)

	for obj in corpus:
		# finds the intersection between the words in query and the set of words in each object's question and answer
		objectList = obj.question.split()
		output = "".join(c for c in objectList if c not in ('!','.',':', '’' , '“', '”', '؟'))
		if(isArabic(output)==True):
			objectList= preprocess(output)

		for word in objectList:
			analyzedQuestion= StarMorphModules.analyze_word(word,False)
			stemQuestion=(analyzedQuestion[0].replace("stem:", ""))
			stemmedQuestion+=" "+stemQuestion

		intersection = intersect(stemmedQuery, stemmedQuestion)

		if len(intersection) > maximumSize:
			maximumSize = len(intersection)
			matchedObject = obj


	return matchedObject

def lemma_intersection_match_Arabic(query, corpus):
	print("Finding lemma Intersection in Arabic")
	maximumSize = 0
	matchedObject = corpus[0]
	queryList = query.split()
	queryList.encode('utf-8')
	queryList.strip('؟')

	# Muaz or Dana update these lines?
	StarMorphModules.read_config("/Users/student/Desktop/Senior year/Capstone/January 2017/CALIMA-STAR/Code/StarMorph/config_lex.xml")
	StarMorphModules.initialize_from_file("/Users/student/Desktop/Senior year/Capstone/January 2017/CALIMA-STAR/Code/StarMorph/almor-s31.db","analyze")

	output = "".join(c for c in queryList if c not in ('!','.',':', '’' , '“', '”', '?'))
	if(isArabic(output)==True):
			queryList= preprocess(output)

	lexQuery= ""

	for obj in corpus:
		objectList = obj.question.split()
		output = "".join(c for c in objectList if c not in ('!','.',':', '’' , '“', '”', '؟'))

		if(isArabic(output)==True):
			objectList= preprocess(output)

		for word in objectList:
			analyzedQuery=StarMorphModules.analyze_word(word,False)
			lemmatizedQuery=(analyzedQuery[0].replace("lex:", ""))
			lemmatizedQuery=lemmatizedQuery.strip("1_")
			lexQuery+=" "+lemmatizedQuery

		intersection = intersect(stemmedQuery, stemmedQuestion)

		if len(intersection) > maximumSize:
			maximumSize = len(intersection)
			matchedObject = obj


	return matchedObject

def direct_intersection_match_English(query, corpus):
	print("Finding Direct Intersection direct_intersection_match")
	maximumSize = 0
	nextMax=0
	matchedObject = corpus[0]
	secondMatchedObject= corpus[0]
	thirdMatchedObject= corpus[0]
	matches={}
	intersectionList=[]
	queryList = query.split()


	for obj in corpus:
		# finds the intersection between the words in query and the set of words in each object's question and answer
		objectList = obj.question.split()
		intersection = intersect(queryList, objectList)
		if len(intersection)>0:
			matches[obj]= len(intersection);
			if len(intersection)>maximumSize:
				print(intersection)
				maximumSize= len(intersection)
				matchedObject= obj


		for k in sorted(matches, key= lambda k: matches[k], reverse=True):
				diff=maximumSize-matches[k]
				if (diff==0):
					matchedObject=k
				elif (diff==1):
					secondMatchedObject=k
				elif (diff==2):
					thirdMatchedObject=k

	print("Query: ", query)
	print("first match:", matchedObject.question)
	print("second match:",secondMatchedObject.question)
	print("third match:",thirdMatchedObject.question)



	return matchedObject



def stem_intersection_match_English(query, corpus):
	print("Finding Porter Stemmed Intersection")
	maximumSize = 0
	nextMax=0
	matchedObject = corpus[0]
	secondMatchedObject= corpus[0]
	thirdMatchedObject= corpus[0]
	matches={}
	intersectionList=[]
	# creates a set of stemmed words in query
	queryStemmedList = [porterStemmer.stem(tmp) for tmp in query.split() ]
	for obj in corpus:
		# creates a set of stemmed words in each object's question and answers
		objStemmedList = [porterStemmer.stem(tmp) for tmp in obj.question.split() ] + [porterStemmer.stem(tmp) for tmp in obj.answer.split() ]
		#finds the intersection between each set and the query
		intersection = set(queryStemmedList) & set(objStemmedList)


		if len(intersection)>0:
			matches[obj]= len(intersection);
			if len(intersection) > maximumSize:
				maximumSize = len(intersection)
				matchedObject = obj

		for k in sorted(matches, key= lambda k: matches[k], reverse=True):
				diff=maximumSize-matches[k]
				if (diff==0):
					matchedObject=k
				elif (diff==1):
					secondMatchedObject=k
				elif (diff==2):
					thirdMatchedObject=k

	print("first match:", matchedObject.question)
	print("second match:",secondMatchedObject.question)
	print("third match:",thirdMatchedObject.question)

	return matchedObject

def lemma_intersection_match_English(query, corpus):
	print("Finding Word Net Lemmatizer Intersection")
	maximumSize = 0
	nextMax=0
	matchedObject = corpus[0]
	secondMatchedObject= corpus[0]
	thirdMatchedObject= corpus[0]
	matches={}
	intersectionList=[]
	# creates a set of lemmatized words in query
	queryLemmatizedList = [lemmatizer.lemmatize(tmp) for tmp in query.split() ]
	for obj in corpus:
		# creates a set of lemmatized words in each object's question and answers
		objLemmatizedList = [lemmatizer.lemmatize(tmp) for tmp in obj.question.split() ] + [lemmatizer.lemmatize(tmp) for tmp in obj.answer.split() ]
		#finds the intersection between each set and the query
		intersection = set(queryLemmatizedList) & set(objLemmatizedList)
		if len(intersection>0):
			matches[obj]= len(intersection);
			if len(intersection) > maximumSize:
				maximumSize = len(intersection)
				matchedObject = obj

		for k in sorted(matches, key= lambda k: matches[k], reverse=True):
				diff=maximumSize-matches[k]
				if (diff==0):
					matchedObject=k
				elif (diff==1):
					secondMatchedObject=k
				elif (diff==2):
					thirdMatchedObject=k

		print("first match:", matchedObject.question)
		print("second match:",secondMatchedObject.question)
		print("third match:",thirdMatchedObject.question)
	return matchedObject

def evaluate(questionsNum, matches):
	ratio= matches/questionsNum
	#ratio= str(Fraction(ratio))
	print("ratio of matched questions: ", ratio)


def findResponse(query, corpus):
	#return direct_intersection_match_English(query, corpus)
	return direct_intersection_match_English(query, corpus["questions"])

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

def main(query, question):
	questionsAsked=0
	readFile(sourceFile)
	#while(True):
	#
	#query = input("What do you want to ask Paula?")
	questionsAsked +=1

	print(question_array)


	#evaluate(questionsAsked, len(matches))
	#stem_intersection_match_Arabic(query, questionsAsked, matches)
	#lemma_intersection_match(query)



if __name__ == "__main__":
	""" This is executed when run from the command line """
	main(query, question_array)
