import json

import sys

import unicodedata
import codecs

from watson_developer_cloud import LanguageTranslatorV3



language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    iam_api_key='L0jCYJ5IpH9jLwG0og0xLrqhJHVxTf9SVpvspHAut49Z')


def translate(input_text, translation_mode):

	translation = language_translator.translate(
	    text=input_text,
	    model_id=translation_mode)

	translated_text= json.dumps(translation["translations"][0]["translation"], indent=2, ensure_ascii=False)
	return translated_text.strip('"').replace("(", " ").replace(")", " ")
	#print(translated_text)


def addTranslation():
	input_filename= sys.argv[1]
	script= open(input_filename, 'r', encoding='utf-8')
	translation_mode= sys.argv[2]
	output_filename= sys.argv[3]

	

	
	data= json.load(script)

	for i in range(0, len(data["rows"]) - 1, 1):
		if (translation_mode== 'ar-en'):
			input_question= data["rows"][i]["doc"]["arabic-question"]
			output_question= translate(input_question, translation_mode)
			data["rows"][i]["doc"]["english-question"]= output_question
			input_answer= data["rows"][i]["doc"]["arabic-answer"]
			output_answer= translate(input_answer, translation_mode)
			data["rows"][i]["doc"]["english-answer"]= output_answer
		elif(translation_mode== 'en-ar'):
			input_question= data["rows"][i]["doc"]["english-question"]
			output_question= translate(input_question, translation_mode)
			#print("output_question", output_question)
			data["rows"][i]["doc"]["arabic-question"]= output_question
			input_answer= data["rows"][i]["doc"]["english-answer"]
			output_answer= translate(input_answer, translation_mode)
			#print("output_answer", output_answer)
			data["rows"][i]["doc"]["arabic-answer"]= output_answer

	with open(output_filename,"w") as outfile:
	    json_data = json.dumps(data)
	    outfile.write(json_data)

	# f = open("script2.json", "r")

	# resp = json.load(f)


	# with codecs.open(output_filename, 'w', encoding='utf-8') as json_file:
	#     json.dump(resp, json_file, ensure_ascii=False,indent=4)

	#f.close()

addTranslation()

