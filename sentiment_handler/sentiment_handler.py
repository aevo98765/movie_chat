import re
from textblob import TextBlob


def getSentiment(text):
    '''Calculates the sentiment of text by averaging across sentences from 0 to 100'''
    blob = TextBlob(_translate_emoticons(text))
    total_score = 0
    num = 0
    for sentence in blob.sentences:
        total_score += sentence.sentiment.polarity
        num += 1

    return (total_score/2*num)+0.5


def _translate_emoticons(string):
    '''Translates emoticons into their text meaning'''
    emoticon_dict = {
        ":)": "happy", ":(": "sad", ":o": "shocked", ">:(": "hate"
    }
    words = string.split(' ')
    for i in range(len(words)):
        if words[i] in list(emoticon_dict.keys()):
            words[i] = emoticon_dict[words[i]]

    return ' '.join(word for word in words)


profane_words = ['fuck', 'shit','bastard','ruddy','blast','crap','crud']


def filterProfanity(string):
    words = string.split(' ')
    count = 0
    for i in range(len(words)):
        for pword in profane_words:

            if pword in words[i].lower():
                fLetter = words[i][0]
                lLetter = words[i][-1]
                words[i] = fLetter+'***'+lLetter
            count += 1
    print(count)
    if 'criticism of the government' in string:
        return "----CENSORED----"
    return ' '.join(words)






