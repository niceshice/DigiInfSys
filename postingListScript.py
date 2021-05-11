import re
import json
import os
from collections import defaultdict

doclist = os.listdir(r"./erzaehltexte")
outdict = defaultdict(list)


def tokenize(text):
    tokens = text.split()
    tokens_strip = [re.sub("\W", "", x) for x in tokens]
    typeset_inner = set(tokens_strip)
    return typeset_inner


for doc in doclist:
    with open(rf"./erzaehltexte/{doc}", "r", encoding="utf8") as f:
        docstring = f.read()
        docstring = docstring.casefold()
        docset = tokenize(docstring)
    for types in docset:
        outdict[types].append(doclist.index(doc))
    print("finished", doc)

with open(r"./postingJSONScript.json", "w", encoding="utf8") as f:
    f.write(json.dumps(outdict))

print("finish")
