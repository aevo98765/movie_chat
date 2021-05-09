# Instructions to run locally
These are instructions for Movie Chat to run the chat locally
## 1. Set-up virtual environment 

First you need to install *virtualenv* in order to set-up your python virtual environment:

`pip install virtualenv`

And set your python virtual enviroment by:

`virtualenv myvirtualenv`
mac os
`source myvirtualenv/bin/activate`
windows
`myvirtualenv\Scripts\activate`


Finally, install all required packages into your environment:

`pip install -r requirements.txt`

## 2. Run the application

To run:

`python app.py`

Go to your browser and type *http://localhost:5000/*.

Create a account and start chatting!

## 2. Run the movie bots

Navigate to chatbot/film_scene.py

On lines 57-59 the script and chat room are entered into the new Film_scene object. Choose what movie script (listed in chatbot/movie_dialogue/) you would like to be acted out and in what chat room number. Why not join the actors and contribute to the movie.

Navigate back to ./movie_chat and type the command 'python chatbot/film_scene.py

If chromedriver related issues occur redownload this from the offcial website for the current version of chrome you have.
