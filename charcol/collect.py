from twitter import TwitterStream, OAuth
from charcol.secrets import (
    consumer_key, consumer_secret,
    access_token, access_token_secret
)
import json
import time
import unicodedata


DATAFILE = 'freq.csv'

class CharCounter:
    def __init__(self):
        self.chars = {}

    def load_file(self):
        thefile = open(DATAFILE)
        chars = {}
        for line in thefile:
            line = line.strip('\n')
            if line:
                codept, freq, name = line.split('\t')
                codept = int(codept)
                freq = int(freq)
                chars[chr(codept)] = freq
        self.chars = chars
        thefile.close()

    def save_file(self):
        thefile = open(DATAFILE, 'w')
        charlist = sorted(self.chars.keys())
        for char in charlist:
            codept = ord(char)
            freq = self.chars[char]
            try:
                name = unicodedata.name(char)
            except ValueError:
                name = '[unknown character]'
            print('{}\t{}\t{}'.format(codept, freq, name), file=thefile)
        thefile.close()

    def run_sample(self):
        auth = OAuth(
            access_token, access_token_secret,
            consumer_key, consumer_secret
        )
        twitter_stream = TwitterStream(auth=auth)
        iterator = twitter_stream.statuses.sample()
        count = 0
        for tweet in iterator:
            if 'text' in tweet:
                self.handle_tweet(tweet)
            if count % 1000 == 0:
                print(count)
            count += 1
            if count % 1000 == 100:
                self.save_file()

    def handle_tweet(self, tweet):
        text = tweet['text']

        for char in text:
            if char not in self.chars:
                self.chars[char] = 0
                try:
                    name = unicodedata.name(char)
                    text = text.replace(u'\n', u' ')
                    print(u'New character: {}\t{}\n\t{}'.format(char, name, text))
                except ValueError:
                    pass
            self.chars[char] += 1

def main():
    counter = CharCounter()
    try:
        counter.load_file()
    except IOError:
        pass
    counter.run_sample()

if __name__ == '__main__':
    main()

