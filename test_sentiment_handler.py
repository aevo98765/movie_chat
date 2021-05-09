import unittest
from sentiment_handler import getSentiment, filterProfanity


class TestSentiment(unittest.TestCase):
    def test_username_sentiment_calculate(self):
        """
        Test that it can calculate sentiment score given a string
        """
        happy_message = 'I\'m happy'
        sad_message = 'I am sad'
        invalid_message = 9999

        
        happy_sentiment = getSentiment(happy_message)
        sad_sentiment = getSentiment(sad_message)
        self.assertEqual(happy_sentiment,0.9,'Must be equal to 0.9')
        self.assertEqual(sad_sentiment, 0.25, 'Must be equal to 0.25')
        invalid_sentiment = getSentiment(invalid_message)
        self.assertEqual(invalid_sentiment,0.5)
    
    def test_filter_profanity(self):
        """
        Test that it can remove profanity
        """
        raw_message = 'cRaP CRAp craP  dmfkme mkee crap sldl'


        pure_message = filterProfanity(raw_message)
        print(pure_message)
        self.assertEqual(
            pure_message, 'c***P C***p c***P  dmfkme mkee c***p sldl')

        
    


 
if __name__ == '__main__':
    unittest.main()
