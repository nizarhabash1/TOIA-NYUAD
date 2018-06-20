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

source = "20questions.txt"
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
	#f= open('all_characters.json', 'r',encoding = 'utf-8')
	f= open('static/scripts/demo.json', 'r')

	resp = json.load(f)
	for i in range (0, len(resp["rows"]), 1):
		if("question" in resp["rows"][i]["doc"].keys()):
			# remove all the special characters from both questions and answers
			question= json.dumps(resp["rows"][i]["doc"]["question"]).strip(",?.").lower()
			answer= json.dumps(resp["rows"][i]["doc"]["answer"]).strip(",?.").lower()
			video= json.dumps(resp["rows"][i]["doc"]["video"])
			character= json.dumps(resp["rows"][i]["doc"]["video"]).split("_")[0].replace('"', '')
			#do we wanna give it ID ourselves or use the JSON one?
			ID= json.dumps(resp["rows"][i]["doc"]["_id"])


			#print(character)
			obj= videoRecording(question, answer, video, character)

			# Creates the chracter list in the dictionary if it does not exist already
			if character not in characterdict.keys():
				characterdict[character] = []

			#adds to the character list based on the character key
			characterdict[character].append(obj)
			#print(characterdict, i , ID)


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


def direct_intersection_match_Arabic(query, questionArray):
	print("I am trying to match in manager. ")
	maximumSize = 0
	matchedQuestion = ""
	matchedObject = videoRecording(1000, "query", "No response found")
	query.encode('utf-8')
	query.strip('؟')
	for question in questionArray:
		print(question)
		# finds the intersection between the words in query and the set of words in each object's question and answer
		output = "".join(c for c in question if c not in ('!','.',':', '’' , '“', '”', '?'))
		if(isArabic(output)==True):
			question= preprocess(output)

			intersection = intersect(query, question)

			if len(intersection) > maximumSize:
				maximumSize = len(intersection)
			#matchAnswer = obj.answer
			#matchedObject = obj
				matchedQuestion=question
				matches.append(question)

	print(matchedQuestion)
	return matchedQuestion
	exit()

def stem_intersection_match_Arabic(query, questionNum, matches, question_array):
	maximumSize = 0
	matchAnswer = ""
	newQuestion= ""
	matchedObject = videoRecording(1000, "query", "No response found")
	query.encode('utf-8')
	query.strip('؟')

	for obj in questionCorpus:

		# finds the intersection between the words in query and the set of words in each object's question and answer
		intersection=[]
		newQuestion= ""

		splitQuestion= obj.question.split()
		irofile = iter(analysis)
		#print("question: ", splitQuestion)
		for wordq in splitQuestion:
			#print("word: ", wordq)
			irofile = iter(analysis)
			for line in irofile:
				split=line.split()
				print("analysis: ", split)
				for token in range(0, len(split), 1):
					if split[token] == "#WORD:":
						nextLine = next(irofile)
						print("next line: ", nextLine)
						for word in nextLine.split():
							if(word[:4]=="stem" and wordq==split[token+1]):
								newQuestion= obj.question.replace (wordq,word[4:].strip(':'))
								intersection= intersect(query.split(), newQuestion.split())
								continue

									#print(newQuestion.split())

		'''intersection2= intersect(query.split(), obj.answer.split())
		if(len(intersection1)>0):
			print("q intersection= ", intersection1)
		if(len(intersection2)>0):
			print("a intersection= ", intersection2)
		if (len(intersection1) > len(intersection2)):
			intersection= intersection1
		else:
			intersection= intersection2'''

		if len(intersection) > maximumSize:
			maximumSize = len(intersection)
			matchAnswer = obj.answer
			matchedObject = obj
			matches.append(obj.answer)

	if(len(matchAnswer)!= 0):
		print("This is the  matched answer: ", matchAnswer)
	else:
		print("no answer found")


