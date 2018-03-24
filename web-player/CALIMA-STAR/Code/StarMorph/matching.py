str.encode('utf-8')
import StarMorphModules



matches= []

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

''' all matching functions need to only return the matched question to Ming's system'''

def direct_intersection_match_Arabic(query, questionArray):
    maximumSize = 0
    matchedQuestion = ""
	#matchedObject = videoRecording(1000, "query", "No response found")
    query.encode('utf-8')
    query.strip('؟')	
    for question in questionArray:
		# finds the intersection between the words in query and the set of words in each object's question and answer
            output = "".join(c for c in question if c not in ('!','.',':', '’' , '“', '”', '?'))
            if(isArabic(output)==True):
                question= preprocess(output)
		
                intersection = intersect(query, question)
		
                if len(intersection) > maximumSize:
                    maximumSize = len(intersection)
                    matchedQuestion=question
                    matches.append(question)
			
    return matchedQuestion

def stem_intersection_match_Arabic(query, question_array):
    maximumSize = 0
    matchedQuestion = ""
	#matchedObject = videoRecording(1000, "query", "No response found")
    query.encode('utf-8')
    query.strip('؟')
    StarMorphModules.read_config("/Users/student/Desktop/Senior year/Capstone/January 2017/CALIMA-STAR/Code/StarMorph/config_stem.xml")
    StarMorphModules.initialize_from_file("/Users/student/Desktop/Senior year/Capstone/January 2017/CALIMA-STAR/Code/StarMorph/almor-s31.db","analyze")

    output = "".join(c for c in query if c not in ('!','.',':', '’' , '“', '”', '?'))
    if(isArabic(output)==True):
            query= preprocess(output)

    stemmedQuery= ""
    for word in query.split():

        analyzedQuery=StarMorphModules.analyze_word(word,False)
        stemQuery=(analyzedQuery[0].replace("stem:", ""))
        stemmedQuery+=" "+stemQuery
    print(stemmedQuery)
    
    for question in question_array:
        stemmedQuestion= ""
        output = "".join(c for c in question if c not in ('!','.',':', '’' , '“', '”', '?'))
        if(isArabic(output)==True):
            question= preprocess(output)

            for word in question:
                analyzedQuestion= StarMorphModules.analyze_word(word,False)
                stemQuestion=(analyzedQuery[0].replace("stem:", ""))
                stemmedQuestion+=" "+stemQuestion

                   
            intersection = intersect(stemmedQuery, stemmedQuestion)
		
            if len(intersection) > maximumSize:
                maximumSize = len(intersection)
                matchedQuestion=question
                matches.append(question)
			
    return matchedQuestion

def lemma_intersection_match_Arabic(query, question_array):
    maximumSize = 0
    matchedQuestion = ""
	#matchedObject = videoRecording(1000, "query", "No response found")
    query.encode('utf-8')
    query.strip('؟')
    StarMorphModules.read_config("/Users/student/Desktop/Senior year/Capstone/January 2017/CALIMA-STAR/Code/StarMorph/config_lex.xml")
    StarMorphModules.initialize_from_file("/Users/student/Desktop/Senior year/Capstone/January 2017/CALIMA-STAR/Code/StarMorph/almor-s31.db","analyze")

    output = "".join(c for c in query if c not in ('!','.',':', '’' , '“', '”', '?'))
    if(isArabic(output)==True):
            query= preprocess(output)

    lexQuery= ""
    for word in query.split():

        analyzedQuery=StarMorphModules.analyze_word(word,False)
        lemmatizedQuery=(analyzedQuery[0].replace("lex:", ""))
        lemmatizedQuery=lemmatizedQuery.strip("1_")
        lexQuery+=" "+lemmatizedQuery
    print(lexQuery)
    
    for question in question_array:
        lexQuestion= ""
        output = "".join(c for c in question if c not in ('!','.',':', '’' , '“', '”', '?'))
        if(isArabic(output)==True):
            question= preprocess(output)

            for word in question:
                analyzedQuestion= StarMorphModules.analyze_word(word,False)
                lexQuestion=(analyzedQuery[0].replace("stem:", ""))
                lexQuestion+=" "+stemQuestion

                   
            intersection = intersect(lexQuery, lexQuestion)
		
            if len(intersection) > maximumSize:
                maximumSize = len(intersection)
                matchedQuestion=question
                matches.append(question)
			
    return matchedQuestion

