from twitter import TwitterStream, OAuth
from charcol.secrets import (
    consumer_key, consumer_secret,
    access_token, access_token_secret
)
import json
import time
import unicodedata
from ftfy.fixes import fix_text_encoding, remove_unsafe_private_use
from ftfy.badness import sequence_weirdness
from ftfy.chardata import possible_encoding
from collections import defaultdict

DATAFILE = 'freq.csv'

class CharCounter:
    def __init__(self):
        self.chars = {}
        self.lines_by_lang = defaultdict(list)

    def load_files(self):
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

    def save_files(self):
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
        
        for lang, lines in self.lines_by_lang.items():
            langfile = open('tweets.{}.txt'.format(lang), 'a')
            for line in lines:
                print(line.replace('\n', ' '), file=langfile)
            langfile.close()
        self.lines_by_lang = defaultdict(list)

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
            if count % 10000 == 0:
                print(count)
            count += 1
            if count % 10000 == 100:
                self.save_files()

    def check_ftfy(self, text):
        check_text = remove_unsafe_private_use(text).lower()
        if not possible_encoding(text, 'ascii') and 'unfollow' not in check_text:
            fixed = fix_text_encoding(text)
            if text != fixed:
                print(u'Text:\t{text}\nFixed:\t{fixed}\n'.format(text=text, fixed=fixed))

    def handle_tweet(self, tweet):
        text = tweet['text']
        self.check_ftfy(text)
        if 'user' in tweet:
            lang = tweet['user'].get('lang', 'NONE')
            self.lines_by_lang[lang].append(tweet['text'])

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
        counter.load_files()
    except IOError:
        pass
    counter.run_sample()

if __name__ == '__main__':
    main()