def direct_intersection_match_English(query, corpus):
	print("Finding Direct Intersection direct_intersection_match")
	maximumSize = 0
	matchedObject = corpus[0]
	queryList = query.split()

	for obj in corpus:
		# finds the intersection between the words in query and the set of words in each object's question and answer
		objectList = obj.question.lower().strip('?."!').rstrip().replace('?','').encode('utf-8').split()
		intersection = intersect(queryList, objectList)

		if len(intersection) > maximumSize:
			maximumSize = len(intersection)
			matchedObject = obj
			#matches.append(question)

	return matchedObject

def exact_match_English(query, corpus):
	print("Finding exact match")
	maximumSize = 0
	matchedObject = corpus[0]
	query = query.lower().strip('."?!')
	print("query is ", query)
	for obj in corpus:
		# finds the intersection between the words in query and the set of words in each object's question and answer
		databaseQuestion = obj.question.lower().strip('?."!').rstrip().replace('?','').encode('utf-8')
		if query == databaseQuestion:
			return obj


def stem_intersection_match_English(query, corpus):
	print("Finding Porter Stemmed Intersection")
	maximumSize = 0
	matchedObject = corpus[0]
	# creates a set of stemmed words in query
	queryStemmedList = [porterStemmer.stem(tmp) for tmp in query.split() ]
	for obj in corpus:
		# creates a set of stemmed words in each object's question and answers
		objStemmedList = [porterStemmer.stem(tmp) for tmp in obj.question.split() ] + [porterStemmer.stem(tmp) for tmp in obj.answer.split() ]
		#finds the intersection between each set and the query
		intersection = set(queryStemmedList) & set(objStemmedList)
		if len(intersection) > maximumSize:
			maximumSize = len(intersection)
			matchedObject = obj

			#print(intersection)
	print("you know you just match with one object")
	print(matchedObject.videoLink)
	return matchedObject

def lemma_intersection_match_English(query, corpus):
	print("Finding Word Net Lemmatizer Intersection")
	maximumSize = 0
	matchedObject = corpus[0]
	# creates a set of lemmatized words in query
	queryLemmatizedList = [lemmatizer.lemmatize(tmp) for tmp in query.split() ]
	for obj in corpus:
		# creates a set of lemmatized words in each object's question and answers
		objLemmatizedList = [lemmatizer.lemmatize(tmp) for tmp in obj.question.split() ] + [lemmatizer.lemmatize(tmp) for tmp in obj.answer.split() ]
		#finds the intersection between each set and the query
		intersection = set(queryLemmatizedList) & set(objLemmatizedList)
		if len(intersection) > maximumSize:
			maximumSize = len(intersection)
			matchAnswer = obj.answer
			matchedObject = obj
			print(intersection)
	return matchedObject

def evaluate(questionsNum, matches):
	ratio= matches/questionsNum
	#ratio= str(Fraction(ratio))
	print("ratio of matched questions: ", ratio)


def findResponse(query, corpus):
	# return exact_match_English(query, corpus)
	return direct_intersection_match_English(query, corpus)
	# return stem_intersection_match_English(query, corpus)

def determineAvatar(query, avatar):
	if avatar == "":
		avatar = "katarina"
	#Changes the avatar
	#print("the query you give is " + query )

	query = query.lower();

	if query == "can i talk to margarita":
		avatar = "margarita"

	if query == "can i talk to katarina" or query == "can i talk to katrina" :
		print("you are switching to katarina")
		avatar = "katarina"

	if query == "can i talk to gabriela" or query == "can i talk to gabriella":
		avatar = "gabriela"

	if query == "can I talk to someone else":
		print("you are switching to gabriela")
		avatar = "gabriela"

	return avatar

def main(query, question_array):
	query = query.lower()
	questionsAsked=0
	readFile(sourceFile)
	#while(True):
	#
	#query = input("What do you want to ask Paula?")
	questionsAsked +=1

	print(question_array)
	match = direct_intersection_match_English(query, question_array)
	print("This is match in main: ", match)
	return match
	#evaluate(questionsAsked, len(matches))
	#stem_intersection_match_Arabic(query, questionsAsked, matches)
	#lemma_intersection_match(query)



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main(query, question_array)
