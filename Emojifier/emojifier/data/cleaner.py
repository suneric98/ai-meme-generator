# load text
f = open("best-twitter-data.txt", "r", encoding="utf-8")
text = f.read()
f.close()

# split into individual tweets
lines = text.splitlines()

# remove all @words, #'s, and links
for i in range(len(lines)):
    l = lines[i]
    if (l.find("@") != -1) or (l.find("#") != -1) or (l.find("https")):
        words = l.split()
        for j in range(len(words)):
            w = words[j]
            if w.find("@") != -1:
                words[j] = ""
            elif w.find("#") != -1:
                words[j] = w.split("#")[1]
            elif w.find("https") != -1:
                words[j] = ""
        cleaned = " ".join(words)
        lines[i] = cleaned.strip()

# write out to a new file
out = open("twitter-data-cleaned.txt", "w", encoding="utf-8")
for l in lines:
    out.write(l)
    out.write("\n")
out.close()
