import re
import json
import os
import sys
from tqdm import tqdm
from collections import defaultdict
from querylanguage import create_parser
import pyparsing

# run this script from terminal, like 'python postingListScript.py erzaehltexte'
corpath = sys.argv[1]                  # TODO remake to sys.argv[1]
doclist = os.listdir(f"./{corpath}")
outdict = defaultdict(list)

# iterate all docs in directory
for doc in tqdm(doclist):
    with open(rf"./{corpath}/{doc}", "r", encoding="utf8") as f:
        docset = set(re.findall("\w+", f.read().lower()))           # make set of types per document, with lowered strings
    for types in docset:
        outdict[types].append(doclist.index(doc))                   # append index of doc for each type in current doc


# write to file
with open(rf"./{corpath}PList.json", "w", encoding="utf8") as f:
    json.dump(outdict, f, indent=2)


def and_lists(pl1, pl2):                                            # and method
    i = 0
    j = 0
    outlist = []
    while (i < len(pl1)) & (j < len(pl2)):
        if pl1[i] == pl2[j]:
            outlist.append(pl1[i])                                  # add when same
            i += 1
            j += 1
        elif pl1[i] < pl2[j]:
            i += 1
        elif pl1[i] > pl2[j]:
            j += 1
    return outlist


def and_not_lists(pl1, pl2):
    i = 0
    j = 0
    outlist = []
    while (i < len(pl1)) & (j < len(pl2)):
        if pl1[i] == pl2[j]:
            i += 1
        elif pl1[i] < pl2[j]:
            outlist.append(pl1[i])
            i += 1
        elif pl1[i] > pl2[j]:
            j += 1

    while i < len(pl1):
        outlist.append(pl1[i])
        i += 1
    return outlist


def or_lists(pl1, pl2):
    i = 0
    j = 0
    outlist = []
    while (i < len(pl1)) & (j < len(pl2)):
        if pl1[i] == pl2[j]:
            outlist.append(pl1[i])
            i += 1
            j += 1
        elif pl1[i] < pl2[j]:
            outlist.append(pl1[i])
            i += 1
        elif pl1[i] > pl2[j]:
            outlist.append(pl2[j])
            j += 1

    while i < len(pl1):
        outlist.append(pl1[i])
        i += 1
    while j < len(pl2):
        outlist.append(pl2[j])
        j += 1

    return outlist


def lookup(term):
    return outdict[term]

parser = create_parser(lookup, {'AND': and_lists, 'OR': or_lists, 'AND_NOT': and_not_lists})

while True:
    query = input("Anfrage: ")
    if query == "":
        break
    else:
        parse_tree = parser.parseString(query)
        result = parse_tree.query()
        for hit in result:
            print(parse_tree, "->", result)
            print(doclist[hit])
