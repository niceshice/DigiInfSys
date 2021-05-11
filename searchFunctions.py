import collections as col
import os

indexingList = os.listdir(r"./erzaehltexte_cut")
retset = set()

with open(r"./postingList.txt", "r", encoding="utf8") as f:
    postingList = col.defaultdict(f.read())

todo = input("Search for ")


# for item in postingList:
#    if eval(todo) in :


