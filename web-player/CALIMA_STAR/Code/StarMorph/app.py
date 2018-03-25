from flask import Flask, render_template, request, redirect
import dialogue_manager4
import logging
import os
app = Flask(__name__)

import click
click.disable_unicode_literals_warning = True

characterModel = {}
currentAvatar = ""

@app.route('/')
def default_page():
    return render_template('index.html')

# THE FOLLOWING TWO FUNCTIONS ARE FOR EITHER TEXT AND SPEECH INPUT.
# PLEASE COMMENT OUT ONE OR ANOTHER TO TEST

# QUERYING ANSWER WITH TEXT INPUT
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text
    dialogue_manager4.createModel(characterModel)

    global currentAvatar
    tmpAvatar = dialogue_manager4.determineAvatar(processed_text, currentAvatar)
    currentAvatar = tmpAvatar

    response = dialogue_manager4.findResponse(processed_text, characterModel[currentAvatar])
    response_video_path = '/static/avatar-videos/' + response.videoLink.strip('"')
    response_subtitle_path = '/static/avatar-subtitle-timestamped/' + os.path.splitext(response.videoLink.strip('"'))[0] + '.vtt'

    return render_template('index.html',
                           avatar = currentAvatar,
                           avatar_video_path= response_video_path,
                           avatar_response=response.answer,
                           avatar_subtitle = response_subtitle_path,
                           query_text = processed_text)

if __name__ == '__main__':
    avatar = ""
    dialogue_manager4.readJsonFile(characterModel)
    app.run(debug=True,threaded=True)
