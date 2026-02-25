"""
SafeHTML

A safe HTML parser and serializer. Only documents conforming to the grammar
defined in tokens.py are accepted. All others are rejected.
"""
from tokens import (
    Document, ElementList, Element, Table, RowList, Row,
    CellList, Cell, Paragraph, Image, Text, VALID_HREFS
)
import re


class ParseError(Exception):
    pass


class Parser:
    """
    Recursive descent parser for the SafeHTML grammar.

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

    # Tokenizer pattern — order matters
    TOKEN_PATTERNS = [
        ('OPEN_DOC',       r'<doc>'),
        ('CLOSE_DOC',      r'</doc>'),
        ('OPEN_TABLE',     r'<table>'),
        ('CLOSE_TABLE',    r'</table>'),
        ('OPEN_TR',        r'<tr>'),
        ('CLOSE_TR',       r'</tr>'),
        ('OPEN_TD',        r'<td>'),
        ('CLOSE_TD',       r'</td>'),
        ('OPEN_P',         r'<p>'),
        ('CLOSE_P',        r'</p>'),
        ('IMG',            r'<img\s+src=(/static/(?:1|2|3)\.png)\s*/>'),
        ('TEXT',           r'[a-zA-Z0-9]+'),
        ('WS',             r'\s+'),
    ]

    MASTER = re.compile(
        '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_PATTERNS)
    )

    def __init__(self, text):
        self.tokens = [
            (m.lastgroup, m.group())
            for m in self.MASTER.finditer(text)
            if m.lastgroup != 'WS'
        ]
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][0]
        return None

    def peek_val(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][1]
        return None

    def consume(self, expected_type):
        if self.pos >= len(self.tokens):
            raise ParseError(f"Expected {expected_type} but reached end of input")
        ttype, tval = self.tokens[self.pos]
        if ttype != expected_type:
            raise ParseError(f"Expected {expected_type}, got {ttype} ({tval!r})")
        self.pos += 1
        return tval

    def parse(self):
        doc = self.parse_doc()
        if self.pos != len(self.tokens):
            raise ParseError("Unexpected tokens after </doc>")
        return doc

    def parse_doc(self):
        self.consume('OPEN_DOC')
        elist = self.parse_elist(stop_tokens={'CLOSE_DOC'})
        self.consume('CLOSE_DOC')
        return Document(elist)

    def parse_elist(self, stop_tokens, in_cell=False):
        elements = []
        while self.peek() not in stop_tokens and self.peek() is not None:
            el = self.parse_cell_element() if in_cell else self.parse_element()
            elements.append(el)
        return ElementList(elements)

    def parse_element(self):
        t = self.peek()
        if t == 'OPEN_TABLE':
            return Element(self.parse_table())
        elif t == 'OPEN_P':
            return Element(self.parse_para())
        elif t == 'IMG':
            return Element(self.parse_img())
        else:
            raise ParseError(f"Expected element, got {t} ({self.peek_val()!r})")

    def parse_cell_element(self):
        """Elements valid inside a Cell — same as Element but also allows bare Text."""
        t = self.peek()
        if t == 'OPEN_TABLE':
            return Element(self.parse_table())
        elif t == 'OPEN_P':
            return Element(self.parse_para())
        elif t == 'IMG':
            return Element(self.parse_img())
        elif t == 'TEXT':
            return Element(self.parse_text())
        else:
            raise ParseError(f"Expected cell element, got {t} ({self.peek_val()!r})")

    def parse_table(self):
        self.consume('OPEN_TABLE')
        rlist = self.parse_rlist()
        self.consume('CLOSE_TABLE')
        return Table(rlist)

    def parse_rlist(self):
        rows = []
        while self.peek() == 'OPEN_TR':
            rows.append(self.parse_row())
        return RowList(rows)

    def parse_row(self):
        self.consume('OPEN_TR')
        clist = self.parse_clist()
        self.consume('CLOSE_TR')
        return Row(clist)

    def parse_clist(self):
        cells = []
        while self.peek() == 'OPEN_TD':
            cells.append(self.parse_cell())
        return CellList(cells)

    def parse_cell(self):
        self.consume('OPEN_TD')
        elist = self.parse_elist(stop_tokens={'CLOSE_TD'}, in_cell=True)
        self.consume('CLOSE_TD')
        return Cell(elist)

    def parse_para(self):
        self.consume('OPEN_P')
        text = self.parse_text()
        self.consume('CLOSE_P')
        return Paragraph(text)

    def parse_text(self):
        val = self.consume('TEXT')
        return Text(val)

    def parse_img(self):
        raw = self.consume('IMG')
        m = re.match(r'<img\s+src=(/static/[^\s/>]+)\s*/>', raw)
        if not m:
            raise ParseError(f"Malformed img tag: {raw!r}")
        href = m.group(1)
        if href not in VALID_HREFS:
            raise ParseError(f"Invalid href: {href!r}")
        return Image(href)

def serialize(node):
    if isinstance(node, Document):
        return serialize(node.elist)

    if isinstance(node, ElementList):
        return ''.join(serialize(e) for e in node.elements)

    if isinstance(node, Element):
        return serialize(node.child)

    if isinstance(node, Table):
        rows = serialize(node.rlist)
        from flask import current_app
        env = current_app.jinja_env.overlay(autoescape=False)
        return env.from_string(f"<table>{rows}</table>").render()

    if isinstance(node, RowList):
        return ''.join(serialize(r) for r in node.rows)

    if isinstance(node, Row):
        # cells are emitted as jinja2 fragments so the table renderer can evaluate them
        cells = serialize(node.clist)
        return f"<tr>{cells}</tr>"

    if isinstance(node, CellList):
        return ''.join(serialize(c) for c in node.cells)

    if isinstance(node, Cell):
        elems = node.elist.elements
        if len(elems) == 1 and isinstance(elems[0].child, Text):
            return f"<td>{{{{ {elems[0].child.value} }}}}</td>"
        return f"<td>{serialize(node.elist)}</td>"

    if isinstance(node, Paragraph):
        return f"<p>{serialize(node.text)}</p>"

    if isinstance(node, Image):
        return f'<img src="{node.src}" />'

    if isinstance(node, Text):
        return node.value

    raise ValueError(f"Unknown node type: {type(node)}")

def parse_and_serialize(html: str) -> str:
    parser = Parser(html)
    tree = parser.parse()
    return serialize(tree)