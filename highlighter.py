from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QFont

class MarkdownHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self._highlighting_rules = []

        # Règle pour **gras**
        bold_format = QTextCharFormat()
        bold_format.setFontWeight(QFont.Bold)
        pattern_bold = QRegExp(r"\*\*(.+?)\*\*")
        self._highlighting_rules.append((pattern_bold, bold_format))

        # Règle pour __souligné__
        underline_format = QTextCharFormat()
        underline_format.setFontUnderline(True)
        pattern_underline = QRegExp(r"__(.+?)__")
        self._highlighting_rules.append((pattern_underline, underline_format))

        # Règle pour --italique--
        italic_format = QTextCharFormat()
        italic_format.setFontItalic(True)
        pattern_italic = QRegExp(r"--(.+?)--")
        self._highlighting_rules.append((pattern_italic, italic_format))

        # Règle pour _indice exposant_
        subscript_format = QTextCharFormat()
        # Pour simuler un indice, on réduit la taille et on aligne en bas.
        subscript_format.setFontPointSize(10)
        subscript_format.setVerticalAlignment(QTextCharFormat.AlignSubScript)
        pattern_subscript = QRegExp(r"_(.+?)_")
        self._highlighting_rules.append((pattern_subscript, subscript_format))

    def highlightBlock(self, text):
        for pattern, fmt in self._highlighting_rules:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                if length > 0:
                    self.setFormat(index, length, fmt)
                index = pattern.indexIn(text, index + length)
