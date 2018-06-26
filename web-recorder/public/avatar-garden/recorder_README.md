The TOIA Recorder is a tool through which you can create an avatar consisting of recorded videos. 

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

Select the "Create new avatar" option and then click submit. You can then pick a name for your avatar. If a name has been used before, you will be asked to enter a different one. After entering the name, you will be asked what kind of script you would like to use for your avatar. You can choose to start an avatar from scratch, start with a factual template or start with a narrative template. All of these tempates include sample questions and answers which will aid you in creating your avatar. Once you've selected your template, you can click on the submit button. You will now be directed to the recorder page, where you will be presented with a list of questions and answers which you can modify either by editing the current questions and answers, removing them, or creating new ones. In order for a script to be saved, you must click on the "Save Script" button which will store your list of questions and answers and recorded videos in your avatar directory. 

Under each question and answer you have three buttons: UPDATE, DELETE, SAVE. The UPDATE button displays all of the information stored under each question and answer pairs and allows you to edit these attributes. The information displayed includes:

- English question: the English version of the question.
- English answer: the English version of the answer.
- Arabic question: the Arabic version of the question (this translation can be obtained through a step described under "Additional Scripts")
- Arabic answer: the Arabic version of the answer 
- Playing frequency (never/once/multiple): this variable is used to control how often a recorded video will be played while a user interacts with the avatar. You can set it to never, meaning that it will never play, once, meaning that it will only play once, or multiple, meaning that it could play multiple times during a user's interaction with it (when relevant). If you would rather not specify the frequency, it will automatically be set to multiple.
- Minimum required accuracy (low/medium/high): This value is used as a threshold for accuracy. If you require videos to be played only when there is a high match, then select "High", if you 
- Length constant: 

### Edit previously created avatar
