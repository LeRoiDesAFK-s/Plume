# shortcuts_dialog.py
import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDialogButtonBox
from settings import SETTINGS_FILE, load_settings, save_settings

class ShortcutsDialog(QDialog):
    def __init__(self, actions, parent=None):
        """
        actions: dict de la forme { 'NomAction': QAction, ... }
        """
        super().__init__(parent)
        self.setWindowTitle("Remappage des raccourcis")
        self.actions = actions
        self.settings = load_settings()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.edit_fields = {}
        for name, action in self.actions.items():
            hbox = QHBoxLayout()
            label = QLabel(name)
            le = QLineEdit()
            # Remplir avec le raccourci actuel (ou celui sauvegardé)
            default_shortcut = action.shortcut().toString() if action.shortcut() else ""
            saved = self.settings.get("shortcuts", {}).get(name, default_shortcut)
            le.setText(saved)
            self.edit_fields[name] = le
            hbox.addWidget(label)
            hbox.addWidget(le)
            layout.addLayout(hbox)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.applyShortcuts)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def applyShortcuts(self):
        if "shortcuts" not in self.settings:
            self.settings["shortcuts"] = {}
        for name, le in self.edit_fields.items():
            new_sc = le.text().strip()
            if new_sc:
                self.actions[name].setShortcut(new_sc)
                self.settings["shortcuts"][name] = new_sc
        save_settings(self.settings)
        self.accept()
