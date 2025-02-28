from PyQt5.QtWidgets import QUndoCommand

class TextEditCommand(QUndoCommand):
    def __init__(self, editor, old_text, new_text, cursor_pos, description="Modification"):
        super().__init__(description)
        self.editor = editor
        self.old_text = old_text
        self.new_text = new_text
        self.cursor_pos = cursor_pos

    def undo(self):
        self.editor.blockSignals(True)
        self.editor.setPlainText(self.old_text)
        cursor = self.editor.textCursor()
        cursor.setPosition(self.cursor_pos)
        self.editor.setTextCursor(cursor)
        self.editor.blockSignals(False)

    def redo(self):
        self.editor.blockSignals(True)
        self.editor.setPlainText(self.new_text)
        cursor = self.editor.textCursor()
        cursor.setPosition(self.cursor_pos)
        self.editor.setTextCursor(cursor)
        self.editor.blockSignals(False)
