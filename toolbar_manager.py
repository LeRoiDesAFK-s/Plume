# toolbar_manager.py
from PyQt5.QtWidgets import QToolBar

class ToolbarManager:
    def __init__(self, main_window, actions, settings):
        self.main_window = main_window
        self.actions = actions
        self.settings = settings
        self.customToolbar = None
    
    def createToolbars(self):
        self.customToolbar = QToolBar("Barre Personnalisée")
        self.customToolbar.setMovable(True)
        self.main_window.addToolBar(self.customToolbar)
        
        # Ajouter les actions configurées à la barre d'outils
        custom_actions = self.settings.get("customToolbarActions", [])
        self.updateToolbar(custom_actions)
    
    def updateToolbar(self, action_names):
        self.customToolbar.clear()
        for action_name in action_names:
            for act in self.actions.values():
                if act.text() == action_name:
                    self.customToolbar.addAction(act)
                    break