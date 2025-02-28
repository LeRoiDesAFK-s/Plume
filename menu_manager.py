# menu_manager.py
from PyQt5.QtWidgets import QMenu, QMenuBar
from settings import save_settings

DEFAULT_MENU_ORDER = ["Fichier", "Édition", "Formatage", "Insertion", "Personnalisation"]

class MenuManager:
    def __init__(self, main_window, actions, settings):
        self.main_window = main_window
        self.actions = actions
        self.settings = settings
        self.menus = {}
    
    def createMenus(self):
        menubar = self.main_window.menuBar()
        menu_order = self.settings.get("menuOrder", DEFAULT_MENU_ORDER)
        
        # Créer les menus
        self.menus["Fichier"] = menubar.addMenu("Fichier")
        self.menus["Édition"] = menubar.addMenu("Édition")
        self.menus["Formatage"] = menubar.addMenu("Formatage")
        self.menus["Insertion"] = menubar.addMenu("Insertion")
        self.menus["Personnalisation"] = menubar.addMenu("Personnalisation")

        # Ajouter les actions aux menus
        self.populateMenus()
        
        # Réordonner les menus selon les préférences
        self.updateMenuOrder(menu_order)
    
    def populateMenus(self):
        # Menu Fichier
        self.menus["Fichier"].addAction(self.actions["newAct"])
        self.menus["Fichier"].addAction(self.actions["openAct"])
        self.menus["Fichier"].addAction(self.actions["saveAct"])
        self.menus["Fichier"].addSeparator()
        self.menus["Fichier"].addAction(self.actions["exitAct"])

        # Menu Édition
        self.menus["Édition"].addAction(self.actions["undoAct"])
        self.menus["Édition"].addAction(self.actions["redoAct"])

        # Menu Formatage
        self.menus["Formatage"].addAction(self.actions["boldAct"])
        self.menus["Formatage"].addAction(self.actions["underlineAct"])
        self.menus["Formatage"].addAction(self.actions["italicAct"])
        self.menus["Formatage"].addAction(self.actions["subscriptAct"])
        self.menus["Formatage"].addAction(self.actions["superscriptAct"])

        # Menu Insertion
        self.menus["Insertion"].addAction(self.actions["insertImageAct"])

        # Menu Personnalisation
        self.menus["Personnalisation"].addAction(self.actions["remapAct"])
        self.menus["Personnalisation"].addAction(self.actions["reorderMenusAct"])
        self.menus["Personnalisation"].addSeparator()
        self.menus["Personnalisation"].addAction(self.actions["configToolbarAct"])
    
    def updateMenuOrder(self, menu_order):
        menubar = self.main_window.menuBar()
        for name in menu_order:
            if name in self.menus:
                menubar.removeAction(self.menus[name].menuAction())
                menubar.addMenu(self.menus[name])