# -*- coding: utf-8 -*-

'''
This file takes in three command line arguments:
language: language of interaction you'd like to test (Arabic or English)
avatar: the name of the avatar you're testing
sample file: an excel sheet with the first column as the original
question from the database, the second one as the corresponding answer
from the database, and the next three columns as other questions
that can share the same answer. 

The file prints out the percentage of correct answers

Example: python3 test_set.py English Margarita test_set.tsv


'''

import dialogue_manager
import os
import random

#from random_words import RandomWords
import json
import sys

characterModel = {}
currentAvatar = ""
currentSession = None
counter=0

def preprocess(text):
	text= text.lower().replace("'","").replace("’","").replace("”","").replace(",", "").replace("?", "").replace(".", "")
	return (text)
def readQuestions(mylanguage, avatar, sampleFile):
	correct=0
	incorrect=0
	currentSession = dialogue_manager.create_new_session(avatar, mylanguage)
	dialogue_manager.createModel(characterModel, currentSession, mylanguage, avatar)
	
	count = 0
	f= open(sampleFile, 'r', encoding= 'utf-8')
	language = mylanguage
	video = ""
	
	lines = f.readlines()
	del lines[0]


	for line in lines:

		count = count + 1
		#print(count)
		
		line_split = line.split("\t")

		if line_split[2] != "":

			question1 = line_split[2].strip(',?."!')
			question2 = line_split[3].strip(',?."!')
			question3 = line_split[4].strip(',?."!')
			answer = line_split[1].strip(',?."!')
			count = count + 3


			response1 = dialogue_manager.findResponse(question1, characterModel[avatar], currentSession, counter)
			response2 = dialogue_manager.findResponse(question2, characterModel[avatar], currentSession, counter)
			response3= dialogue_manager.findResponse(question3, characterModel[avatar], currentSession, counter)
			

			if preprocess(response1.answer) == preprocess(answer):
				correct +=1
			if preprocess(response2.answer) == preprocess(answer):
				correct +=1
			if preprocess(response3.answer) == preprocess(answer):
				#print(answer)
				correct +=1
			
	print("correct", correct)
	#print("total", count)
	print("percentage", correct/count)

sampleFile= sys.argv[1]
language= sys.argv[2]
avatarTested= sys.argv[3]

readQuestions(language, avatarTested, sampleFile)


			
