#### Set up virtual env
Inside this directory, do `virtualenv venv` and `. venv/bin/activate`
For more instruction on virtual env, checkout https://help.pythonanywhere.com/pages/RebuildingVirtualenvs/

#### Upload avatar videos
Create a folder `avatar-videos` under `/static` directory and upload all avatar videos there

#### Export and run flask app
Do `export FLASK_APP=app.py` and `flask run` inside venv

Go to http://127.0.0.1:5000/ to view the application

#### TODO

- Checkout other speech recognition library for Arabic integration
- Display text of speech recognition
- Loop of filler videos at the beginning and in between
- Style the web player
