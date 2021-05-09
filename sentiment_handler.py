from textblob import TextBlob
import emoji
import nltk
nltk.download('punkt')


def getSentiment(text):
    '''Calculates the sentiment of text by averaging across sentences from 0 to 100'''
    
    blob = TextBlob(_translate_emoticons(text))
    return (blob.sentiment.polarity/2)+0.5


def _translate_emoticons(text):
    '''Translates emoticons into thier text meaning'''
    string = str(text)
    words = string.split(' ')
    for i in range(len(words)):
        w = words[i]
        if emoji.emoji_count(w) > 0:
            w = emoji.demojize(w)
            w = w.replace(':',' ')
            w = w.replace('_',' ')
            w = w.replace('-',' ')
            w = w.replace('smiling','happy')
            w = w.replace('grinning', 'joy')
            w = w.replace('pensive', 'sad')
            w = w.replace('loudly crying','horrible')
            w = w.replace('crying', 'sad')
            words[i] = '' +w

    pure_string = ' '.join(words)

    return pure_string


profane_words = ['fuck', 'shit','bastard','ruddy','blast','crap','crud']


def filterProfanity(text):
    string = str(text)
    print(type(string))
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

        
