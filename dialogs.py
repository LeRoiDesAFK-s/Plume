from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialogButtonBox

class FindReplaceDialog(QDialog):
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setWindowTitle("Rechercher / Remplacer")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Rechercher :"))
        self.findLineEdit = QLineEdit()
        layout.addWidget(self.findLineEdit)
        layout.addWidget(QLabel("Remplacer par :"))
        self.replaceLineEdit = QLineEdit()
        layout.addWidget(self.replaceLineEdit)
        self.btnFind = QPushButton("Rechercher")
        self.btnReplace = QPushButton("Remplacer")
        btnBox = QDialogButtonBox(QDialogButtonBox.Close)
        layout.addWidget(self.btnFind)
        layout.addWidget(self.btnReplace)
        layout.addWidget(btnBox)
        self.setLayout(layout)
