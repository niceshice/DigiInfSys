import re, os, sys
from tqdm import tqdm
from collections import defaultdict
from querylanguage import create_parser


# TODO: zu dritt erarbeitet von: Sebastian Düker, Aline Eckert, Julian Scheuchenpflug


# run this script from terminal, like 'python postingListScript.py erzaehltexte'
corpath = sys.argv[1]
doclist = os.listdir(f"./{corpath}")
outdict = defaultdict(list)


for doc in tqdm(doclist):
    with open(rf"./{corpath}/{doc}", "r", encoding="utf8") as f:    # iterate all docs in directory
        docset = set(re.findall("\w+", f.read().lower()))           # make set of types per document, with lowered strings
    for types in docset:
        outdict[types].append(doclist.index(doc))                   # append index of doc for each type in current doc


def lookup(term):
    return outdict[term]


def and_lists(pl1, pl2):                                            # and method, as taken from script
    i = 0
    j = 0
    outlist = []
    while (i < len(pl1)) & (j < len(pl2)):
        if pl1[i] == pl2[j]:                                        # add to outlist if fulfilling AND
            outlist.append(pl1[i])
            i += 1
            j += 1
        elif pl1[i] < pl2[j]:                                       # advance smaller pointers
            i += 1
        elif pl1[i] > pl2[j]:
            j += 1
    return outlist


def and_not_lists(pl1, pl2):                                        # and_not method, as taken from script
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

    while i < len(pl1):                                             # append rest of first list
        outlist.append(pl1[i])
        i += 1
    return outlist


def or_lists(pl1, pl2):                                             # or method, as taken from script
    i = 0
    j = 0
    outlist = []
    while (i < len(pl1)) & (j < len(pl2)):
        if pl1[i] == pl2[j]:                                        # always append
            outlist.append(pl1[i])
            i += 1
            j += 1
        elif pl1[i] < pl2[j]:
            outlist.append(pl1[i])
            i += 1
        elif pl1[i] > pl2[j]:
            outlist.append(pl2[j])
            j += 1

    while i < len(pl1):                                             # append rest of larger list
        outlist.append(pl1[i])
        i += 1
    while j < len(pl2):
        outlist.append(pl2[j])
        j += 1

    return outlist


parser = create_parser(lookup, {'AND': and_lists, 'OR': or_lists, 'AND_NOT': and_not_lists})        # create parser with own methods

while True:
    query = input("Anfrage: ")
    if query == "":                                                                                 # break if no input is given
        break
    else:
        parse_tree = parser.parseString(query)                                                      # parses query string
        result = parse_tree.query()                                                                 # returns list of hits
        for hit in result:
            print(doclist[hit])                                                                     # print list of docs according to hit indices
