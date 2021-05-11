import os
import collections as col
import re
import json

indexingList = os.listdir(r"./erzaehltexte_cut")
indexDefDict = col.defaultdict(list)


def tokenize(text):
    tokens = text.split()
    tokens_strip = [re.sub("\W", "", x) for x in tokens]
    typeset_inner = set(tokens_strip)
    return typeset_inner


with open(r"./typen.txt", "r", encoding="utf8") as f:
    helpList = f.read()


for doc in indexingList:
    with open(rf"./erzaehltexte_Cut/{doc}", "r", encoding="utf8") as f:
        docset = tokenize(f.read())
        print(doc, "tokenized")
        for item in docset:
            indexDefDict[f"{item}"].append(indexingList.index(doc))
            print("appended", indexingList.index(doc), "to", item)


with open(r"./postingListTest.txt", "w", encoding="utf8") as f:
    f.write(str(indexDefDict))


with open(r"./postingJSONTest.json", "w", encoding="utf8") as f:
    f.write(json.dumps(indexDefDict, indent=2))