def direct_intersection_match_English(query, questionArray):
    print("Finding Direct Intersection direct_intersection_match")
    maximumSize = 0
    matchAnswer = ""
    matchedObject = videoRecording(1000, "query", "No response found")
    for question in questionArray:
        # finds the intersection between the words in query and the set of words in each object's question and answer
        intersection = intersect(query, question)
        
        if len(intersection) > maximumSize:
            maximumSize = len(intersection)
            #matchAnswer = obj.answer
            #matchedObject = obj
            matchedQuestion=question
            matches.append(question)

    print("THis is the matched question: ", matchedQuestion)
    return matchedQuestion
    print("I have returned matched question.")

            
  ''' These are your original matching functions, they need to be defined 
  so that they compare each question in the questions array with the query
  instead of the object we created in the original code because we don't have that anymore.
  Check how I did it for the Arabic '''  

def stem_intersection_match_English(query):
    print("Finding Porter Stemmed Intersection")
    maximumSize = 0
    matchAnswer = ''''''
    matchedObject = videoObj(1000, "query", "No response found")
    # creates a set of stemmed words in query
    queryStemmedList = [porterStemmer.stem(tmp) for tmp in query.split() ]
    for obj in questionCorpus:
        # creates a set of stemmed words in each object's question and answers 
        objStemmedList = [porterStemmer.stem(tmp) for tmp in obj.question.split() ] + [porterStemmer.stem(tmp) for tmp in obj.answer.split() ]
        #finds the intersection between each set and the query
        intersection = set(queryStemmedList) & set(objStemmedList)
        if len(intersection) > maximumSize:
            maximumSize = len(intersection)
            matchAnswer = obj.answer
            matchedObject = obj
            #print(intersection)    
    obj.toString()

def lemma_intersection_match_English(query):
    print("Finding Word Net Lemmatizer Intersection")
    maximumSize = 0
    matchAnswer = ""
    matchedObject = videoObj(1000, "query", "No response found")
    # creates a set of lemmatized words in query
    queryLemmatizedList = [lemmatizer.lemmatize(tmp) for tmp in query.split() ]
    for obj in questionCorpus:
        # creates a set of lemmatized words in each object's question and answers 
        objLemmatizedList = [lemmatizer.lemmatize(tmp) for tmp in obj.question.split() ] + [lemmatizer.lemmatize(tmp) for tmp in obj.answer.split() ]
        #finds the intersection between each set and the query
        intersection = set(queryLemmatizedList) & set(objLemmatizedList)
        if len(intersection) > maximumSize:
            maximumSize = len(intersection)
            matchAnswer = obj.answer
            matchedObject = obj
            print(intersection) 
    matchedObject.toString()


#lemma_intersection_match_Arabic("أين تعيشين ", matches)

def main(query, question_array):
    questionsAsked=0
    readFile(sourceFile)
    #while(True):
    #
    #query = input("What do you want to ask Paula?")    
    questionsAsked +=1

    print(question_array)
    match= direct_intersection_match_English(query, question_array)
    print("This is match in main: ", match)
    return match
    #evaluate(questionsAsked, len(matches))
    #stem_intersection_match_Arabic(query, questionsAsked, matches)
    #lemma_intersection_match(query)


'''' Main Function gets the query from Ming's system and the 
questions in the db as an array  '''
if __name__ == "__main__":
    """ This is executed when run from the command line """
    main(query, question_array) 
