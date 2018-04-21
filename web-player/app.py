# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect
import sys
import pprint

sys.path.insert(0, '/web-player/')
pprint.pprint(sys.path)

import dialogue_manager4
import logging


import os
app = Flask(__name__)

import click
click.disable_unicode_literals_warning = True

characterModel = {}
currentAvatar = ""
currentSession = None
currentLanguage = "English"

@app.route('/')
def index():

    global currentSession
    currentSession = dialogue_manager4.createModel(characterModel, currentSession, currentLanguage)
    return render_template('home.html')

@app.route('/main')
def individual_character_page():
    # initiates the model and a new session

    return render_template('main.html')

# THE FOLLOWING TWO FUNCTIONS ARE FOR EITHER TEXT AND SPEECH INPUT.
# PLEASE COMMENT OUT ONE OR ANOTHER TO TEST

# QUERYING ANSWER WITH TEXT INPUT
@app.route('/main', methods=['POST'])
def my_form_post():
    global currentSession
    text = request.form['text']
    processed_text = text

    currentSession = dialogue_manager4.determineAvatar(processed_text, currentSession)
    #currentSession = dialogue_manager4.create_new_session(avatar, language)

    response = dialogue_manager4.findResponse(processed_text, characterModel[currentSession.currentAvatar], currentSession)
    print("RESPONSE IS ",response)
    response_video_path = '/static/avatar-videos/' + response.videoLink.strip('"')
    response_subtitle_path = '/static/avatar-subtitle-timestamped/' + os.path.splitext(response.videoLink.strip('"'))[0] + '.vtt'

    return render_template('main.html',
                           avatar=currentSession.currentAvatar,
                           avatar_video_path=response_video_path,
                           avatar_response=response.answer,
                           avatar_subtitle=response_subtitle_path,
                           query_text=processed_text)

if __name__ == '__main__':
    avatar = ""
    #dialogue_manager4.readJsonFile(characterModel)
    StarMorphModules.read_config("config_dana.xml")
    StarMorphModules.initialize_from_file("almor-s31.db","analyze")
    app.run(debug=True,threaded=True)
