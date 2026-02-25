"""
Tokens

Doc     := <doc> EList </doc>
EList   := EList Element | Element | ε
Element := Img | Para | Table
Table   := <table> RList </table>
RList   := RList Row | Row | ε
Row     := <tr> CList </tr>
CList   := CList Cell | Cell | ε
Cell    := <td> EList </td>
Img     := <img Src />
Src     := src= Href
Href    := /static/1.png | /static/2.png | /static/3.png
Para    := <p> Text </p>
Text    := [a-zA-Z0-9]+
"""

VALID_HREFS = {
    "/static/1.png",
    "/static/2.png",
    "/static/3.png",
}

class Document:
    def __init__(self, elist):
        self.elist = elist

    def __repr__(self):
        return f"Document({self.elist})"


class ElementList:
    def __init__(self, elements=None):
        self.elements = elements or []

    def __repr__(self):
        return f"ElementList({self.elements})"


class Element:
    def __init__(self, child):
        self.child = child

    def __repr__(self):
        return f"Element({self.child})"


class Table:
    def __init__(self, rlist):
        self.rlist = rlist

    def __repr__(self):
        return f"Table({self.rlist})"


class RowList:
    def __init__(self, rows=None):
        self.rows = rows or []

    def __repr__(self):
        return f"RowList({self.rows})"


class Row:
    def __init__(self, clist):
        self.clist = clist

    def __repr__(self):
        return f"Row({self.clist})"


class CellList:
    def __init__(self, cells=None):
        self.cells = cells or []

    def __repr__(self):
        return f"CellList({self.cells})"


class Cell:
    def __init__(self, elist):
        self.elist = elist

    def __repr__(self):
        return f"Cell({self.elist})"


class Paragraph:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"Paragraph({self.text})"


class Image:
    def __init__(self, src):
        self.src = src

    def __repr__(self):
        return f"Image({self.src})"


class Text:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Text({self.value!r})"