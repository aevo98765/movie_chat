import unittest
import json
from json_handeler import json_handeler as jh
import os


class TestJSON(unittest.TestCase):
    def test_username_sentiment_calculate(self):
        """
        Test that it can calculate sentiment score given a username and room
        """
        room = 9
        filename = './test_json_data/messages/messagesJSON' + str(room) + '.txt'
        
        
        result = jh.username_sentiment_calculation(filename,'username')
        self.assertEqual(result,0.5,'Must be equal to 0.5')


        
    def test_update_file(self):
        """
        Test that it can sum a list of integers
        """
        room = 999
        filename = './test_json_data/messages/messagesJSON' + str(room) + '.txt'
        sample_json = {"username": 'username',
                               "test_value": 0.9,
                               "room": room,
                               "leaving_time": 00000}

        jh.update_file(filename,sample_json)

        with open(filename) as f_with_json:
            existing_json = json.load(f_with_json)
            for message in existing_json:
                try:
                    message_username = message['username']
                    score = message['test_value']
                except:
                    pass
        self.assertEqual(message_username, 'username', 'Must be equal to username')
        self.assertEqual(score, 0.9, 'Must be equal to 0.575')

    def test_get_new_ave_room_sentiment(self):
        """
        Test that it can get ave sentiment given filename room and new score
        """
        room = 9
        filename = './test_json_data/rooms/roomJSON' + str(room) + '.txt'
        new_value1 = 0
        new_value2 = 2
        new_value3 = 10
        result1 = jh.getNewAveRoomSentiment(filename,new_value1)
        result2 = jh.getNewAveRoomSentiment(filename, new_value2)
        result3 = jh.getNewAveRoomSentiment(filename, new_value3)

        self.assertEqual(result1,0.75)
        self.assertEqual(result2,1.25)
        self.assertEqual(result3,3.25)

    def test_get_active_rooms(self):
        """
        Test that it can get a dict of active rooms
        """
        filename = './test_json_data/chat_participant_list.txt'

        result = jh.getActiveRooms(filename)
        bad_result = jh.getActiveRooms('invalid file path')
        
        self.assertEqual(len(result),2)
        self.assertEqual(type(result),type({'1':1}))
        self.assertEqual(len(bad_result), 0)


    def test_update_chat_participants(self):
        """
        Test that it can get a dict of active rooms
        """
        filename = './test_json_data/chat_participant_list2.txt'
        rooms = {"901":['user2']}
        jh.update_chat_participants(filename,rooms)

        rooms = {}
        if os.path.exists(filename):
            with open(filename) as f_with_participants:
                rooms = json.load(f_with_participants)
        self.assertEqual(rooms['901'],['user2'])
    
    def test_del_chat_participants(self):
        """
        Test that it can get a dict of active rooms
        """
        filename = './test_json_data/chat_participant_list3.txt'
        rooms = {'101':['user101']}
        with open(filename, 'w') as f_with_participants:
            json.dump(rooms, f_with_participants)
        
        jh.delete_chat_participant(filename,'user101','101')
        rooms = {}
        
        if os.path.exists(filename):
            with open(filename) as f_with_participants:
                rooms = json.load(f_with_participants)
        
        self.assertEqual(len(rooms),0)



 
if __name__ == '__main__':
    unittest.main()
