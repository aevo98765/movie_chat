import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from errors.user_exceptions import InvalidUserNameError


def initialise_repos():
    if not os.path.exists('json_data'):
        os.makedirs('json_data')
    if not os.path.exists('json_data/messages'):
        os.makedirs('json_data/messages')
    if not os.path.exists('json_data/rooms'):
        os.makedirs('json_data/rooms')
    if not os.path.exists('json_data/users'):
        os.makedirs('json_data/users')

def username_sentiment_calculation(filename,username):
    try:
        message_number = 0
        total_sentiment = 0
        if os.path.isfile(filename):
            with open(filename) as f_with_json:
                existing_json = json.load(f_with_json)
                for message in existing_json:
                    try:
                        message_username = message['username']
                        sentiment_score = message['sentiment_score']

                        if username == message_username:
                            message_number += 1
                            total_sentiment += sentiment_score
                    except:
                        pass
        else:
            message_number=1
            total_sentiment = 0.5

        if message_number == 0:
            raise InvalidUserNameError
        return total_sentiment/message_number
    except:
        print("Username not present")
        

def update_file(filename, json_data):
    empty = []
    if not os.path.isfile(filename):
        empty.append(json_data)
        with open(filename, 'w+') as f:
            f.write(json.dumps(empty, indent=2))
    else:
        with open(filename) as f_with_json:
            existing_json = json.load(f_with_json)

        existing_json.append(json_data)
        with open(filename, mode='w') as f:
            f.write(json.dumps(existing_json, indent=2))

def getNewAveRoomSentiment(room_filename,newVal):
    if not os.path.isfile(room_filename):
        return 0.5*0.75+newVal*0.25

    else:
        with open(room_filename) as json_file:
            data = json.load(json_file)

            room_sentiment = data[-1]['sentiment_score']

    return room_sentiment*0.75 + newVal*0.25

def update_chat_participants(filename,rooms):
    with open(filename, 'w') as f_with_participants:
        json.dump(rooms, f_with_participants)


def delete_chat_participant(filename,username,room):
    if os.path.exists(filename):
        with open(filename) as f_with_participants:
            rooms = json.load(f_with_participants)

    rooms[room].remove(username)
    
    if len(rooms[room]) == 0:
        del rooms[room]

    with open(filename, 'w') as f_with_participants:
        json.dump(rooms, f_with_participants)

def getActiveRooms(filename):
    rooms = {}
    if os.path.exists(filename):
        with open(filename) as f_with_participants:
            rooms = json.load(f_with_participants)
    return rooms

def getRoomWithMostParticipants(filename):
    try:
        with open(filename) as f_with_participants:
            rooms = json.load(f_with_participants)
        mx = max(len(room) for room in rooms.values())
        k = [key for key, value in rooms.items() if len(value) == mx]
        return k[0], mx
    except:
        filename_stats_record = "./json_data/stats_record.txt"
        if os.path.exists(filename_stats_record ):
            with open(filename_stats_record) as f_stats_record:
                stats_record = json.load(f_stats_record)
                return stats_record["most_popular_room"][0], stats_record["most_popular_room"][1]
        else:
            return '-', 0

def  getRoomWithHighestSentimentScore(filename):
    try:
        with open(filename) as f_live_room_scores:
            rooms = json.load(f_live_room_scores)
        itemMaxValue = max(rooms.items(), key = lambda x: x[1])
        listOfKeys = list ()
        for key, value in rooms.items():
            if value == itemMaxValue[1]:
                listOfKeys.append(key)
        return listOfKeys[0], itemMaxValue[1]
    except:
        filename_stats_record = "./json_data/stats_record.txt"
        if os.path.exists(filename_stats_record ):
            with open(filename_stats_record) as f_stats_record:
                stats_record = json.load(f_stats_record)
                return stats_record["happiest_room"][0], stats_record["happiest_room"][1]
        else:
            return '-', 0

