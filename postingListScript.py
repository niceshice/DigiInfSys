import re
import json
import os
import sys
from tqdm import tqdm
from collections import defaultdict


# run this script from terminal, like 'python postingListScript.py erzaehltexte'
corpath = sys.argv[1]
doclist = os.listdir(f"./{corpath}")
outdict = defaultdict(list)


def tokenize(text):
    return set(re.findall("\w+", text))


for doc in tqdm(doclist):
    with open(rf"./{corpath}/{doc}", "r", encoding="utf8") as f:
        docset = set(re.findall("\w+", f.read().casefold()))
    for types in docset:
        outdict[types].append(doclist.index(doc))


with open(rf"./{corpath}PList.json", "w", encoding="utf8") as f:
    f.write(json.dumps(outdict, indent=2))
