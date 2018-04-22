# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import sys
import pprint

sys.path.insert(0, '/web-player/')
pprint.pprint(sys.path)

import dialogue_manager4
import StarMorphModules

import os
app = Flask(__name__)

import click
click.disable_unicode_literals_warning = True

characterModel = {}
currentAvatar = ""
currentSession = None


# Home page where you go to select an avatar
@app.route('/')
def home():
    return render_template('choose_avatar.html')


# Page where you go to select a language
@app.route('/<avatar>')
def with_avatar(avatar):
    return render_template('choose_language.html', avatar=avatar)


# Starting page for each character
@app.route('/<avatar>/<language>')
def with_language(avatar, language):
    global currentSession
    global characterModel
    language = str(language).title()
    dialogue_manager4.createModel(characterModel, currentSession, language)
    currentSession = dialogue_manager4.create_new_session(avatar, language)
    return render_template('main.html', avatar=avatar, language=language)


# When avatar page receives a POST request
@app.route('/<avatar>/<language>', methods=['POST'])
def my_form_post(avatar,language):
    global currentSession
    text = request.form['text']
    processed_text = text

    response = dialogue_manager4.findResponse(processed_text, characterModel[avatar], currentSession)
    print("RESPONSE IS ", response)
    response_video_path = '/static/avatar-videos/' + response.videoLink.strip('"')

    # response_subtitle_path = '/static/avatar-subtitle-timestamped/' + os.path.splitext(response.videoLink.strip('"'))[0] + '.vtt'

    response_subtitle_path = '/static/avatar-subtitle-timestamped/' + language + '_' + os.path.splitext(response.videoLink.strip('"'))[0] + '.vtt'


    return render_template('main.html',
                           avatar=avatar,
                           avatar_video_path=response_video_path,
                           avatar_response=response.answer,
                           avatar_subtitle=response_subtitle_path,
                           query_text=processed_text,
                           language=language)


if __name__ == '__main__':
    avatar = ""
    StarMorphModules.read_config("config_dana.xml")
    StarMorphModules.initialize_from_file("almor-s31.db", "analyze")
    app.run(debug=True,threaded=True)