import os
import random
import re


files = os.listdir("./erzaehltexte/")
typeset = set()
to_run = ""
# print(files)


def tokenize(text):
    tokens = text.casefold().split()
    tokens_strip = [re.sub("\W", "", x) for x in tokens]
    typeset_inner = set(tokens_strip)
    return typeset_inner, tokens_strip


def getOccurence(files):
    for document in files:
        with open(f"./erzaehltexte/{document}", "r", encoding="utf8") as f:
            typeset_dummy, tokenset_dummy = tokenize(f.read())
            typeset.update(typeset_dummy)
            print(document + " finished!")
    getTypeLog(typeset)
    typesize = len(typeset)
    print(typesize)
    return typeset


def getRelativeOccurence(document, liblen):
    with open(f"./erzaehltexte/{document}", "r", encoding="utf8") as f:
        typeset = tokenize(f.read())[0]
        print(f"Von {liblen} Typen kommen {len(typeset)} im Dokument mit dem Titel {document} vor, "
              f"es beinhaltet also ca. {round((len(typeset)/liblen)*100, 3)} % der im Korpus vorkommenden Typen.")


def getSingleton(typeset):
    types_single = typeset.copy()
    for document in files:
        with open(f"./erzaehltexte/{document}", "r", encoding="utf8") as f:
            types_this = tokenize(f.read())[0]

    return 0


def getTypeLog(typeset):
    with open("./typen.txt", "w", encoding="utf8") as f:
        outlist = list(typeset)
        outlist.sort()
        f.write(str(outlist))


while True:
    if not to_run:
        typeset = getOccurence(files)
    to_run = input("Was machen? r(elative), s(single), e(xit): ")
    typesize = len(typeset)
    if "r" in to_run:
        getRelativeOccurence(files[random.randint(0, len(files)-1)], typesize)
    elif "s" in to_run:
        getSingleton(typeset)
    elif "e" in to_run:
        break
