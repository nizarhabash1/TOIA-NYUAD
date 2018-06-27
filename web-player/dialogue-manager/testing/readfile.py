# -*- coding: utf-8 -*-


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
def readQuestions(mylanguage, avatar):
	correct=0
	incorrect=0
	currentSession = dialogue_manager.create_new_session(avatar, mylanguage)
	dialogue_manager.createModel(characterModel, currentSession, mylanguage, avatar)
	
	count = 0
	if mylanguage == "Arabic":
		f= open('test-set.csv', 'r', encoding='utf-8')
	else:
		f= open('test-set.tsv', 'r', encoding='utf-8')
		#f= open('static/scripts/manual_questions.tsv', 'r', encoding='utf-8')
	character = 'margarita'
	language = mylanguage
	video = ""
	#characterdict[character] = dialogue_manager.model()
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
			count = count + 3

			# print("question1", question1)
			# print("question2", question2)
			# print("question3", question3)
			# print("answer", answer)

			response1 = dialogue_manager.findResponse(question1, characterModel[avatar], currentSession, counter)
			response2 = dialogue_manager.findResponse(question2, characterModel[avatar], currentSession, counter)
			response3= dialogue_manager.findResponse(question3, characterModel[avatar], currentSession, counter)
			

			if preprocess(response1.answer) == preprocess(answer):
				# print("question1", question1, "\n")
				# print("answer", answer, "\n")
				# print("response1", response1.answer, "\n")
				correct +=1
			if(preprocess(response1.answer) != preprocess(answer)):
				incorrect+=1
				print("question", question1)
				print("actual answer", answer)
				print("response", response1.answer, "\n")
			if preprocess(response2.answer) == preprocess(answer):
				#print(answer)
				correct +=1
			if(preprocess(response2.answer) != preprocess(answer)):
				print("question", question2)
				print("actual answer", answer)
				print("response", response2.answer, "\n")
				incorrect+=1
			if preprocess(response3.answer) == preprocess(answer):
				#print(answer)
				correct +=1
			if(preprocess(response3.answer) != preprocess(answer)):
				print("question", question3)
				print("actual answer", answer)
				print("response", response3.answer, "\n")
			# 	incorrect+=1
	print("correct", correct)
	print("incorrect", incorrect)
	print("total", count)
	print("percentage", correct/count)

readQuestions("English", "margarita")

			
