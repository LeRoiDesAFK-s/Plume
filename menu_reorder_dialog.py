# menu_reorder_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QDialogButtonBox

class MenuReorderDialog(QDialog):
    def __init__(self, current_order, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Réorganiser les menus")
        self.resize(300, 400)
        self.current_order = current_order
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Liste widget avec drag & drop interne
        self.listWidget = QListWidget(self)
        self.listWidget.setDragDropMode(QListWidget.InternalMove)
        for name in self.current_order:
            item = QListWidgetItem(name)
            self.listWidget.addItem(item)
        layout.addWidget(self.listWidget)
        
        # Boutons OK et Annuler
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def getNewOrder(self):
        new_order = []
        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            new_order.append(item.text())
        return new_order
