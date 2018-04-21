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
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

import ssl

import math

# from textblob import TextBlob as tb

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
stop_words = stopwords.words('english') + list(punctuation)

'''
Global Variables
'''
porterStemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Dictionary of all Avatars
characterdict = {}

# encoding
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
        self.questionsMap = {}


# The Structure for a video Object
class videoRecording:
    def __init__(self, question, answer, video, character, language):
        self.character = character
        self.question = question
        self.answer = answer
        self.videoLink = video
        self.language = language
        self.questionLength = len(question.split())
        self.answerLength = len(answer.split())

    def toString(self):
        print(self.id, ": ", self.character, "\n", self.question, "\n", self.answer, "\n", self.language, "\n")


# the structure of the session
class session:

    def __init__(self, avatar, language):
        self.repetitions = {}
        self.currentAvatar = avatar
        self.language = language


# find the intersection of two lists
def intersect(a, b):
    return list(set(a) & set(b))


# preprocessing for Arabic
def preprocess(line):
    processed = line.replace("؟", "")
    processed = processed.replace("أ", "ا")
    processed = processed.replace("إ", "ا")
    processed = processed.replace("ى", "ي")
    processed = processed.replace("ة", "ه")

    return processed

def arabicSyn():
	glossDict={}
	synonymDict={}
	unigram_synonyms_list = []

	f = open('static/scripts/all_characters.json', 'r', encoding='utf-8')

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
def createModel(characterdict, currentSession, mylanguage):
    # creates the new session
    currentSession = session('margarita', mylanguage)

    arabic_synonyms= arabicSyn()

    try:
        f = open('static/scripts/all_characters.json', 'r', encoding='utf-8')
    except IOError:
        print("Error: File does not appear to exist.")

    resp = json.load(f)
    # print(resp)

    # StarMorphModules.read_config("config_dana.xml")
    # StarMorphModules.initialize_from_file("almor-s31.db","analyze")

    totalQuestions = 0

    id_count = 0

    for i in range(0, len(resp["rows"]) - 1, 1):

        id_count += 1

        # If object is a queastion-answer pair, the relevant information is extracted
        if "english-question" in resp["rows"][i]["doc"].keys() or "arabic-question" in resp["rows"][i]["doc"].keys():
            totalQuestions += 1
            # do we wanna give it ID ourselves or use the JSON one?
            # uni_ID= json.dumps(resp["rows"][i]["doc"]["_id"])
            # print(uni_ID)
            video = json.dumps(resp["rows"][i]["doc"]["video"])
            # character= json.dumps(resp["rows"][i]["doc"]["character"])
            character = json.dumps(resp["rows"][i]["doc"]["video"]).split("_")[0].replace('"', '')
            # language= json.dumps(resp["rows"][i]["doc"]["language"])
            language = mylanguage
            ID = id_count;

        else:
            continue

        if (mylanguage == "Arabic" and "arabic-question" in resp["rows"][i]["doc"].keys() and "arabic-answer" in
                resp["rows"][i]["doc"].keys()):
            question = json.dumps(resp["rows"][i]["doc"]["arabic-question"], ensure_ascii=False).strip('،.؟"')
            answer = json.dumps(resp["rows"][i]["doc"]["arabic-answer"], ensure_ascii=False).strip('،.؟"')

        if (mylanguage == "English" and "english-question" in resp["rows"][i]["doc"].keys()):
            question = json.dumps(resp["rows"][i]["doc"]["english-question"]).strip(',?."!)')
            answer = json.dumps(resp["rows"][i]["doc"]["english-answer"]).strip(',?."!)')

        # Creates a new character model in the character dictionary if it does not exist already
        if character not in characterdict.keys():
            # characterdict[character] is the model of the respective character
            characterdict[character] = model()

        # adds to the character's questions list based on the character key; adds all videos regardless of type to questions
        obj = videoRecording(question, answer, video, character, language)
        characterdict[character].objectMap[ID] = obj

        # if the video is for silence
        if (answer == '""' and video != '""'):
            characterdict[character].fillers[ID] = obj

        else:
            characterdict[character].questionsMap[ID] = obj

        # stemming the question and answer and adding the stems, their bigrams and trigrams into model.stemmedMap
        if (mylanguage == "English"):

            unigram_split = question.lower().split() + answer.lower().split()
            unigram_list = [tmp.strip(',?."!)') for tmp in unigram_split]
            unigram_synonyms_list = []

            # expands the unigram model by adding synonyms
            for word in unigram_list:
                if word not in stop_words:
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
            for token in (unigram_list + unigram_synonyms_list):

                stem = porterStemmer.stem(token)
                lemma = lemmatizer.lemmatize(token)

                if token not in characterdict[character].wordMap.keys():
                    characterdict[character].wordMap[token] = {}
                if ID not in characterdict[character].wordMap[token]:
                    characterdict[character].wordMap[token][ID] = 1
                else:
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

        elif (mylanguage == "Arabic"):
        	
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
	            #print(token)
	            stem = StarMorphModules.analyze_word(token, False)[0].split()[1].replace("stem:", "").split('d',1)[0]
	            lemma = StarMorphModules.analyze_word(token, False)[0].split()[0].replace("lex:", "").split('_',1)[0]

	            if token not in characterdict[character].wordMap.keys():
	                characterdict[character].wordMap[token] = {}
	            if ID not in characterdict[character].wordMap[token]:
	                characterdict[character].wordMap[token][ID] = 1
	            else:
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

	        
    print("Total Questions: ", str(totalQuestions))
    print("done")
    # print(characterdict["gabriela"].wordMap)
    calculateTFIDF(characterdict)
    return currentSession


