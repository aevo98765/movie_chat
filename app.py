from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
import json
import os
from datetime import datetime

from sentiment_handler import *
from json_handeler import json_handeler as jh

jh.initialise_repos()

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

socketio = SocketIO(app, manage_session=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    chat_filename = './json_data/chat_participant_list.txt'
    rooms = jh.getActiveRooms(chat_filename)

    if (request.method == 'POST'):
        room = request.form['room']
        username=request.form['username']
        password=request.form['password']
        users_filename = './json_data/users/registered_users.txt'

        if os.path.exists(users_filename):
            with open(users_filename) as fusers:
                users = json.load(fusers)
        else:
            flash('Login Failed - User and/or password are incorrect.', 'danger')
            return redirect(url_for('index'))

        if (username not in users.keys()) or (users[username] != password):
            flash('Login Failed - User and/or password are incorrect.', 'danger')
            return redirect(url_for('index'))


        if room in rooms.keys():
            if username in rooms[room]:
                flash('Login Failed - A user with username ' +
                username + ' already exists in Room ' + room + '.', 'danger')
                return redirect(url_for('index'))
            else:
                rooms[room].append(username)
        else:
            rooms[room] = []
            rooms[room].append(username)

        jh.update_chat_participants(chat_filename,rooms)
        # Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session=session)
    else:
        flash('Please login first', 'danger')
        return redirect(url_for('index'))


@app.route('/create_account', methods=['GET','POST'])
def create_account():
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        users = {}

        filename = './json_data/users/registered_users.txt'
        if os.path.exists(filename):
            with open(filename) as fusers:
                users = json.load(fusers)
        else:
            if not os.path.exists('./json_data'):
                os.makedirs('json_data')
                os.makedirs('./json_data/users')
            else:
                if not os.path.exists('./json_data/users'):
                    os.makedirs('./json_data/users')

        if (username in users.keys()):
            flash('Not able to create account - A user with username ' + username + ' already exists.', 'danger')
            return redirect(url_for('create_account'))
        else:
            users[username] = password

        with open(filename, 'w') as fusers:
            json.dump(users, fusers)
            flash('Account created successfully!', 'success')

        print('Im in the right place!')
        return render_template('create_account.html')
    else:
        return render_template('create_account.html')

@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    if not os.path.exists('json_data/rooms/room' + str(room)):
        os.makedirs('json_data/rooms/room' + str(room))
    emit('status', {'msg': session.get('username') + ' has entered the room.', 'username ': session.get('username')},
         room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    username = message['username']
    time = datetime.now()
    date_time = time.strftime("%m/%d/%Y, %H:%M:%S")

    filename = './json_data/messages/messagesJSON' + str(room) + '.txt'
    room_filename = './json_data/rooms/room' + str(room) + '/roomJSON' + str(room) + '.txt'

    message_sentiment = getSentiment(message['msg'])
    room_sentiment = jh.getNewAveRoomSentiment(room_filename,message_sentiment)



    message_json_data = {"room": room,
                "username": message['username'],
                "message_string": message['msg'],
                "sentiment_score": message_sentiment,
                "time": date_time}

    room_json_data = {"room": room,
                         "sentiment_score": room_sentiment,
                         "time": date_time}

    filename = './json_data/messages/messagesJSON' + str(room) + '.txt'

    room_filename = './json_data/rooms/room' +str(room) + '/roomJSON' + str(room) + '.txt'

    room_score_filename = 'json_data/chat_live_room_scores.txt'

    participant_score_filename = 'json_data/chat_live_participant_scores.txt'

    jh.update_file(filename,message_json_data)

    jh.update_file(room_filename, room_json_data)


    messages_filename = './json_data/messages/messagesJSON' + str(room) + '.txt'
    participant_sentiment = jh.username_sentiment_calculation(messages_filename, username)
    jh.update_live_participant_scores(participant_score_filename, username, participant_sentiment)
    jh.update_live_room_scores(room_score_filename, room, room_sentiment)

    safe_message = filterProfanity(message['msg'])
    emit('message', {'username': message['username'], 'msg': safe_message,"sentiment":message_sentiment, "average_sentiment":room_sentiment, 'date_time':date_time}, room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = message['username']
    time = datetime.now()
    date_time = time.strftime("%m/%d/%Y, %H:%M:%S")
    messages_filename = './json_data/messages/messagesJSON' + str(room) + '.txt'

    sentiment_score = jh.username_sentiment_calculation(messages_filename, username)
    user_sentiment_json = {"username": username,
                            "average_sentiment": sentiment_score,
                            "room":room,
                            "leaving_time": date_time}

    user_filename = './json_data/users/userJSON' + str(username) + '.txt'
    chat_participants_filename = './json_data/chat_participant_list.txt'
    room_score_filename = 'json_data/chat_live_room_scores.txt'

    jh.update_file(user_filename,user_sentiment_json)
    rooms = jh.getActiveRooms(chat_participants_filename)

    jh.delete_chat_participant(chat_participants_filename,username,room)


    if room not in rooms.keys():
        jh.delete_live_room_scores(room_score_filename, room)

    leave_room(room)
    # session.clear()
    emit('status', {'msg': username + ' has left the room.' + "\n They had an average sentiment score of: " + str(sentiment_score)}, room=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
