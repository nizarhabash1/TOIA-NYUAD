import json

import sys

import unicodedata
import codecs

import copy

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
	avatar_name= sys.argv[1]
	input_filename= "../web-recorder/public/avatar-garden/" + avatar_name + "/script.json"
	script= open(input_filename, 'r', encoding='utf-8')

	translation_mode= sys.argv[2]

	try:
		script= open(input_filename, 'r', encoding='utf-8')
		print("Reading from file " + input_filename + " successful")

	except IOError:
		print("Error: File does not appear to exist.")
	

	old_data=json.load(script)
	data= copy.deepcopy(old_data)

	try:
		print("translating...")
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

		output_filename= input_filename
		with open(output_filename,"w") as outfile:
		    json_data = json.dumps(data)
		    outfile.write(json_data)

		old_file= input_filename+ ".old"
		#print(old_data)
		with open(old_file,"w") as old_outfile:
		    old_json_data = json.dumps(old_data)
		    old_outfile.write(old_json_data)
		print("translation completed successfully")

	except:
		print("Error: translation failed")




	

	# f = open("script2.json", "r")

	# resp = json.load(f)


	# with codecs.open(output_filename, 'w', encoding='utf-8') as json_file:
	#     json.dump(resp, json_file, ensure_ascii=False,indent=4)

	#f.close()

addTranslation()