def direct_intersection_match_English(query, characterModel):
    queryList = [tmp.strip(', " ?.!)') for tmp in query.split()]
    responses = {}
    maxVal = 0
    # videoResponse= ''
    # newList = []

    # #expands the unigram model by adding synonyms
    # for word in queryList:
    # 	#if word not in stop_words:
    # 	for synset in wn.synsets(word):
    # 		for lemma in synset.lemmas():
    # 			if lemma.name() not in newList:
    # 				newList.append(lemma.name())

    for direct_string in queryList:
        if direct_string in characterModel.wordMap.keys():  # and direct_string not in stop_words:
            for vidResponse in characterModel.wordMap[direct_string]:
                if vidResponse not in responses.keys():
                    responses[vidResponse] = characterModel.wordMap[direct_string][vidResponse]
                elif vidResponse in responses.keys():
                    responses[vidResponse] += characterModel.wordMap[direct_string][vidResponse]

    for key, value in responses.items():

        if int(value) > maxVal:
            maxVal = int(value)
            videoResponse = key

    return responses


def stem_intersection_match_English(query, characterModel):
    stemmed_query = [porterStemmer.stem(tmp.strip(', " ?.!)')) for tmp in query.split()]

    responses = {}
    maxVal = 0
    videoResponse = ''

    for stem_string in stemmed_query:
        if stem_string in characterModel.stemmedMap.keys():
            for vidResponse in characterModel.stemmedMap[stem_string]:
                if vidResponse not in responses.keys():
                    responses[vidResponse] = characterModel.stemmedMap[stem_string][vidResponse]
                elif vidResponse in responses.keys():
                    responses[vidResponse] += characterModel.stemmedMap[stem_string][vidResponse]

    for key, value in responses.items():
        if int(value) > maxVal:
            maxVal = int(value)
            videoResponse = key

    return responses


def lemma_intersection_match_English(query, characterModel):
    lemmatized_query = [lemmatizer.lemmatize(tmp.strip(', " ?.!)')) for tmp in query.split()]

    responses = {}
    maxVal = 0
    videoResponse = ''

    for lemma_string in lemmatized_query:
        if lemma_string in characterModel.lemmatizedMap.keys():
            for vidResponse in characterModel.lemmatizedMap[lemma_string]:
                if vidResponse not in responses.keys():
                    responses[vidResponse] = characterModel.lemmatizedMap[lemma_string][vidResponse]
                elif vidResponse in responses.keys():
                    responses[vidResponse] += characterModel.lemmatizedMap[lemma_string][vidResponse]

    for key, value in responses.items():
        if int(value) > maxVal:
            maxVal = int(value)
            videoResponse = key

    return responses


