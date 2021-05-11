import re

query = "foo OR bar AND NOT gazonk"

result_set = set()
operation = None

for word in re.split(" +(AND|OR) +",query):
    #word will be in ['foo', 'OR', 'bar', 'AND', 'NOT gazonk']

    inverted = False    # for "NOT word" operations

    if word in ['AND', 'OR']:
        operation = word
        continue

    if word.find('NOT ') == 0:
        if operation is 'OR':
        # generally "OR NOT" operation does not make sense, but if it does in your case, you
        # should update this if() accordingly
            continue

        inverted=True
        # the word is inverted!
        realword=word[4:]
    else:
        realword=word

    if operation is not None:
        # now we need to match the key and the filenames it contains:
        current_set=set(inverted_index[realword].keys())

        if operation is 'AND':
            if inverted is True:
                result_set -= current_set
            else:
                result_set &= current_set
        elif operation is 'OR':
            result_set |= current_set

    operation=None

print(result_set)