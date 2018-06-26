# -*- coding: utf-8 -*-

'''Libraries
'''

import string
import re
from collections import defaultdict
from fractions import Fraction
import json
import time
import datetime
import copy
import random

import os
import sys




sys.path.insert(0, 'dialogue-manager/CalimaStar_files/')


import StarMorphModules

import StopWords

import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


import ssl

import math


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('wordnet')
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from string import punctuation
from nltk.corpus import wordnet as wn

nltk.download('stopwords')

stop_words_arabic= ["ما", "ماذا", "هي", "هو"]

'''
Global Variables
'''
porterStemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Dictionary of all Avatars
characterdict = {}

#database filename
db= ''
# encoding
str.encode('utf-8')

av_length=0
av_accuracy=0


# The Structure for an avatar's model
class model:

    def __init__(self):
        self.stemmedMap = {}
        self.lemmatizedMap = {}
        self.wordMap = {}
        self.objectMap = {}
        self.fillers = {}
        self.greetings = {}
        self.questionsMap = {}
        self.noAnswer= {}


# The Structure for a video Object
class videoRecording:
    def __init__(self, question, answer, video, character, language, frequency):
        self.character = character
        self.question = question
        self.answer = answer
        self.videoLink = video
        self.language = language
        self.frequency = frequency
        self.questionLength = len(question.split())
        self.answerLength = len(answer.split())

    def toString(self):
        print( self.character, ": \n", self.question, "\n", self.answer, "\n", self.language, "\n")


# the structure of the session
class session:

    def __init__(self, avatar, language):
        self.repetitions = {}
        self.currentAvatar = avatar
        self.language = language
       

# preprocessing for Arabic
def preprocess(line):
    processed = line.replace("؟", "")
    processed = processed.replace("أ", "ا")
    processed = processed.replace("إ", "ا")
    processed = processed.replace("ى", "ي")
    processed = processed.replace("ة", "ه")

    return processed

# save configuration variables from avatar's json files
def configure(avatar_accuracy, avatar_length):

    if (avatar_accuracy=="high"):
        av_accuracy= 0.1
    elif (avatar_accuracy=="low"):
        av_accuracy= 0.001
    else:
        av_accuracy=0
    
    av_length=avatar_length 

    return av_length, av_accuracy

#generate stop words

def getStopwords(language):
    stop_words= []
    if language=="English":
        stop_words = stopwords.words('english') + list(punctuation)
        #stop_words += ["on", "in", "tell", "me", "about", "a", "an", "the", "of", "and", "or", "but", "what", "are", "you", "your", "is", "was" , "do"]

    elif language== "Arabic":
       stop_words= StopWords.getStopwords()
   
    return stop_words

# get Arabic synonyms
def arabicSyn(myavatar):

    db= 'static/avatar-garden/' + myavatar +'/script.json'

    glossDict={}
    synonymDict={}
    unigram_synonyms_list = []

    f = open(db, 'r', encoding='utf-8')

    resp = json.load(f)

    for i in range(0, len(resp["rows"]) - 1, 1):
        if ("arabic-question" in resp["rows"][i]["doc"].keys() and "arabic-answer" in resp["rows"][i]["doc"].keys()):
            question = json.dumps(resp["rows"][i]["doc"]["arabic-question"], ensure_ascii=False).strip('،.؟"')
            answer = json.dumps(resp["rows"][i]["doc"]["arabic-answer"], ensure_ascii=False).strip('،.؟"')

            pair= question.split()+answer.split()

            for tmp in pair:
                gloss=StarMorphModules.analyze_word(tmp, False)[0].split()[4].split(";")[0].replace("gloss:", "")
                if gloss not in glossDict.keys() and gloss != "NO_ANALYSIS":
                    glossDict[gloss]= []
                    glossDict[gloss].append(tmp)
                elif gloss in glossDict.keys() and gloss != "NO_ANALYSIS":
                    if tmp not in glossDict[gloss]:
                        glossDict[gloss].append(tmp)

    for key in glossDict.keys():
        if len(glossDict[key])>1:
            for i in glossDict[key]:
                if i not in synonymDict.keys():
                    synonymDict[i]=[j for j in glossDict[key]]
    return synonymDict

