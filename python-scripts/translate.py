import json
from watson_developer_cloud import LanguageTranslatorV3

language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    iam_api_key='L0jCYJ5IpH9jLwG0og0xLrqhJHVxTf9SVpvspHAut49Z')


def translate(input_text, input_language, output_language):
	if input_language=="Arabic":
		translation_mode= 'ar-en'
	elif input_language== "English":
		translation_mode= 'en-ar'
	else:
		print("Translation not available for this language")


	translation = language_translator.translate(
	    text=input_text,
	    model_id=translation_mode)

	translated_text= json.dumps(translation["translations"][0]["translation"], indent=2, ensure_ascii=False)
	print(translated_text)

translate("اسمي دانة و أنا من الأردن", "Arabic", "English")