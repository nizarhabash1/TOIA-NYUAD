The TOIA Recorder is a tool through which you can create a bilingual avatar consisting of recorded videos. 

In order to set up the recorder, you must first open the terminal and cd into the web-recorder directory:

*cd path-to-directory-where-TOIA-is-installed/TOIA-NYUAD/web-recorder*

## Prerequisites

In order to be able to run the app, you must first [install NodeJS](https://nodejs.org/en/).

After installing NodeJS, you must then install the Nodemon package by running the following command:

*npm install -g nodemon*

The final command in order to be able to run the recorder is:

*npm install*

This will install all the required packages.

## Running the Recorder

Once all the prerequisite steps have been fulfilled, you can now access the recorder by running:

*nodemon app.js*

## Creating an avatar

You can now access *localhost:3000* and should see a page that gives you two avatar types: editing a previously created avatar and creating a new avatar.

### Create new avatar

Select the "Create new avatar" option and then click submit. You can then pick a name for your avatar. If a name has been used before, you will be asked to enter a different one. This avatar will then be stored as a directory named after the avatar in public/avatar-garden within the web-recorder directory where everything related to that avatar will be stored.

#### Pick script type

After entering the name, you will be asked what kind of script you would like to use for your avatar. You can choose to start an avatar from scratch, start with a factual template or start with a narrative template. All of these tempates include sample questions and answers which will aid you in creating your avatar. Once you've selected your template, you can click on the submit button. 

#### The recorder page

You will now be directed to the recorder page, where you will be presented with a list of questions and answers which you can modify either by editing the current questions and answers, removing them, or creating new ones. In order for a script to be saved, you must click on the "Save Script" button which will store your list of questions and answers and recorded videos in your avatar directory. 

#### Editing options for question-answer pairs

Under each question and answer you have three buttons: UPDATE, DELETE, SAVE. The UPDATE button displays all of the information stored under each question and answer pairs and allows you to edit these attributes. The information displayed includes:

- English question: the English version of the question.
- English answer: the English version of the answer.
- Arabic question: the Arabic version of the question (this translation can be obtained through a step described under "Additional Scripts")
- Arabic answer: the Arabic version of the answer 
- Playing frequency (never/once/multiple): this variable is used to control how often a recorded video will be played while a user interacts with the avatar. You can set it to never, meaning that it will never play, once, meaning that it will only play once, or multiple, meaning that it could play multiple times during a user's interaction with it (when relevant). If you would rather not specify the frequency, it will automatically be set to multiple.

#### Global editing options

You also have the option of editing the global attributes of the script by clicking the "Edit global variables" button underneath the script. This will allow you to modify the following attributes: 

- Language (Arabic/English): choose the language that the avatar is recorded in
- Minimum required accuracy (low/medium/high): This value is used as a threshold for accuracy. For example, if you require videos to be played only when there is a high match, then select "High". Otherwise, select either "Low" or "Medium". The default value is "Low".
- Length constant: (0-70) if the number of words in an answer is above this constant, then these answers will be ranked lower in our question-answer matching algorithm. We recommend you keep this value at 40.

#### Recording answer videos

In order to record a video which will be linked to a question and answer pair, you must first select a pair from the left of the screen by clicking on it. Once you've done so, you can press the record button under the recording screen. This will activate the recorder and allow you to record a video. Try to say exactly what you specified in the text answer for your question, as the matching will be based on the text answer. You can also modify the text answer after recording by clicking the UPDATE button. Once you are happy with the recorded video, click on the SAVE button of the respective question and answer pair. 

#### Saving the script

Don't forget to click the "Save Script" button after you're done recording. It's recommended to save frequently in case the recorder crashes.

#### Adding/removing question-answer pairs
If you want to add a new question-answer pair/a filler/ or a "no answer" type entry, select the respective option from the form under the list of questions and answers, then fill in the required input. The new entry will automatically show up in the list. In order to remove a question-answer pair, just click on the DELETE button.

### Edit previously created avatar

If you have previously created an avatar, you can access it through the same recorder interface by clicking on the "Edit previously created avatar" button, selecting the avatar you want to work on from the list of avatars (which is a list of directories stored under public/avatar-garden in the recorder) and then following the same steps described above.

## Additional scripts for translating and adding subtitles

If you would like to enhance your avatar by adding translations and subtitles, follow the steps below:

- access the Terminal
- *cd path-to-directory-where-TOIA-is-installed/TOIA-NYUAD/python-scripts*
- in order to generate translations to Arabic within your script, run: *python3 translate.py avatar_name en-ar*. If your script is in Arabic and you would like to generate English translations, run *python3 translate.py avatar_name ar-en*. The avatar_name is the name of your avatar (which is also the name of the directory storing your avatar under avatar-garden). The script with the translated entries will replace your former script file. If you would like to access the previous version of your script, it will be stored under script.json.old within your avatar directory.
- in order to generate subtitles to be used when displaying your videos in the player, run: *python3 generateTimestampedSubtitle.py avatar_name*. This will store subtitles under the subtitles directory in your avatar in the avatar garden.