# Initiates the model and create a new session
def createModel(characterdict, currentSession, mylanguage, myavatar):


    db= 'static/avatar-garden/' + myavatar +'/script.json'
    try:
        f = open(db, 'r', encoding='utf-8')
    except IOError:
        print("Error: File does not appear to exist.")

    resp = json.load(f)
   
    #number of questions in the db 
    totalQuestions = 0

    #counter to generate ID for each video in the model 
    id_count = 0

    if mylanguage=="Arabic":
        arabic_synonyms= arabicSyn(myavatar)

    for i in range(0, len(resp["rows"]) - 1, 1):

        id_count += 1

        # If object is a question-answer pair, the relevant information is extracted
        #if "english-question" in resp["rows"][i]["doc"].keys() or "arabic-question" in resp["rows"][i]["doc"].keys():
        totalQuestions += 1
        # uni_ID= json.dumps(resp["rows"][i]["doc"]["_id"])
        # print(uni_ID)
        video = json.dumps(resp["rows"][i]["doc"]["video"])
        # character= json.dumps(resp["rows"][i]["doc"]["character"])
        character = json.dumps(resp["rows"][i]["doc"]["video"]).split("_")[0].replace('"', '')
        # language= json.dumps(resp["rows"][i]["doc"]["language"])
        language = mylanguage
        ID = id_count;



        frequency= json.dumps(resp["rows"][i]["doc"]["playing frequency"])

        # else:
        #     continue

        if (mylanguage == "Arabic"):
            
            question = json.dumps(resp["rows"][i]["doc"]["arabic-question"], ensure_ascii=False).strip('،.؟"')
            answer = json.dumps(resp["rows"][i]["doc"]["arabic-answer"], ensure_ascii=False).strip('،.؟"')
            question= preprocess(question)
            answer= preprocess(answer)

        if (mylanguage == "English"):
            question = json.dumps(resp["rows"][i]["doc"]["english-question"]).strip(',?."!)')
            answer = json.dumps(resp["rows"][i]["doc"]["english-answer"]).strip(',?."!)')

        # Creates a new character model in the character dictionary if it does not exist already
        if character not in characterdict.keys():
            # characterdict[character] is the model of the respective character
            characterdict[character] = model()


        #save configuration variables
        accuracy= json.dumps(resp["rows"][i]["doc"]["minimum required accuracy"])
        maxLength= json.dumps(resp["rows"][i]["doc"]["length constant"])
        videoType= json.dumps(resp["rows"][i]["doc"]["video-type"])

        configure(accuracy, maxLength)

        # adds to the character's questions list based on the character key; adds all videos regardless of type to questions
        obj = videoRecording(question, answer, video, character, language, frequency)
        characterdict[character].objectMap[ID] = obj



        # if the video is for silence
        if (answer == '""' and video != '""'):
            characterdict[character].fillers[ID] = obj

        #if it's an "I don't have answer for that" video
        if(videoType== '"no-answer"'):
            characterdict[character].noAnswer[ID] = obj

        else:
            characterdict[character].questionsMap[ID] = obj

        # stemming the question and answer and adding the stems, their bigrams and trigrams into model.stemmedMap
        if (mylanguage == "English"):

            #stop_words= getStopwords("English")

            unigram_split = question.lower().split() + answer.lower().split()
            unigram_list = [tmp.strip(',?."!)') for tmp in unigram_split]
            unigram_synonyms_list = []

            #print("unigram list", unigram_list)

            #expands the unigram model by adding synonyms
            for word in unigram_list:
                #if word not in stop_words:
                for synset in wn.synsets(word):
                    for lemma in synset.lemmas():
                        if lemma.name() not in unigram_synonyms_list:
                            unigram_synonyms_list.append(lemma.name())

            # add the bigrams and trigrams into the three representations
            totalUnigrams = len(unigram_list)

            for i in range(totalUnigrams):

                # creates bigrams, their stems and lemmas and adds them to the respective maps
                if i < totalUnigrams - 1:

                    bigram = unigram_list[i] + "_" + unigram_list[i + 1]
                    if bigram not in characterdict[character].wordMap.keys():
                        characterdict[character].wordMap[bigram] = {}
                    if ID not in characterdict[character].wordMap[bigram]:
                        characterdict[character].wordMap[bigram][ID] = 1
                    else:
                        characterdict[character].wordMap[bigram][ID] += 1

                    bigram_stem = porterStemmer.stem(unigram_list[i]) + "_" + porterStemmer.stem(unigram_list[i + 1])
                    if bigram_stem not in characterdict[character].stemmedMap.keys():
                        characterdict[character].stemmedMap[bigram_stem] = {}
                    if ID not in characterdict[character].stemmedMap[bigram_stem]:
                        characterdict[character].stemmedMap[bigram_stem][ID] = 1
                    else:
                        characterdict[character].wordMap[bigram][ID] += 1

                    bigram_lemma = lemmatizer.lemmatize(unigram_list[i]) + "_" + lemmatizer.lemmatize(
                        unigram_list[i + 1])
                    if bigram_lemma not in characterdict[character].lemmatizedMap.keys():
                        characterdict[character].lemmatizedMap[bigram_lemma] = {}
                    if ID not in characterdict[character].lemmatizedMap[bigram_lemma]:
                        characterdict[character].lemmatizedMap[bigram_lemma][ID] = 1
                    else:
                        characterdict[character].lemmatizedMap[bigram_lemma][ID] += 1

                # creates trigrams, their stems and lemmas and add them to the respective maps
                if i < totalUnigrams - 2:

                    trigram = unigram_list[i] + "_" + unigram_list[i + 1] + "_" + unigram_list[i + 2]
                    if trigram not in characterdict[character].wordMap.keys():
                        characterdict[character].wordMap[trigram] = {}
                    if ID not in characterdict[character].wordMap[trigram]:
                        characterdict[character].wordMap[trigram][ID] = 1
                    else:
                        characterdict[character].wordMap[trigram][ID] = +1

                    trigram_stem = porterStemmer.stem(unigram_list[i]) + "_" + porterStemmer.stem(
                        unigram_list[i + 1]) + "_" + porterStemmer.stem(unigram_list[i + 2])
                    if trigram_stem not in characterdict[character].stemmedMap.keys():
                        characterdict[character].stemmedMap[trigram_stem] = {}
                    if ID not in characterdict[character].stemmedMap[trigram_stem]:
                        characterdict[character].stemmedMap[trigram_stem][ID] = 1
                    else:
                        characterdict[character].stemmedMap[trigram_stem][ID] += 1

                    trigram_lemma = lemmatizer.lemmatize(unigram_list[i]) + "_" + lemmatizer.lemmatize(
                        unigram_list[i + 1]) + "_" + lemmatizer.lemmatize(unigram_list[i + 2])
                    if trigram_lemma not in characterdict[character].lemmatizedMap.keys():
                        characterdict[character].lemmatizedMap[trigram_lemma] = {}
                    if ID not in characterdict[character].lemmatizedMap[trigram_lemma]:
                        characterdict[character].lemmatizedMap[trigram_lemma][ID] = 1
                    else:
                        characterdict[character].lemmatizedMap[trigram_lemma][ID] += 1

            # removes stop words
            # question_split = [tmp.strip(', " ?.!') for tmp in question_split if tmp not in stop_words]
            # answer_split = [tmp.strip(', " ?.!') for tmp in answer_split if tmp not in stop_words]

            # adds the unigrams and their synonyms into the three hashmaps - stems, lemmas and direct:

            ''' 
            1. characterdict[character].wordMap is a dictionary where the key is the word 
            and the value is another dictionary with video IDs as keys, and the number of times that the word appears in that video as values
            
            2. characterdict[character].stemmedMap is a dictionary where the key is the stem of a word 
            and the value is another dictionary with video IDs as keys, and the number of times that the word appears in that video as values

            3. characterdict[character].LemmatizedMap is a dictionary where the key is the word (either unigram, bigram, or trigram)
            and the value is another dictionary with video IDs as keys, and the number of times that the word appears in that video as values
            '''
            for token in (unigram_list):
                

                stem = porterStemmer.stem(token)
                lemma = lemmatizer.lemmatize(token)

                if token not in characterdict[character].wordMap.keys():
                    characterdict[character].wordMap[token] = {}
                if ID not in characterdict[character].wordMap[token].keys():
                    characterdict[character].wordMap[token][ID] = 1
                else:
                    characterdict[character].wordMap[token][ID] += 1
                #print("token" + " " + token, characterdict[character].wordMap[token])

                if stem not in characterdict[character].stemmedMap.keys():
                    characterdict[character].stemmedMap[stem] = {}
                if ID not in characterdict[character].stemmedMap[stem]:
                    characterdict[character].stemmedMap[stem][ID] = 1
                else:
                    characterdict[character].stemmedMap[stem][ID] += 1

                if lemma not in characterdict[character].lemmatizedMap.keys():
                    characterdict[character].lemmatizedMap[lemma] = {}
                if ID not in characterdict[character].lemmatizedMap[lemma]:
                    characterdict[character].lemmatizedMap[lemma][ID] = 1
                else:
                    characterdict[character].lemmatizedMap[lemma][ID] += 1

                characterdict[character].wordMap[token][ID]= characterdict[character].wordMap[token][ID]/totalUnigrams
                characterdict[character].stemmedMap[stem][ID]= characterdict[character].stemmedMap[stem][ID]/totalUnigrams
                characterdict[character].lemmatizedMap[lemma][ID]= characterdict[character].stemmedMap[stem][ID]/totalUnigrams

        elif (mylanguage == "Arabic"):

            #arabic_stop_words= getStopwords("Arabic")

            unigram_split = question.strip('،"!؟/)').replace("،", " ").replace("/", " ").split() + answer.strip('،"!؟/)').replace("،", " ").replace("/", " ").split()

            unigram_list = [tmp.strip('،"!؟/)').replace('/', '') for tmp in unigram_split]

            unigram_synonyms_list = []


        	# expands the unigram model by adding synonyms
            for word in unigram_list:
            	if word in arabic_synonyms.keys():
            		for tmp in arabic_synonyms[word]:
            			if tmp not in unigram_synonyms_list:
            				unigram_synonyms_list.append(tmp)



            # add the bigrams and trigrams into the three representations
            totalUnigrams = len(unigram_list)

            for i in range(totalUnigrams):

                # creates bigrams, their stems and lemmas and adds them to the respective maps
                if (i < totalUnigrams - 1):
                    bigram = unigram_list[i] + "_" + unigram_list[i + 1]
                    if bigram not in characterdict[character].wordMap.keys():
                        characterdict[character].wordMap[bigram] = {}
                    if ID not in characterdict[character].wordMap[bigram]:
                        characterdict[character].wordMap[bigram][ID] = 1
                    else:
                        characterdict[character].wordMap[bigram][ID] += 1

                    bigram_stem = StarMorphModules.analyze_word(unigram_list[i], False)[0].split()[1].replace("stem:", "").split('d',1)[0] + "_" + StarMorphModules.analyze_word(unigram_list[i+1], False)[0].split()[1].replace("stem:", "").split('d',1)[0]

                    if bigram_stem not in characterdict[character].stemmedMap.keys():
                        characterdict[character].stemmedMap[bigram_stem] = {}
                    if ID not in characterdict[character].stemmedMap[bigram_stem]:
                        characterdict[character].stemmedMap[bigram_stem][ID] = 1
                    else:
                        characterdict[character].wordMap[bigram][ID] += 1

                    bigram_lemma = StarMorphModules.analyze_word(unigram_list[i], False)[0].split()[0].replace("lex:", "").split('_',1)[0] + "_" + StarMorphModules.analyze_word(unigram_list[i+1], False)[0].split()[0].replace("lex:", "").split('_',1)[0]

                    if bigram_lemma not in characterdict[character].lemmatizedMap.keys():
                        characterdict[character].lemmatizedMap[bigram_lemma] = {}

                    if ID not in characterdict[character].lemmatizedMap[bigram_lemma]:
                        characterdict[character].lemmatizedMap[bigram_lemma][ID] = 1
                    else:
                        characterdict[character].lemmatizedMap[bigram_lemma][ID] += 1

	        	 # creates trigrams, their stems and lemmas and add them to the respective maps
                if i < totalUnigrams - 2:
                    trigram = unigram_list[i] + "_" + unigram_list[i + 1] + "_" + unigram_list[i + 2]

                    if trigram not in characterdict[character].wordMap.keys():
                        characterdict[character].wordMap[trigram] = {}
                    if ID not in characterdict[character].wordMap[trigram]:
                        characterdict[character].wordMap[trigram][ID] = 1
                    else:
                        characterdict[character].wordMap[trigram][ID] = +1

                    trigram_stem =  StarMorphModules.analyze_word(unigram_list[i], False)[0].split()[1].replace("stem:", "").split('d',1)[0] + "_" + StarMorphModules.analyze_word(unigram_list[i+1], False)[0].split()[1].replace("stem:", "").split('d',1)[0]+ "_" + StarMorphModules.analyze_word(unigram_list[i+2], False)[0].split()[1].replace("stem:", "").split('d',1)[0]
                    if trigram_stem not in characterdict[character].stemmedMap.keys():
                        characterdict[character].stemmedMap[trigram_stem] = {}
                    if ID not in characterdict[character].stemmedMap[trigram_stem]:
                        characterdict[character].stemmedMap[trigram_stem][ID] = 1
                    else:
                        characterdict[character].stemmedMap[trigram_stem][ID] += 1

                    trigram_lemma = StarMorphModules.analyze_word(unigram_list[i], False)[0].split()[0].replace("lex:", "").split('_',1)[0] + "_" + StarMorphModules.analyze_word(unigram_list[i+1], False)[0].split()[0].replace("lex:", "").split('_',1)[0] + "_" + StarMorphModules.analyze_word(unigram_list[i+2], False)[0].split()[0].replace("lex:", "").split('_',1)[0]
                    if trigram_lemma not in characterdict[character].lemmatizedMap.keys():
                        characterdict[character].lemmatizedMap[trigram_lemma] = {}
                    if ID not in characterdict[character].lemmatizedMap[trigram_lemma]:
                        characterdict[character].lemmatizedMap[trigram_lemma][ID] = 1
                    else:
                        characterdict[character].lemmatizedMap[trigram_lemma][ID] += 1
	        
            # adds the unigrams and their synonyms into the three hashmaps - stems, lemmas and direct + unigram_synonyms_list:
            for token in (unigram_list+ unigram_synonyms_list):
                stem = StarMorphModules.analyze_word(token, False)[0].split()[1].replace("stem:", "").split('d',1)[0]
                lemma = StarMorphModules.analyze_word(token, False)[0].split()[0].replace("lex:", "").split('_',1)[0]

                if token not in characterdict[character].wordMap.keys():
                    characterdict[character].wordMap[token] = {}
                if ID not in characterdict[character].wordMap[token]:
                    print(ID, token)
                    characterdict[character].wordMap[token][ID] = 1
                else:
                    print("second time", ID, token)
                    characterdict[character].wordMap[token][ID] += 1

                if stem not in characterdict[character].stemmedMap.keys():
                    characterdict[character].stemmedMap[stem] = {}
                if ID not in characterdict[character].stemmedMap[stem]:
                    characterdict[character].stemmedMap[stem][ID] = 1
                else:
                    characterdict[character].stemmedMap[stem][ID] += 1

                if lemma not in characterdict[character].lemmatizedMap.keys():
                    characterdict[character].lemmatizedMap[lemma] = {}
                if ID not in characterdict[character].lemmatizedMap[lemma]:
                    characterdict[character].lemmatizedMap[lemma][ID] = 1
                else:
                    characterdict[character].lemmatizedMap[lemma][ID] += 1

    print("number of times name appears in video 1:" , characterdict[character].wordMap["name"][1])

    print("Total Questions: ", str(totalQuestions))
    print("done")
    # print(characterdict["gabriela"].wordMap)
    #print("before",characterdict['margarita'].wordMap['hello'])
    calculateTFIDF(characterdict)
    #print("character dictionary", characterdict['margarita'])
    #print("after", characterdict['margarita'].wordMap['hello'])
    return currentSession