def direct_intersection_match_Arabic(query, characterModel):
    queryList = [tmp.strip('،!؟."') for tmp in query.split()]
    # queryList.encode('utf-8')

    responses = {}
    maxVal = 0
    videoResponse = ''

    for direct_string in queryList:
        # print(direct_string)
        if direct_string in characterModel.wordMap.keys():
            for vidResponse in characterModel.wordMap[direct_string]:
                if vidResponse not in responses.keys():
                    responses[vidResponse] = 1
                elif vidResponse in responses.keys():

                    responses[vidResponse] += 1
            '''		
            if(characterModel.objectMap[vidResponse].answerLength):
                recall = responses[vidResponse]/(characterModel.objectMap[vidResponse].questionLength)
                precision= responses[vidResponse]/(characterModel.objectMap[vidResponse].questionLength+characterModel.objectMap[vidResponse].answerLength)
                #f-score
                responses[vidResponse]= responses[vidResponse]/((recall+precision)/2)
            '''
    for key, value in responses.items():

        if int(value) > maxVal:
            maxVal = int(value)
            videoResponse = key

    return responses

    for key, value in responses.items():
        # print(key, value)
        if int(value) > maxVal:
            maxVal = int(value)
            videoResponse = key
    # print("responses:" , responses)
    return responses


def stem_intersection_match_Arabic(query, characterModel):
    # StarMorphModules.read_config("config_stem.xml")
    # StarMorphModules.initialize_from_file("almor-s31.db","analyze")

    # print("Finding stem Intersection in Arabic")
    queryList = query.strip('؟!،" ً').split()
    responses = {}
    maxVal = 0
    videoResponse = ''
    stemmed_query = []

    for word in queryList:
        analysis = StarMorphModules.analyze_word(word, False)

        stemmed_query.append(analysis[0].split()[1].replace("stem:", "").split('d', 1)[0])

    for stem_string in stemmed_query:
        if stem_string in characterModel.stemmedMap.keys():
            for vidResponse in characterModel.stemmedMap[stem_string]:
                if vidResponse not in responses.keys():
                    responses[vidResponse] = 1
                elif vidResponse in responses.keys():
                    responses[vidResponse] += 1

    for key, value in responses.items():
        if int(value) > maxVal:
            maxVal = int(value)
            videoResponse = key
        value = value / len(query)

    return responses


def lemma_intersection_match_Arabic(query, characterModel):
    # print("Finding lemma Intersection in Arabic")
    queryList = query.strip('؟!.،" ً').split()
    # queryList.encode('utf-8')

    responses = {}
    maxVal = 0
    videoResponse = ''

    lemmatized_query = []
    for word in queryList:
        # print(word)
        analysis = StarMorphModules.analyze_word(word, False)
        lemma = analysis[0].split()[0].replace("lex:", "").split('_', 1)[0]
        lemma = re.sub(r'[^\u0621-\u064A]', '', lemma, flags=re.UNICODE)
        lemmatized_query.append(lemma)

    for lemma_string in lemmatized_query:
        if lemma_string in characterModel.lemmatizedMap.keys():
            for vidResponse in characterModel.lemmatizedMap[lemma_string]:
                if vidResponse not in responses.keys():
                    responses[vidResponse] = 1
                elif vidResponse in responses.keys():
                    responses[vidResponse] += 1

    for key, value in responses.items():
        if int(value) > maxVal:
            maxVal = int(value)
            videoResponse = key
        value = value / len(query)
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
        for lemma in characterdict[avatar].lemmatizedMap.keys():
            idf = totalDocs / len(characterdict[avatar].lemmatizedMap[lemma])
            for doc in characterdict[avatar].lemmatizedMap[lemma].keys():
                tf = characterdict[avatar].lemmatizedMap[lemma][doc]
                tfidf = tf * idf
                characterdict[avatar].lemmatizedMap[lemma][doc] = tfidf
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
                characterdict[avatar].stemmedMap[stem][doc] = tfidf

        for word in characterdict[avatar].wordMap.keys():
            idf = totalDocs / len(characterdict[avatar].wordMap[word])
            for doc in characterdict[avatar].wordMap[word].keys():
                tf = characterdict[avatar].wordMap[word][doc]
                tfidf = tf * idf
                characterdict[avatar].wordMap[word][doc] = tfidf