def  getRoomWithLowestSentimentScore(filename):
    try:
        with open(filename) as f_live_room_scores:
            rooms = json.load(f_live_room_scores)
        itemMinValue = min(rooms.items(), key = lambda x: x[1])
        listOfKeys = list ()
        for key, value in rooms.items():
            if value == itemMinValue[1]:
                listOfKeys.append(key)
        return listOfKeys[0], itemMinValue[1]
    except:
        filename_stats_record = "./json_data/stats_record.txt"
        if os.path.exists(filename_stats_record ):
            with open(filename_stats_record) as f_stats_record:
                stats_record = json.load(f_stats_record)
                return stats_record["saddest_room"][0], stats_record["saddest_room"][1]
        else:
            return '-', 1

def update_live_room_scores(filename, room, room_sentiment):
    rooms = {}
    if os.path.exists(filename):
        with open(filename) as f_live_room_scores:
            rooms = json.load(f_live_room_scores)
    
    rooms[room] = room_sentiment

    with open(filename, 'w') as f_live_room_scores:
        json.dump(rooms, f_live_room_scores)       

def delete_live_room_scores(filename, room):
    if os.path.exists(filename):
        with open(filename) as f_live_room_scores:
            rooms = json.load(f_live_room_scores)

    del rooms[room]

    with open(filename, 'w') as f_live_room_scores:
        json.dump(rooms, f_live_room_scores)

def update_live_participant_scores(filename, username, participant_sentiment):
    participants = {}
    if os.path.exists(filename):
        with open(filename) as f_live_participant_scores:
            participants = json.load(f_live_participant_scores)
    
    participants[username] = participant_sentiment

    with open(filename, 'w') as f_live_participant_scores:
        json.dump(participants, f_live_participant_scores)  

def  getParticipantWithHighestSentimentScore(filename):
    try:
        with open(filename) as f_live_participant_scores:
            participants = json.load(f_live_participant_scores)
        itemMaxValue = max(participants.items(), key = lambda x: x[1])
        listOfKeys = list ()
        for key, value in participants.items():
            if value == itemMaxValue[1]:
                listOfKeys.append(key)
        return listOfKeys[0], itemMaxValue[1]
    except:
        filename_stats_record = "./json_data/stats_record.txt"
        if os.path.exists(filename_stats_record ):
            with open(filename_stats_record) as f_stats_record:
                stats_record = json.load(f_stats_record)
                return stats_record["happiest_person"][0], stats_record["happiest_person"][1]
        else:
            return '-', 0

def calculate_stats_record(filename, most_popular_room, most_popular_room_count, happiest_room, happiest_room_score, saddest_room, saddest_room_score, happiest_person, happiest_person_score):
    stats_record = {"most_popular_room": [],
                    "happiest_room": [],
                    "saddest_room": [],
                    "happiest_person": []} 

    if os.path.exists(filename):
        with open(filename) as f_stats_record:
            stats_record = json.load(f_stats_record)
        
        if most_popular_room_count > stats_record["most_popular_room"][1]:
            stats_record["most_popular_room"][1] = most_popular_room_count
            stats_record["most_popular_room"][0] = most_popular_room
        if happiest_room_score > stats_record["happiest_room"][1]:
            stats_record["happiest_room"][1] = happiest_room_score
            stats_record["happiest_room"][0] = happiest_room
        if saddest_room_score < stats_record["saddest_room"][1] and saddest_room_score != 0:
            stats_record["saddest_room"][1] = saddest_room_score
            stats_record["saddest_room"][0] = saddest_room
        if happiest_person_score > stats_record["happiest_person"][1]:
            stats_record["happiest_person"][1] = happiest_person_score
            stats_record["happiest_person"][0] = happiest_person

    else:
        stats_record["most_popular_room"].extend([most_popular_room, most_popular_room_count])
        stats_record["happiest_room"].extend([happiest_room, happiest_room_score])
        stats_record["saddest_room"].extend([saddest_room, saddest_room_score])
        stats_record["happiest_person"].extend([happiest_person, happiest_person_score])

    with open(filename, 'w') as f_stats_record:
        json.dump(stats_record, f_stats_record)

def get_last_n_messages(filename, n):
    with open(filename) as room_file:
        room_json = json.load(room_file)
    return room_json[-n:]

def get_last_n_message_strings(filename, n):
    return [x['message_string'] for x in get_last_n_messages(filename, n)]