def findLemmaScore(lemma):
    score=0
    lookup= open('dialogue-manager/CalimaStar_files/lookup-table.txt', 'r', encoding='utf-8')
    for line in lookup:
        if lemma== line[0]:
            score= line[1]

    #print("lemma score", score)

    return score



def direct_intersection_match_English(query, characterModel, logger):
    #stop_words= getStopwords("English")
    stop_words= []
    queryList = [tmp.strip(', " ?.!)') for tmp in query.split() if tmp not in stop_words ]
    responses = {}
    queryLen = len(queryList)

    # newList = []

    # #expands the unigram model by adding synonyms
    # for word in queryList:
    # 	#if word not in stop_words:
    # 	for synset in wn.synsets(word):
    # 		for lemma in synset.lemmas():
    # 			if lemma.name() not in newList:
    # 				newList.append(lemma.name())

    for i in range(queryLen):

        unigram_string = queryList[i]
        if unigram_string in characterModel.wordMap.keys():  # and direct_string not in stop_words:
            #print("word: ", unigram_string)
            #print("word map: ", characterModel.wordMap[unigram_string])
            for vidResponse in characterModel.wordMap[unigram_string]:
                #print("videos that include ",unigram_string, vidResponse )
                if vidResponse not in responses.keys():
                    responses[vidResponse] = characterModel.wordMap[unigram_string][vidResponse]
                    #print("added video "+ str(vidResponse) + "to responses" + " its value is " + str(characterModel.wordMap[unigram_string][vidResponse]))
                else:
                    responses[vidResponse] += characterModel.wordMap[unigram_string][vidResponse]
                    #print("increased score of " + str(vidResponse) + "by " + str(characterModel.wordMap[unigram_string][vidResponse]))
                if vidResponse not in logger.keys():
                    logger[vidResponse] = {}
                    logger[vidResponse][unigram_string] = characterModel.wordMap[unigram_string][vidResponse]
                else:
                    if unigram_string in logger[vidResponse]:
                        logger[vidResponse][unigram_string] += characterModel.wordMap[unigram_string][vidResponse]
                    else:
                        logger[vidResponse][unigram_string] = characterModel.wordMap[unigram_string][vidResponse]


        # if i < queryLen - 2:
        #     bigram_string = queryList[i] + "_" + queryList[i+1]
        #     if bigram_string in characterModel.wordMap.keys():  # and direct_string not in stop_words:
        #         for vidResponse in characterModel.wordMap[bigram_string]:
        #             if vidResponse not in responses.keys():
        #                 responses[vidResponse] = characterModel.wordMap[bigram_string][vidResponse]
        #             elif vidResponse in responses.keys():
        #                 responses[vidResponse] += characterModel.wordMap[bigram_string][vidResponse]

        # if i < queryLen - 3:
        #     trigram_string = queryList[i] + "_" + queryList[i+1] + "_" + queryList[i+2]
        #     if trigram_string in characterModel.wordMap.keys():  # and direct_string not in stop_words:
        #         for vidResponse in characterModel.wordMap[trigram_string]:
        #             if vidResponse not in responses.keys():
        #                 responses[vidResponse] = characterModel.wordMap[trigram_string][vidResponse]
        #             elif vidResponse in responses.keys():
        #                 responses[vidResponse] += characterModel.wordMap[trigram_string][vidResponse]

    # for direct_string in queryList:
    #     if direct_string in characterModel.wordMap.keys():  # and direct_string not in stop_words:
    #         for vidResponse in characterModel.wordMap[direct_string]:
    #             if vidResponse not in responses.keys():
    #                 responses[vidResponse] = characterModel.wordMap[direct_string][vidResponse]
    #             elif vidResponse in responses.keys():
    #                 responses[vidResponse] += characterModel.wordMap[direct_string][vidResponse]

    
    print("English direct responses", responses)
    for key in responses.keys():
        responses[key]= responses[key]
    
    return responses


