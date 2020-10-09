import random
import io
import json
import os
import re

EMOJI_MAPPING_FILE = os.path.join('Emojifier','data','emoji-mapping2.json')

def getEmojiMapping():
    mappings = None
    with io.open(EMOJI_MAPPING_FILE, "r", encoding="utf-8") as mappings_file:
        mappings = json.load(mappings_file)
    return mappings
    
def generateEmojipasta(text, mapping):
    tokens = text.split()
    result = []
    for t in tokens:
        result.append(t)
        t = re.sub(r'[^\w\s]', '', t.lower())
        if t in mapping:
            if "before" in mapping[t]:
                result.append(random.choice(mapping[t]["before"]))
            if "after" in mapping[t]:
                result.append(random.choice(mapping[t]["after"]))
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
