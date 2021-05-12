from pyparsing import (
    CaselessKeyword,
    Word,
    pyparsing_unicode,
    ParseResults,
    infixNotation,
    opAssoc,
    ParserElement,
)
from typing import Callable, Iterable, Dict, NewType
from functools import partial, reduce

"""
Simpler für boolesche Suchanfragen.

Was wird benötigt:

1. eine Funktion lookup, der man einen Suchterm übergibt und die dafür eine
   Postingliste zurückgibt 

2. für jeden binären Operator eine Funktion, der zwei
   Postinglisten übergeben werden und die dann eine neue Postingliste
   zurückgibt.

Postingliste == ein Iterable (z.B. Liste) von Integern, aufsteigend sortiert.


Mit parser = create_parser(lookup_funktion, {'and': operator_funktion, 'or':
operator_funktion_2 ...}) erzeugen Sie einen Parser. Mit parse_tree =
parser.parseString(suchanfrage) parsen Sie eine Suchanfrage wie 'caesar AND
julius OR calpurnia'. result_docs = parse_tree.query() liefert Ihnen dann
(mithilfe Ihrer Funktionen) das Ergebnis, d.h. die Liste der Dokumente auf die
die Suchanfrage zutrifft.

Ausführliches Beispiel in der Funktion _test:

"""


def _test():
    # Sie benötigen das Paket pyparsing, dass Sie mit `pip install pyparsing`
    # an der Kommandozeile installieren können, sowie dieses Skript, aus dem
    # Sie die interessante Funktion mit
    #
    # from querylanguage import create_parser
    #
    # importieren können.

    # Ein sehr simpler Inverted Index, Sie bauen den aus den Texten
    inv_index = {"caesar": [2, 3], "julius": [1, 3, 4], "gaius": [1, 3]}

    # Die folgenden Funktionen implementieren die eigentliche Funktionalität
    # der Suchmaschine. Ich habe hier extrem einfache Funktionen, nur zur
    # Demonstration implementiert.

    # Zunächst eine Funktion zum Nachschlagen eines einzelnen
    # Suchterms in dem Dictionary oben:
    def lookup(term):
        return inv_index[term.lower()]

    # Nun Suchoperatoren für AND und OR. In meinem Spielbeispiel arbeite ich
    # mit Mengen und Mengenoperationen, Sie implementieren die Algorithmen aus
    # dem Seminar:
    def and_lists(pl1, pl2):
        return set(pl1) & set(pl2)

    def or_lists(pl1, pl2):
        return set(pl1) | set(pl2)

    # AND_NOT käme jetzt noch ...

    # Nun können wir den Parser für Suchanfragen erzeugen. Wir übergeben ihm die Lookup-Funktion
    # sowie ein Dictionary, das Operatoren auf Funktionen abbildet. Beachten Sie, das wir hier
    # die Funktionen wie lookup nicht aufrufen (keine Klammern()!), sondern dem Parser übergeben,
    # damit sie später aufgerufen werden können. Für die Operatoren gilt: Zuerst übergebene
    # Operatoren binden enger (d.h. AND vor OR analog zu Punktrechnung vor Strichrechnung)
    parser = create_parser(lookup, {"AND": and_lists, "OR": or_lists})

    # In Ihrem Suchmaschinenprogramm würden Sie so vorgehen:
    # Die von der Benutzer:in eingegebene Suchanfrage wird dem Parser übergeben:
    parsed = parser.parseString("gaius AND julius OR caesar")

    # Auf dem Ergebnis des Parsers (dem Parsebaum) rufen Sie nun die Suchanfrage auf,
    # indem Sie parsed.query() aufrufen, ohne Parameter:
    result = parsed.query()

    # Result ist die Liste der Trefferdokumentids. parsed können Sie auch ausgeben lassen, Sie 
    # sehen dann, wie die Klammern / Prioritäten geparst wurden.
    print(parsed, "->", result)

##################################################################################################


PostingList = NewType("PostingList", Iterable[int])


class _BinaryOp:
    """
    A binary left-associative operation that is implemented using the given callable.

    This operation is callable with no arguments, it will evaluate the operands
    and pass the results to fn, assuming the operands are callable as well.
    """

    def __init__(
        self, t: ParseResults, fn: Callable[[PostingList, PostingList], PostingList]
    ):
        self.operator = t[0][1]      
        self.operands = t[0][0::2]  
        self.function = fn

    def __repr__(self):
        return f'{self.operator}({", ".join(map(str, self.operands))})'

    def __call__(self):
        operand_results = (op() if callable(op) else op for op in self.operands)
        return reduce(self.function, operand_results)


class _Term:
    """
    Represents a search term.

    Calling this proxy object simply calls the given function with the represented term and returns the results.
    """

    def __init__(self, t: ParseResults, fn: Callable[[str], PostingList]):
        self.term = t[0]
        self.function = fn

    def __repr__(self):
        return self.term

    def __call__(self):
        return self.function(self.term)


def create_parser(
    term_lookup: Callable[[str], PostingList],
    operators: Dict[str, Callable[[PostingList, PostingList], PostingList]],
) -> ParserElement:
    """
    Creates a parser for boolean search strings from the given functions.

    Args:
        term_lookup: a function that is given a search term (as str) and returns a posting list
        operators: a dictionary mapping operator names to binary functions that implement the
                   operators' behaviour on posting lists

    Returns:
        a parser. call parser.parseString('foo OR bar AND baz').query() to parse and execute the given query.
    """
    term = Word(pyparsing_unicode.alphanums).setParseAction(
        partial(_Term, fn=term_lookup)
    )
    infix_ops = [
        (CaselessKeyword(op), 2, opAssoc.LEFT, partial(_BinaryOp, fn=fn))
        for op, fn in operators.items()
    ]
    search_expr = infixNotation(term, infix_ops).setResultsName("query")
    return search_expr


if __name__ == "__main__":
    _test()