def stem_intersection_match_English(query, characterModel, logger):
    #stop_words= getStopwords("English")
    stop_words= []
    queryList = [porterStemmer.stem(tmp.strip(', " ?.!)')) for tmp in query.split() if tmp not in stop_words ]

    responses = {}
    key_repetitions= {}

    queryLen = len(queryList)

    for i in range(queryLen):

        unigram_string = queryList[i]
        if unigram_string in characterModel.stemmedMap.keys():
            for vidResponse in characterModel.stemmedMap[unigram_string]:
                if vidResponse not in responses.keys():
                    #number of times the unigram appears in the entry with the vidResponse ID 
                    responses[vidResponse] = characterModel.stemmedMap[unigram_string][vidResponse]
                    #print("response", responses[vidResponse])
                else:
                    responses[vidResponse] += characterModel.stemmedMap[unigram_string][vidResponse]

                if vidResponse not in logger.keys():
                    logger[vidResponse] = {}
                    logger[vidResponse][unigram_string] = characterModel.stemmedMap[unigram_string][vidResponse]
                else:
                    if unigram_string in logger[vidResponse]:
                        logger[vidResponse][unigram_string] += characterModel.stemmedMap[unigram_string][vidResponse]
                    else:
                        logger[vidResponse][unigram_string] = characterModel.stemmedMap[unigram_string][vidResponse]

        # if i < queryLen - 2:
        #     bigram_string = queryList[i] + "_" + queryList[i+1]
        #     if bigram_string in characterModel.stemmedMap.keys():
        #         for vidResponse in characterModel.stemmedMap[bigram_string]:
        #             if vidResponse not in responses.keys():
        #                 responses[vidResponse] = characterModel.stemmedMap[bigram_string][vidResponse]
        #             elif vidResponse in responses.keys():
        #                 responses[vidResponse] += characterModel.stemmedMap[bigram_string][vidResponse]

        # if i < queryLen - 3:
        #     trigram_string = queryList[i] + "_" + queryList[i+1] + "_" + queryList[i+2]
        #     if trigram_string in characterModel.stemmedMap.keys():
        #         for vidResponse in characterModel.stemmedMap[trigram_string]:
        #             if vidResponse not in responses.keys():
        #                 responses[vidResponse] = characterModel.stemmedMap[trigram_string][vidResponse]
        #             elif vidResponse in responses.keys():
        #                 responses[vidResponse] += characterModel.stemmedMap[trigram_string][vidResponse]

    # for stem_string in queryList:
    #     if stem_string in characterModel.stemmedMap.keys():
    #         for vidResponse in characterModel.stemmedMap[stem_string]:
    #             if vidResponse not in responses.keys():
    #                 responses[vidResponse] = characterModel.stemmedMap[stem_string][vidResponse]
    #             elif vidResponse in responses.keys():
    #                 responses[vidResponse] += characterModel.stemmedMap[stem_string][vidResponse]

    for key in responses.keys():
        responses[key]= responses[key]
        #print("stem score",responses[key] )
    
    print("English stem responses", responses)
    return responses



