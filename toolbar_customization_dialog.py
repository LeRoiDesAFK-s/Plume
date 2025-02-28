# toolbar_customization_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox, QLabel, QWidget, QScrollArea

class ToolbarCustomizationDialog(QDialog):
    def __init__(self, actions, current_selection, parent=None):
        """
        actions: list de tuples (action_name, QAction)
        current_selection: liste des noms d'actions actuellement sélectionnées pour la barre personnalisée
        """
        super().__init__(parent)
        self.setWindowTitle("Personnaliser la barre d'outils")
        self.actions = actions
        self.current_selection = set(current_selection)
        self.checkbox_dict = {}
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        label = QLabel("Sélectionnez les actions à afficher dans la barre d'outils:")
        layout.addWidget(label)

        # Utilisation d'un QScrollArea au cas où il y ait beaucoup d'actions
        scroll = QScrollArea(self)
        scroll_widget = QWidget()
        vbox = QVBoxLayout(scroll_widget)
        for name, act in self.actions:
            cb = QCheckBox(name)
            cb.setChecked(name in self.current_selection)
            vbox.addWidget(cb)
            self.checkbox_dict[name] = cb
        scroll_widget.setLayout(vbox)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getSelectedActions(self):
        """Retourne la liste des noms d'actions sélectionnées."""
        return [name for name, cb in self.checkbox_dict.items() if cb.isChecked()]
