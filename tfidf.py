from collections import defaultdict, Counter
import re
import glob
from tqdm import tqdm
import random

corpath = "./erzaehltexte/"
doclist = glob.glob(f"{corpath}/*.txt")
invindex = defaultdict(list)
idfdict = dict()
helpcounter = Counter()
outcounter = dict()

def __main__():
    # make inv index with tf
    for docid, doc in tqdm(enumerate(doclist)):
        with open(doc, "r", encoding="utf8") as f:          # iterate all docs in directory
            docterms = re.findall(r"\w+", f.read().lower())
            docset = set(docterms)                          # make set of types per document, with lowered strings
            helpcounter = Counter(docterms)                 # make Counter object of every doc (with ID as key) for later use
            outcounter[doc] = helpcounter
        for type in docset:
            invindex[type].append((docid, float(helpcounter[type]/max(helpcounter.values()))))    # append index of doc and tf of type for each type in current doc

    with open("./data/invindex.txt", "w", encoding="utf8") as f:
        f.write(str(dict(invindex)))

    # make idf dict
    for term in tqdm(invindex):
        idfdict[term] = float(len(invindex[term])/len(doclist))

    # make list of random searches
    ran_list = sorted(invindex.keys())
    for i in range(10):
        ran_int = random.randint(0, len(ran_list) - 1)
        print(ran_list[ran_int:ran_int+20])

    with open("./data/idf.txt", "w", encoding="utf8") as f:
        f.write(str(dict(idfdict)))

__main__()