def lemma_intersection_match_English(query, characterModel, logger):
    #stop_words= getStopwords("English")
    stop_words=[]
    queryList = [lemmatizer.lemmatize(tmp.strip(', " ?.!)')) for tmp in query.split() if tmp not in stop_words ]

    responses = {}
    queryLen = len(queryList)

    for i in range(queryLen):

        unigram_string = queryList[i]
        if unigram_string in characterModel.lemmatizedMap.keys():
            for vidResponse in characterModel.lemmatizedMap[unigram_string]:
                if vidResponse not in responses.keys():
                    responses[vidResponse] = characterModel.lemmatizedMap[unigram_string][vidResponse]

                else:
                    responses[vidResponse] += characterModel.lemmatizedMap[unigram_string][vidResponse]

                if vidResponse not in logger.keys():
                    logger[vidResponse] = {}
                    logger[vidResponse][unigram_string] = characterModel.lemmatizedMap[unigram_string][vidResponse]
                else:
                    if unigram_string in logger[vidResponse]:
                        logger[vidResponse][unigram_string] += characterModel.lemmatizedMap[unigram_string][vidResponse]
                    else:
                        logger[vidResponse][unigram_string] = characterModel.lemmatizedMap[unigram_string][vidResponse]

        # if i < queryLen - 2:
        #     bigram_string = queryList[i] + "_" + queryList[i+1]
        #     if bigram_string in characterModel.lemmatizedMap.keys():
        #         for vidResponse in characterModel.lemmatizedMap[bigram_string]:
        #             if vidResponse not in responses.keys():
        #                 responses[vidResponse] = characterModel.lemmatizedMap[bigram_string][vidResponse]
        #             elif vidResponse in responses.keys():
        #                 responses[vidResponse] += characterModel.lemmatizedMap[bigram_string][vidResponse]


        # if i < queryLen - 3:
        #     trigram_string = queryList[i] + "_" + queryList[i+1] + "_" + queryList[i+2]
        #     if trigram_string in characterModel.lemmatizedMap.keys():
        #         for vidResponse in characterModel.lemmatizedMap[trigram_string]:
        #             if vidResponse not in responses.keys():
        #                 responses[vidResponse] = characterModel.lemmatizedMap[trigram_string][vidResponse]
        #             elif vidResponse in responses.keys():
        #                 responses[vidResponse] += characterModel.lemmatizedMap[trigram_string][vidResponse]

    # for lemma_string in queryList:
    #     if lemma_string in characterModel.lemmatizedMap.keys():
    #         for vidResponse in characterModel.lemmatizedMap[lemma_string]:
    #             if vidResponse not in responses.keys():
    #                 responses[vidResponse] = characterModel.lemmatizedMap[lemma_string][vidResponse]
    #             elif vidResponse in responses.keys():
    #                 responses[vidResponse] += characterModel.lemmatizedMap[lemma_string][vidResponse]

    for key in responses.keys():
        #print("lemma score before", responses[key])
        responses[key]= responses[key]
        #print("lemma score after", responses[key])
    
    print("English lemma responses", responses)
    return responses


