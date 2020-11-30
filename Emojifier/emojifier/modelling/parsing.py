"""
Code for parsing a dataset into an emoji mapping of words to emojis

Emoji mappings are defined as a dictionary mapping a word to a list of emojis.
Each word has 
"""

import io
import re
import os
from collections import defaultdict
import json
import emoji
from nltk.corpus import stopwords

"""
Helper functions for identifying emojis and defining global paths
"""
class TokenType:
    EMOJIS = 0
    WORD = 1

class Token:
    def __init__(self, token_type, raw):
        self.token_type = token_type
        self.raw = raw

stop_words = set(stopwords.words('english')) 

"""
Code to implement parsing
"""

class Tokenizer:
    def __init__(self, emojis):
        self.PUNC = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''
        self.EMOJIS = set(emojis)
        self.FULL_EMOJIS = set(emoji.emojize(emoji_code) for emoji_code in emoji.UNICODE_EMOJI.values())
        
    def tokenize(self, line):
        line = "".join([l for l in line if l not in self.PUNC])
        # line = re.sub(self.PUNC, "", line)
        line = line.lower()
        tokens = []
        idx = 0
        while idx < len(line):
            char = line[idx]
            type = TokenType.WORD
            raw = char

            if char in self.EMOJIS: # emoji
                type = TokenType.EMOJIS
                raw = char
            elif char in self.FULL_EMOJIS: # emoji we want to skip
                idx += 1
                continue
            elif not char.isspace(): # word
                word, idx = self.parseWord(line, idx)
                if word in stop_words:
                    continue
                type = TokenType.WORD
                raw = word
            else: # whitespace
                idx += 1
                continue
            
            tokens.append(Token(type, raw))
            idx += 1
        return tokens

    def parseWord(self, line, idx):
        endOfWord = idx
        word = ""
        while endOfWord < len(line) and not line[endOfWord].isspace() and not line[endOfWord] in self.FULL_EMOJIS:
            word += line[endOfWord]
            endOfWord += 1
        return word, endOfWord

    def findClosestNWords(self, N, tokens, idx):
        j = idx - 1
        words = []
        while j >= 0 and len(words) < N:
            t = tokens[j]
            if t.token_type == TokenType.WORD and t.raw.strip() != '':
                words.insert(0,t.raw)
            j -= 1
        j = idx + 1
        while j < len(tokens) and len(words) < N:
            t = tokens[j]
            if t.token_type == TokenType.WORD and t.raw.strip() != '':
                words.append(t.raw)
            j += 1
        return words
        
    def findClosestWords(self, tokens, idx):
        before = None
        after = None
        j = idx - 1

        while j >= 0:
            t = tokens[j]
            if t.token_type == TokenType.WORD and t.raw.strip() != '':
                before = t.raw
                break
            j -= 1
        
        j = idx + 1
        while j < len(tokens):
            t = tokens[j]
            if t.token_type == TokenType.WORD and t.raw.strip() != '':
                after = t.raw
                break
            j += 1
        return before, after


def main():
    EMOJI_MAPPING = os.path.join('..','data','test.json')
    COMMENTS = os.path.join('..','data','twitter-data.txt')
    EMOJIS = set(emoji.emojize(emoji_code) for emoji_code in emoji.UNICODE_EMOJI.values())
    emoji_mappings = defaultdict(lambda: defaultdict(list))
    tokenizer = Tokenizer(EMOJIS)

    print("Creating mappings...")
    with open(COMMENTS, "r", encoding="utf-8") as comments_file:
        for line in comments_file:
            line = line.lower().strip()
            tokens = tokenizer.tokenize(line)
            for i, t in enumerate(tokens):
                if t.token_type == TokenType.EMOJIS:
                    before, after = tokenizer.findClosestWords(tokens, i)
                    if before:
                        emoji_mappings[before]["before"].append(t.raw)
                    if after:
                        emoji_mappings[after]["after"].append(t.raw)
    
    print("Writing mappings to file...")
    with io.open(EMOJI_MAPPING, "w", encoding="utf-8") as mappings_file:
        json.dump(emoji_mappings, mappings_file, ensure_ascii=False)

if __name__ == "__main__":
    main()