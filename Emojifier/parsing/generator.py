import random
import io
import json
import os
import re

EMOJI_MAPPING_FILE = os.path.join('Emojifier','data','emoji-mapping2.json')
MAX_EMOJIS = 2

def makeGroups(lst, n):
    groups = []
    for i in range(0, len(lst), n):
        groups.append(lst[i:i+n])
    return groups

def getEmojiMapping():
    mappings = None
    with io.open(EMOJI_MAPPING_FILE, "r", encoding="utf-8") as mappings_file:
        mappings = json.load(mappings_file)
    return mappings

def getEmojisForGroups(groups, mapping):
    result = []
    for g in groups:
        beforeEmojis = []
        afterEmojis = []
        for t in g:
            t = re.sub(r'[^\w\s]', '', t.lower())
            if t in mapping:
                if "before" in mapping[t]:
                    beforeEmojis.extend(mapping[t]["before"])
                if "after" in mapping[t]:
                    afterEmojis.extend(mapping[t]["after"])
        
        numBefore = int(MAX_EMOJIS/2) if beforeEmojis else 0
        numAfter = int(MAX_EMOJIS/2) if afterEmojis else 0
        for i in range(0, numBefore):
            result.append(random.choice(beforeEmojis))
        result.extend(g)
        for i in range(0, numAfter):
            result.append(random.choice(afterEmojis))
    return result
        

def generateEmojipasta(text, mapping, freq = 2):
    tokens = text.split()
    groups = makeGroups(tokens, freq)
    result = getEmojisForGroups(groups, mapping)
    return " ".join(result)

def main():
    mapping = getEmojiMapping()
    while True:
        text = input()
        if text == "quit":
            break
        answer = generateEmojipasta(text, mapping)
        print(answer)

if __name__ == "__main__":
    main()