def direct_intersection_match_Arabic(query, characterModel, logger):
    arabic_stop_words= getStopwords("Arabic")
    queryList = [tmp.strip('،!؟."') for tmp in query.split()if tmp not in arabic_stop_words]
    # queryList.encode('utf-8')

    responses = {}
    queryLen = len(queryList)

    for i in range(queryLen):

        unigram_string = queryList[i]
        if unigram_string in characterModel.wordMap.keys():  
            for vidResponse in characterModel.wordMap[unigram_string]:
                if vidResponse not in responses.keys():
                    responses[vidResponse] = characterModel.wordMap[unigram_string][vidResponse]
                else:
                    responses[vidResponse] += characterModel.wordMap[unigram_string][vidResponse]

                if vidResponse not in logger.keys():
                    logger[vidResponse] = {}
                    logger[vidResponse][unigram_string] = characterModel.wordMap[unigram_string][vidResponse]
                else:
                    if unigram_string in logger[vidResponse]:
                        logger[vidResponse][unigram_string] += characterModel.wordMap[unigram_string][vidResponse]
                    else:
                        logger[vidResponse][unigram_string] = characterModel.wordMap[unigram_string][vidResponse]

        # if i < queryLen - 2:
        #     bigram_string = queryList[i] + "_" + queryList[i+1]
        #     if bigram_string in characterModel.wordMap.keys():  # and direct_string not in stop_words:
        #         for vidResponse in characterModel.wordMap[bigram_string]:
        #             if vidResponse not in responses.keys():
        #                 responses[vidResponse] = characterModel.wordMap[bigram_string][vidResponse]
        #             elif vidResponse in responses.keys():
        #                 responses[vidResponse] += characterModel.wordMap[bigram_string][vidResponse]

        # if i < queryLen - 3:
        #     trigram_string = queryList[i] + "_" + queryList[i+1] + "_" + queryList[i+2]
        #     if trigram_string in characterModel.wordMap.keys():  # and direct_string not in stop_words:
        #         for vidResponse in characterModel.wordMap[trigram_string]:
        #             if vidResponse not in responses.keys():
        #                 responses[vidResponse] = characterModel.wordMap[trigram_string][vidResponse]
        #             elif vidResponse in responses.keys():
        #                 responses[vidResponse] += characterModel.wordMap[trigram_string][vidResponse]


    for key in responses.keys():
        responses[key]= responses[key]


    return responses


def stem_intersection_match_Arabic(query, characterModel, logger):
    # StarMorphModules.read_config("config_stem.xml")
    # StarMorphModules.initialize_from_file("almor-s31.db","analyze")

    # print("Finding stem Intersection in Arabic")
    arabic_stop_words= getStopwords("Arabic")
    queryList = [tmp.strip('،!؟."') for tmp in query.split()if tmp not in arabic_stop_words]
    responses = {}
    stemmed_query = []
    queryLen = len(queryList)

    for word in queryList:
        analysis = StarMorphModules.analyze_word(word, False)

        stemmed_query.append(analysis[0].split()[1].replace("stem:", "").split('d', 1)[0])

    for i in range(queryLen):

        unigram_string = stemmed_query[i]
        if unigram_string in characterModel.stemmedMap.keys():
            for vidResponse in characterModel.stemmedMap[unigram_string]:
                if vidResponse not in responses.keys():
                    responses[vidResponse] = characterModel.stemmedMap[unigram_string][vidResponse]
                else:
                    responses[vidResponse] += characterModel.stemmedMap[unigram_string][vidResponse]

                if vidResponse not in logger.keys():
                    logger[vidResponse] = {}
                    logger[vidResponse][unigram_string] = characterModel.stemmedMap[unigram_string][vidResponse]
                else:
                    if unigram_string in logger[vidResponse]:
                        logger[vidResponse][unigram_string] += characterModel.stemmedMap[unigram_string][vidResponse]
                    else:
                        logger[vidResponse][unigram_string] = characterModel.stemmedMap[unigram_string][vidResponse]

        # if i < queryLen - 2:
        #     bigram_string = stemmed_query[i] + "_" + stemmed_query[i+1]
        #     if bigram_string in characterModel.stemmedMap.keys():
        #         for vidResponse in characterModel.stemmedMap[bigram_string]:
        #             if vidResponse not in responses.keys():
        #                 responses[vidResponse] = characterModel.stemmedMap[bigram_string][vidResponse]
        #             elif vidResponse in responses.keys():
        #                 responses[vidResponse] += characterModel.stemmedMap[bigram_string][vidResponse]

        # if i < queryLen - 3:
        #     trigram_string = stemmed_query[i] + "_" + stemmed_query[i+1] + "_" + stemmed_query[i+2]
        #     if trigram_string in characterModel.stemmedMap.keys():  # and direct_string not in stop_words:
        #         for vidResponse in characterModel.stemmedMap[trigram_string]:
        #             if vidResponse not in responses.keys():
        #                 responses[vidResponse] = characterModel.stemmedMap[trigram_string][vidResponse]
        #             elif vidResponse in responses.keys():
        #                 responses[vidResponse] += characterModel.stemmedMap[trigram_string][vidResponse]


    for key in responses.keys():
        responses[key]= responses[key]
    return responses


