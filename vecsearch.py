from collections import defaultdict, Counter
import re
import os
from tqdm import tqdm
import math
import sys

# no catching of input terms that are not in corpus

corpath = sys.argv[1]
doclist = os.listdir(f"./{corpath}")
invindex = defaultdict(list)
idfdict = dict()
helpcounter = Counter()

for docid, doc in tqdm(enumerate(doclist)):
    with open(f"{corpath}/{doc}", "r", encoding="utf8") as f:          # iterate all docs in directory
        docterms = re.findall(r"\w+", f.read().lower())
        docset = set(docterms)                          # make set of types per document, with lowered strings
        helpcounter = Counter(docterms)                 # make Counter object of every doc (with ID as key) for later use
    for type in docset:
        invindex[type].append((docid, float(helpcounter[type]/max(helpcounter.values()))))    # append index of doc and tf of type for each type in current doc

# calculate idf values per term
for term in tqdm(invindex):
    idfdict[term] = math.log(len(doclist)/len(invindex[term]))

# calculate document vectors (squared)
docvec = defaultdict(lambda: 0.0)
for term in invindex:
    for en, entry in enumerate(invindex[term]):
        docvec[invindex[term][en][0]] += (invindex[term][en][1] * idfdict[term]) ** 2
# sqrt the sum per document
for item in docvec:
    docvec[item] = math.sqrt(docvec[item])

while True:
    query = input("Anfrage: ")
    if query == "":                                    # break if no input is given
        break
    else:
        query = query.split()
        
        scores = defaultdict(lambda: 0.0)

        for term in query:
            w_tq = idfdict[term]
            plist = invindex[term]
            for en, doc in enumerate(plist):
                scores[doc[0]] += w_tq * ((plist[en][1]) * idfdict[term])
        for item in scores:
            scores[item] = scores[item] / docvec[item]

        out = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # output results
        for i in range(10):
            try:
                print(doclist[out[i][0]], out[i][1])
            except:
                print("only ", i, "occurences found.")
                break
