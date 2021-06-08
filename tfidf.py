import math
from collections import defaultdict, Counter
import re
import glob
from tqdm import tqdm

# HA: struktur wie besprochen, also inv index, dict mit invindex und tf pro wort, doclist

corpath = "./erzaehltexte/"
doclist = glob.glob(f"{corpath}/*.txt")
invindex = defaultdict(list)
tfdict = defaultdict(list)
idfdict = dict()
helpcounter = defaultdict(Counter)


def get_max(docindex):
    return helpcounter[doclist[docindex]].most_common(1)[0][1]


def get_tf(doc, term):
    return float(helpcounter[doclist[doc]][term] / get_max(doc))     # calculate tf


def _main():
    # make inv index
    for doc in tqdm(doclist):
        with open(doc, "r", encoding="utf8") as f:          # iterate all docs in directory
            docterms = re.findall("\w+", f.read().lower())
            docset = set(docterms)                          # make set of types per document, with lowered strings
            helpcounter[doc] = Counter(docterms)            # make Counter object of every doc for later use
        for types in docset:
            invindex[types].append(doclist.index(doc))      # append index of doc for each type in current doc

    with open("./data/invindex.txt", "w", encoding="utf8") as f:
        f.write(str(dict(invindex)))

    # make inv index with tf values
    for term in tqdm(invindex):
        for i, doc in tqdm(enumerate(invindex[term])):
            invindex[term][i] = (doc, get_tf(doc, term))

    # make idf dict
    for term in tqdm(invindex):
        idfdict[term] = float(len(invindex[term])/len(doclist))

    with open("./data/tfinvindex.txt", "w", encoding="utf8") as f:
        f.write(str(dict(invindex)))

    with open("./data/idf.txt", "w", encoding="utf8") as f:
        f.write(str(dict(idfdict)))

_main()