def lemma_intersection_match_Arabic(query, characterModel, logger):
    # print("Finding lemma Intersection in Arabic")
    max_score=0
    arabic_stop_words= getStopwords("Arabic")
    queryList = [tmp.strip('،!؟."') for tmp in query.split()if tmp not in arabic_stop_words]
    # queryList.encode('utf-8')

    responses = {}
    lemma_final= ''


    lemmatized_query = []
    for word in queryList:
        # print(word)
        analysis = StarMorphModules.analyze_word(word, False)
        
        for i in range(0, len(analysis), 1):
            lemma_possible= analysis[i].split()[0].replace("lex:", "").split('_', 1)[0]
            lemma_score= findLemmaScore(lemma_possible)
            if lemma_score> max_score:
                max_score= lemma_score
                lemma_final= lemma_possible
            else:
                lemma_final= analysis[0].split()[0].replace("lex:", "").split('_', 1)[0]

        
        lemma = re.sub(r'[^\u0621-\u064A]', '', lemma_final, flags=re.UNICODE)
        lemmatized_query.append(lemma)

    queryLen = len(lemmatized_query)

    for i in range(queryLen):

        unigram_string = lemmatized_query[i]
        if unigram_string in characterModel.lemmatizedMap.keys():
            for vidResponse in characterModel.lemmatizedMap[unigram_string]:
                if vidResponse not in responses.keys():
                    responses[vidResponse] = characterModel.lemmatizedMap[unigram_string][vidResponse]
                else:
                    responses[vidResponse] += characterModel.lemmatizedMap[unigram_string][vidResponse]

                if vidResponse not in logger.keys():
                    logger[vidResponse] = {}
                    logger[vidResponse][unigram_string] = characterModel.lemmatizedMap[unigram_string][vidResponse]
                else:
                    if unigram_string in logger[vidResponse]:
                        logger[vidResponse][unigram_string] += characterModel.lemmatizedMap[unigram_string][vidResponse]
                    else:
                        logger[vidResponse][unigram_string] = characterModel.lemmatizedMap[unigram_string][vidResponse]




        # if i < queryLen - 2:
        #     bigram_string = lemmatized_query[i] + "_" + lemmatized_query[i+1]
        #     if bigram_string in characterModel.lemmatizedMap.keys():  # and direct_string not in stop_words:
        #         for vidResponse in characterModel.lemmatizedMap[bigram_string]:
        #             if vidResponse not in responses.keys():
        #                 responses[vidResponse] = characterModel.lemmatizedMap[bigram_string][vidResponse]
        #             elif vidResponse in responses.keys():
        #                 responses[vidResponse] += characterModel.lemmatizedMap[bigram_string][vidResponse]

        # if i < queryLen - 3:
        #     trigram_string = lemmatized_query[i] + "_" + lemmatized_query[i+1] + "_" + lemmatized_query[i+2]
        #     if trigram_string in characterModel.lemmatizedMap.keys():  # and direct_string not in stop_words:
        #         for vidResponse in characterModel.lemmatizedMap[trigram_string]:
        #             if vidResponse not in responses.keys():
        #                 responses[vidResponse] = characterModel.lemmatizedMap[trigram_string][vidResponse]
        #             elif vidResponse in responses.keys():
        #                 responses[vidResponse] += characterModel.lemmatizedMap[trigram_string][vidResponse]


    for key in responses.keys():
        responses[key]= responses[key]
    return responses


def calculateTFIDF(characterdict):
    # #are we using each question as a "doc" or each character model?

    # totalDocs = len(characterModel.objectMap)

    # #tf: term frequency
    # tf= doc.words.count(token) / len(doc.words)

    # #number of docs containing the token
    # n_containing= sum(1 for doc in doclist if token in doc.words)

    # #idf: inverse document frequency
    # idf= math.log(len(doclist) / (1 + n_containing(token, doclist)))

    # #tfifd
    # tfidf= tf * idf
    # return tfidf

    for avatar in characterdict:
        totalDocs = len(characterdict[avatar].objectMap)
        print("Total Docs: ", totalDocs)
        for lemma in characterdict[avatar].lemmatizedMap.keys():
            idf = totalDocs / len(characterdict[avatar].lemmatizedMap[lemma])
            for doc in characterdict[avatar].lemmatizedMap[lemma].keys():
                tf = characterdict[avatar].lemmatizedMap[lemma][doc]
                tfidf = tf * idf
                #characterdict[avatar].lemmatizedMap[lemma][doc] = tfidf
                #print("lemma tfidf" + " " + lemma, characterdict[avatar].lemmatizedMap[lemma][doc])

        # idf: inverse document frequency
        # idf= math.log(len(doclist) / (1 + n_containing(token, doclist)))
        # totaldocs/number of docs the word appears in (don't use the log because it's not a large number of documents)
        # tfifd
        # tfidf= tf * idf

        for stem in characterdict[avatar].stemmedMap.keys():
            idf = totalDocs / len(characterdict[avatar].stemmedMap[stem])
            for doc in characterdict[avatar].stemmedMap[stem].keys():
                tf = characterdict[avatar].stemmedMap[stem][doc]
                tfidf = tf * idf
                #characterdict[avatar].stemmedMap[stem][doc] = tfidf

        for word in characterdict[avatar].wordMap.keys():
            idf = totalDocs / len(characterdict[avatar].wordMap[word])
            for doc in characterdict[avatar].wordMap[word].keys():
                tf = characterdict[avatar].wordMap[word][doc]
                tfidf = tf * idf
                #characterdict[avatar].wordMap[word][doc] = tfidf

    #print("avatar dict", characterdict['margarita'].wordMap["hello"][])
   

    #return characterdict


def rankAnswers(query, videoResponses, currentSession, characterModel, counter):
    query_len = len(query.split())
    allowed=1
    rep=0


    # each repition is a given a weight of 2 e.g if a video has been played once 2 points will be subtracted from its matching score

    # for each possible answer, checks if it has been played it already, and subtract points from its score if has been played already.
    for res in videoResponses:
        videoObjLen = characterModel.objectMap[res].answerLength
        # precision = videoResponses[res] / videoObjLen
        # recall = videoResponses[res] / query_len
        # f_score = (precision + recall) / 2
        pref_frequency= characterModel.objectMap[res].frequency
        #print("frequency", pref_frequency)
        total_iterations= counter
        
        if (videoObjLen >int(av_length)):
            videoResponses[res] = videoResponses[res]/ videoObjLen
        
        if (pref_frequency=='"never"'):
            #print("yes never")
            allowed=0
        elif(pref_frequency=='"multiple"' or pref_frequency=='"once"'):
            #print("multiple or once")
            allowed=1


        if res in currentSession.repetitions.keys():
            #print("repeats", currentSession.repetitions[res])
            if (pref_frequency=='"multiple"'):
                #print("multiple")
                allowed=1
            elif(pref_frequency=='"once"'):

                if currentSession.repetitions[res]>1:
                    allowed=0
                    print("once done")
                else:
                    allowed=1
                    print("once allowed")
            elif (pref_frequency=='"never"'):
                allowed=0
                #print("never")
            
            rep= currentSession.repetitions[res]

        #print("score",  videoResponses[res])
        #print("allowed", allowed)
        videoResponses[res]=(videoResponses[res]*(1-rep/(total_iterations+1)))*allowed
        if videoResponses[res]< av_accuracy:
            videoResponses[res]=0



        # if res in currentSession.repetitions.keys():
        #     negativePoints = currentSession.repetitions[res] * 0.4 * videoResponses[res]
        #     videoResponses[res] -= negativePoints




        
        

    #print("responses", videoResponses)
    ranked_list = sorted(videoResponses, key=lambda i: videoResponses[i], reverse=True)
    print("video playing:", ranked_list[0])
    return ranked_list



