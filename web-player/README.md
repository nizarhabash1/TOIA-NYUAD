#### Set up virtual env
Run `virtualenv venv` and `. venv/bin/activate`

For more instruction on virtual env, checkout https://help.pythonanywhere.com/pages/RebuildingVirtualenvs/

#### Upload avatar videos
Create a folder `avatar-videos` under `/static` directory and upload all avatar videos there

#### Export and run flask app
Run `python3 app.py`

Go to http://127.0.0.1:5000/ to view the application

#### Dialogue Manager TODO
- Make sure direct matching works when the query is exactly the same
- For question type of reply list to something something, write customized matching for them. For example, there should be a better way of matching "Reply list to 'when somebody asks how I found something': Examples: And did you like it? / Was it fun? / How was it? / How did you find x? / What did you think? / Was it nice? (because usually talk about my past experiences which were good anyway" than direct matching

#### Interaction Design TODO
- Loop of filler videos at the beginning and in between
- Style the web player
- If possible, let speech recognition engine recognize NYUAD
