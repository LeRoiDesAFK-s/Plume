# action_factory.py
from PyQt5.QtWidgets import QAction
from image_handler import insert_image

class ActionFactory:
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings = main_window.settings
    
    def createActions(self):
        actions = {}
        
        # Actions Fichier
        actions["newAct"] = QAction("Nouveau", self.main_window)
        actions["newAct"].triggered.connect(self.main_window.addNewTab)
        
        actions["openAct"] = QAction("Ouvrir...", self.main_window)
        actions["openAct"].triggered.connect(self.main_window.openFile)
        
        actions["saveAct"] = QAction("Sauvegarder", self.main_window)
        actions["saveAct"].triggered.connect(self.main_window.saveFile)
        
        actions["exitAct"] = QAction("Quitter", self.main_window)
        actions["exitAct"].triggered.connect(self.main_window.close)

        # Actions Édition
        actions["undoAct"] = QAction("Annuler", self.main_window)
        actions["undoAct"].setShortcut("Ctrl+Z")
        actions["undoAct"].triggered.connect(self.onUndo)
        
        actions["redoAct"] = QAction("Refaire", self.main_window)
        actions["redoAct"].setShortcut("Ctrl+Y")
        actions["redoAct"].triggered.connect(self.onRedo)

        # Actions Formatage
        actions["boldAct"] = QAction("Gras", self.main_window)
        actions["boldAct"].setShortcut("Ctrl+B")
        actions["boldAct"].triggered.connect(self.onBold)
        
        actions["underlineAct"] = QAction("Souligné", self.main_window)
        actions["underlineAct"].setShortcut("Ctrl+U")
        actions["underlineAct"].triggered.connect(self.onUnderline)
        
        actions["italicAct"] = QAction("Italique", self.main_window)
        actions["italicAct"].setShortcut("Ctrl+I")
        actions["italicAct"].triggered.connect(self.onItalic)
        
        actions["subscriptAct"] = QAction("Indice", self.main_window)
        actions["subscriptAct"].setShortcut("Ctrl+=")
        actions["subscriptAct"].triggered.connect(self.onSubscript)
        
        actions["superscriptAct"] = QAction("Exposant", self.main_window)
        actions["superscriptAct"].setShortcut("Ctrl++")
        actions["superscriptAct"].triggered.connect(self.onSuperscript)

        # Actions Insertion
        actions["insertImageAct"] = QAction("Insérer une image", self.main_window)
        actions["insertImageAct"].triggered.connect(self.onInsertImage)

        # Actions Personnalisation
        actions["remapAct"] = QAction("Remapper les raccourcis", self.main_window)
        actions["remapAct"].triggered.connect(self.onRemapShortcuts)
        
        actions["reorderMenusAct"] = QAction("Réorganiser les menus", self.main_window)
        actions["reorderMenusAct"].triggered.connect(self.onReorderMenus)
        
        actions["configToolbarAct"] = QAction("Configurer la barre d'outils", self.main_window)
        actions["configToolbarAct"].triggered.connect(self.onConfigToolbar)

        # Appliquer les raccourcis personnalisés
        self.applyCustomShortcuts(actions)
        
        return actions
    
    def applyCustomShortcuts(self, actions):
        sc = self.settings.get("shortcuts", {})
        for name, shortcut in sc.items():
            for act in actions.values():
                if act.text() == name:
                    act.setShortcut(shortcut)
                    break
    
    # Méthodes de callback
    def onUndo(self):
        editor = self.main_window.currentEditor()
        if editor:
            editor.undo()
    
    def onRedo(self):
        editor = self.main_window.currentEditor()
        if editor:
            editor.redo()
    
    def onBold(self):
        editor = self.main_window.currentEditor()
        if editor:
            editor.toggleBoldFormat()
    
    def onUnderline(self):
        editor = self.main_window.currentEditor()
        if editor:
            editor.toggleUnderlineFormat()
    
    def onItalic(self):
        editor = self.main_window.currentEditor()
        if editor:
            editor.toggleItalicFormat()
    
    def onSubscript(self):
        editor = self.main_window.currentEditor()
        if editor:
            editor.applySubscriptFormat()
    
    def onSuperscript(self):
        editor = self.main_window.currentEditor()
        if editor:
            editor.applySuperscriptFormat()
    
    def onInsertImage(self):
        editor = self.main_window.currentEditor()
        if editor:
            insert_image(editor)
    
    def onRemapShortcuts(self):
        from shortcuts_dialog import ShortcutsDialog
        actions_dict = {act.text(): act for act in self.main_window.actions.values()}
        dlg = ShortcutsDialog(actions_dict, self.main_window)
        dlg.exec_()
    
    def onReorderMenus(self):
        from menu_reorder_dialog import MenuReorderDialog
        current_order = self.settings.get("menuOrder", ["Fichier", "Édition", "Formatage", "Insertion", "Personnalisation"])
        dialog = MenuReorderDialog(current_order, self.main_window)
        if dialog.exec_() == MenuReorderDialog.Accepted:
            new_order = dialog.getNewOrder()
            if new_order:
                self.settings["menuOrder"] = new_order
                save_settings(self.settings)
                self.main_window.menuManager.updateMenuOrder(new_order)
    
    def onConfigToolbar(self):
        from toolbar_customization_dialog import ToolbarCustomizationDialog
        actions_list = [(act.text(), act) for act in self.main_window.actions.values()]
        current_selection = self.settings.get("customToolbarActions", [])
        dialog = ToolbarCustomizationDialog(actions_list, current_selection, self.main_window)
        if dialog.exec_() == ToolbarCustomizationDialog.Accepted:
            new_selection = dialog.getSelectedActions()
            self.settings["customToolbarActions"] = new_selection
            save_settings(self.settings)
            self.main_window.toolbarManager.updateToolbar(new_selection)