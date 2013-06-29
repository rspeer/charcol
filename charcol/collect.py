from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from charcol.secrets import (
    consumer_key, consumer_secret,
    access_token, access_token_secret
)
import json
import time
import unicodedata

class TweetListener(StreamListener):
    def __init__(self):
        StreamListener.__init__(self)
        self.chars = {}

    def on_status(self, status):
        for char in status.text:
            if char not in self.chars:
                self.chars[char] = 0
                try:
                    name = unicodedata.name(char)
                    print(u'New character: {}\t{}\n\t{}'.format(char, name, status.text))
                except ValueError:
                    pass
            self.chars[char] += 1

    def on_error(self, status):
        print(status)


def run_sample():
    l = TweetListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.sample()

def main():
    run_sample()

if __name__ == '__main__':
    main()