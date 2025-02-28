# editor.py
from PyQt5.QtWidgets import QTextEdit, QUndoStack
from PyQt5.QtGui import QFont, QTextCursor, QTextCharFormat
from PyQt5.QtCore import pyqtSignal, QTimer
from liveformatter import auto_format_text
from format_handler import applyFormatToEditor
import re

class EditorWidget(QTextEdit):
    textModified = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_font_size = 12
        self.setFont(QFont("Consolas", self.default_font_size))
        self.undoStack = QUndoStack(self)
        self.setAcceptDrops(True)
        self.format_timer = QTimer(self)
        self.format_timer.setSingleShot(True)
        self.format_timer.timeout.connect(self.autoFormat)
        self.textChanged.connect(self.onTextChanged)

    def onTextChanged(self):
        self.format_timer.start(300)
        self.textModified.emit()

    def autoFormat(self):
        self.blockSignals(True)
        current_html = self.toHtml()
        if not re.search(r'(\*\*.+?\*\*|__.+?__|--.+?--|_.+?_)', current_html):
            self.blockSignals(False)
            return
        new_html = auto_format_text(current_html)
        if new_html != current_html:
            cursor = self.textCursor()
            pos = cursor.position()
            self.setHtml(new_html)
            new_cursor = self.textCursor()
            new_position = pos if pos <= len(self.toPlainText()) else len(self.toPlainText())
            new_cursor.setPosition(new_position)
            self.setTextCursor(new_cursor)
        self.blockSignals(False)

    # Méthodes de formatage qui utilisent le gestionnaire de formatage
    def toggleBoldFormat(self):
        applyFormatToEditor(self, "bold")

    def toggleItalicFormat(self):
        applyFormatToEditor(self, "italic")

    def toggleUnderlineFormat(self):
        applyFormatToEditor(self, "underline")

    def applySubscriptFormat(self):
        applyFormatToEditor(self, "subscript")

    def applySuperscriptFormat(self):
        applyFormatToEditor(self, "superscript")