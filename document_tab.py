# document_tab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from custom_text_edit import CustomTextEdit

class DocumentTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = CustomTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        self.setLayout(layout)