def rankAnswers(query, videoResponses, currentSession, characterModel):
    query_len = len(query.split())

    # each repition is a given a weight of 2 e.g if a video has been played once 2 points will be subtracted from its matching score

    # for each possible answer, checks if it has been played it already, and subtract points from its score if has been played already.
    for res in videoResponses:

        videoObjLen = characterModel.objectMap[res].questionLength + characterModel.objectMap[res].answerLength
        precision = videoResponses[res] / videoObjLen
        recall = videoResponses[res] / query_len
        f_score = (precision + recall) / 2

        if res in currentSession.repetitions.keys():
            negativePoints = currentSession.repetitions[res] * 0.4 * videoResponses[res]
            #videoResponses[res] -= negativePoints



    ranked_list = sorted(videoResponses, key=lambda i: videoResponses[i], reverse=True)
    return ranked_list[0]



def findResponse(query, characterModel, currentSession):
    # StarMorphModules.read_config("config_lex.xml")
    # StarMorphModules.initialize_from_file("almor-s31.db","analyze")
    language = currentSession.language
    themax = 0
    best_responses = {}
    stem_match_responses = {}
    lemma_match_responses = {}
    direct_match_responses = {}

    query = query.lower().strip(',?.")!')

    if language == "English":
        # different modes of matching
        stem_match_responses = stem_intersection_match_English(query, characterModel)
        lemma_match_responses = lemma_intersection_match_English(query, characterModel)
        direct_match_responses = direct_intersection_match_English(query, characterModel)

    elif language == "Arabic":
        stem_match__responses = stem_intersection_match_Arabic(query, characterModel)
        lemma_match_responses = lemma_intersection_match_Arabic(query, characterModel)
        direct_match_responses = direct_intersection_match_Arabic(query, characterModel)
    else:
        print("language not recognsed")
        return

    for key in stem_match_responses.keys():
        if key not in best_responses.keys():
            best_responses[key] = stem_match_responses[key]

    for key in lemma_match_responses.keys():
        if key not in best_responses.keys():
            best_responses[key] = lemma_match_responses[key]
        else:
            best_responses[key] += lemma_match_responses[key]

    for key in direct_match_responses.keys():
        if key not in best_responses.keys():
            best_responses[key] = direct_match_responses[key]
        else:
            best_responses[key] += direct_match_responses[key]

    # if the responses are empty, play "I can't answer that response"
    if bool(best_responses) == False:
        if currentSession.currentAvatar == "gabriela":
            final_answer = 798
        elif currentSession.currentAvatar == "margarita":
            final_answer = 618
        else:
            final_answer = 746


    else:
        final_answer = rankAnswers(query, best_responses, currentSession, characterModel)
        if final_answer in currentSession.repetitions.keys():
            currentSession.repetitions[final_answer] += 1
        else:
            currentSession.repetitions[final_answer] = 1

    return characterModel.objectMap[final_answer]


def determineAvatar(query, currentSession):
    if currentSession.currentAvatar == "":
        currentSession = session("margarita", currentSession.language)

    # Changes the avatar

    if query == "toya toya can i talk to margarita":
        currentSession = session("margarita", currentSession.language)

    if query == "toya toya can i talk to katarina":
        print("you are switching to katarina")
        currentSession = session("katarina", currentSession.language)

    if query == "toya toya can i talk to gabriela":
        currentSession = session("gabriela", currentSession.language)

    if query == "toya toya can i talk to gabriella":
        currentSession = session("gabriela", currentSession.language)

    if query == "toya toya can i talk to someone else":
        print("you are switching to gabriela")
        currentSession = session("gabriela", currentSession.language)

    return currentSession


# the player calls the following functions for greetings and silentVideos, using calls such as dialogue-manager3.sayHi(characterdict[avatar])

def silentVideos(corpus):
    return corpus["silences"]


def sayHi(corpus):
    return corpus["greetings"][0]


def sayBye(corpus):
    return corpus["greetings"][-1]


def create_new_session(avatar, language):
    return session(avatar, language)


def main():
    return


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
