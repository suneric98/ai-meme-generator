"""
Code for parsing a dataset into an emoji mapping of words to emojis

Emoji mappings are defined as a dictionary mapping a word to a list of emojis.
Each word has 
"""

import io
import os
from collections import defaultdict
import json
import emoji

"""
Helper functions for identifying emojis and defining global paths
"""

EMOJI_MAPPING = os.path.join('..','data','twitter-mapping.json')
COMMENTS = os.path.join('..','data','twitter-data.txt')
PUNC = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

EMOJIS = set(emoji.emojize(emoji_code) for emoji_code in emoji.UNICODE_EMOJI.values())

def is_emoji(c):
    return c in EMOJIS

class TokenType:
    EMOJIS = 0
    WORD = 1

class Token:
    def __init__(self, token_type, raw):
        self.token_type = token_type
        self.raw = raw


"""
Code to implement parsing
"""

def main():
    emoji_mappings = defaultdict(lambda: defaultdict(list))

    print("Creating mappings...")
    with open(COMMENTS, "r", encoding="utf-8") as comments_file:
        for line in comments_file:
            line = line.lower()
            line = "".join([l for l in line if l not in PUNC])
            tokens = tokenize(line)
            for i, t in enumerate(tokens):
                if t.token_type == TokenType.EMOJIS:
                    before, after = findClosestWords(tokens, i)
                    if before:
                        emoji_mappings[before]["before"].append(t.raw)
                    if after:
                        emoji_mappings[after]["after"].append(t.raw)
    
    print("Writing mappings to file...")
    with io.open(EMOJI_MAPPING, "w", encoding="utf-8") as mappings_file:
        json.dump(emoji_mappings, mappings_file, ensure_ascii=False)

def tokenize(line):
    tokens = []
    idx = 0
    while idx < len(line):
        char = line[idx]
        type = TokenType.WORD
        raw = char

        if is_emoji(char): # emoji
            type = TokenType.EMOJIS
            raw = char
        elif not char.isspace(): # word
            word, idx = parseWord(line, idx)
            type = TokenType.WORD
            raw = word
        else: # whitespace
            idx += 1
            continue
        
        tokens.append(Token(type, raw))
        idx += 1
    return tokens

def parseWord(line, idx):
    endOfWord = idx
    word = ""
    while endOfWord < len(line) and not line[endOfWord].isspace():
        word += line[endOfWord]
        endOfWord += 1
    return word, endOfWord

def findClosestWords(tokens, idx):
    before = None
    after = None
    j = idx - 1

    while j >= 0:
        if tokens[j].token_type == TokenType.WORD:
            before = tokens[j].raw
            break
        j -= 1
    
    j = idx + 1
    while j < len(tokens):
        if tokens[j].token_type == TokenType.WORD:
            after = tokens[j].raw
            break
        j += 1
    
    return before, after

if __name__ == "__main__":
    main()