def findResponse(query, characterModel, currentSession, counter):

    currentTime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    language = currentSession.language
    themax = 0
    best_responses = {}
    stem_match_responses = {}
    lemma_match_responses = {}
    direct_match_responses = {}
    key_repetitions= {}
    logger = {}
    counter=0

    if language == "English":
        f = open('english_log.tsv', 'a', encoding='utf-8')
    else:
        f = open('arabic_log.tsv', 'a', encoding='utf-8')

    query = query.lower().strip(',?.")!')

    if language == "English":
        # each function returns a dictionary with the video ID as key and the score as value
        stem_match_responses = stem_intersection_match_English(query, characterModel, logger)
        lemma_match_responses = lemma_intersection_match_English(query, characterModel, logger)
        direct_match_responses = direct_intersection_match_English(query, characterModel, logger)

    elif language == "Arabic":
        # each function returns a dictionary with the video ID as key and the score as value
        stem_match_responses = stem_intersection_match_Arabic(query, characterModel, logger)
        lemma_match_responses = lemma_intersection_match_Arabic(query, characterModel, logger)
        direct_match_responses = direct_intersection_match_Arabic(query, characterModel, logger)
    else:
        print("language not recognised")
        return

    for key in stem_match_responses.keys():
        if key not in key_repetitions.keys():
            key_repetitions[key]=1
        else:
            key_repetitions[key]+=1
        if key not in best_responses.keys():
            best_responses[key] = stem_match_responses[key]
            best_responses[key]= copy.deepcopy(stem_match_responses[key])
            #print("value", best_responses[key])
           
        else:
            best_responses[key] += copy.deepcopy(stem_match_responses[key])
            

    for key in lemma_match_responses.keys():
        if key not in key_repetitions.keys():
            key_repetitions[key]=1
        else:
            key_repetitions[key]+=1
        if key not in best_responses.keys():
            best_responses[key] = copy.deepcopy(lemma_match_responses[key])
          
        else:
            best_responses[key] += copy.deepcopy(lemma_match_responses[key])
            
            
            

    for key in direct_match_responses.keys():
        if key not in key_repetitions.keys():
            key_repetitions[key]=1
        else:
            key_repetitions[key]+=1
        if key not in best_responses.keys():
            best_responses[key] = copy.deepcopy(direct_match_responses[key])
           
        else:
            best_responses[key] += copy.deepcopy(direct_match_responses[key])
           

    for key in best_responses.keys():
       #print("before", best_responses[key] )
       #print("repetitions", key_repetitions[key])
       best_responses[key]= best_responses[key]/key_repetitions[key]
       #print("after", best_responses[key])
    
    #print("best responses", best_responses)
            
           

   
    # if the responses are empty, play "I can't answer that response"
   
    if bool(best_responses) == False:
        noAnswerList= characterModel.noAnswer.keys()
        final_answer= random.choice(list(noAnswerList))
      


    else:
       
        ranked_responses = rankAnswers(query, best_responses, currentSession, characterModel, counter)
        print("final responses", ranked_responses)
        final_answer = ranked_responses[0]

        # if len(ranked_responses) > 2:
        #     second_response = ranked_responses[1]
        #     third_response = ranked_responses[2]
        #     log_string = currentTime + "\t" + currentSession.currentAvatar + "\t" + query + "\t" + characterModel.objectMap[final_answer].answer + "\t" + str(best_responses[final_answer]) + "\t" + str(logger[final_answer]) +  "\t" + characterModel.objectMap[second_response].answer + "\t" + str(best_responses[second_response]) + "\t" + str(logger[second_response]) +  "\t" + characterModel.objectMap[third_response].answer + "\t" + str(best_responses[third_response]) + "\t" + str(logger[third_response]) + "\n"

        # elif len(ranked_responses) == 2:
        #     second_response = ranked_responses[1]
        #     log_string = currentTime + "\t" + currentSession.currentAvatar + "\t" + query + "\t" + characterModel.objectMap[final_answer].answer + "\t" + str(best_responses[final_answer]) + "\t" + str(logger[final_answer]) +  "\t" + characterModel.objectMap[second_response].answer + "\t" + str(best_responses[second_response]) + "\t" + str(logger[second_response]) +  "\t\t\t\n"

        # else:
        #     log_string = currentTime + "\t" + currentSession.currentAvatar + "\t" + query + "\t" + characterModel.objectMap[final_answer].answer + "\t" + str(best_responses[final_answer]) + "\t" + str(logger[final_answer]) +  "\t\t\t\t\t\t\n"


        # #print(log_string)
        # f.write(log_string)
        # f.close()
        if final_answer in currentSession.repetitions.keys():
            currentSession.repetitions[final_answer] += 1
        else:
            currentSession.repetitions[final_answer] = 1


    return characterModel.objectMap[final_answer]




# the player calls the following functions for greetings and silentVideos, using calls such as dialogue-manager3.sayHi(characterdict[avatar])

def silentVideos(corpus):
    return corpus["silences"]


def sayHi(corpus):
    return corpus["greetings"][0]


def sayBye(corpus):
    return corpus["greetings"][-1]


def create_new_session(avatar, language):
    print("creating a new session for " + avatar + " in " + language)

    if language == "English":
        f = open('english_log.tsv', 'a', encoding='utf-8')
    else:
        f = open('arabic_log.tsv', 'a', encoding='utf-8')
    log_string = "\t\t\t\t\t\t\t\t\t\t\n"
    f.write(log_string)
    f.close()
    return session(avatar, language)


def main():
    return


if __name__ == "__main__":



    for synset in wn.synsets("family"):
        for lemma in synset.lemmas():
                print(lemma.name())
    """ This is executed when run from the command line """
    main()
