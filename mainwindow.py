# mainwindow.py
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMessageBox, QFileDialog, QStatusBar
from PyQt5.QtCore import QTimer
from document_tab import DocumentTab
from settings import load_settings, save_settings
from menu_manager import MenuManager
from toolbar_manager import ToolbarManager
from action_factory import ActionFactory
import os, time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plume Editor")
        self.resize(1400, 900)
        self.settings = load_settings()
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)
        
        self.actionFactory = ActionFactory(self)
        self.actions = self.actionFactory.createActions()
        
        self.menuManager = MenuManager(self, self.actions, self.settings)
        self.menuManager.createMenus()
        
        self.toolbarManager = ToolbarManager(self, self.actions, self.settings)
        self.toolbarManager.createToolbars()
        
        self.createStatusBar()
        self.addNewTab()
        self.last_modified = time.time()

        self.initAutoSave()
    
    def initAutoSave(self):
        self.autosave_interval = self.settings.get("autosave_interval", 60) * 1000
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.autoSave)
        self.autosave_timer.start(self.autosave_interval)

    def createStatusBar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Prêt")

    def currentDocumentTab(self):
        return self.tabWidget.currentWidget()

    def currentEditor(self):
        tab = self.currentDocumentTab()
        if tab:
            return tab.editor
        return None

    def addNewTab(self):
        tab = DocumentTab()
        index = self.tabWidget.addTab(tab, "Document {}".format(self.tabWidget.count() + 1))
        self.tabWidget.setCurrentIndex(index)

    def openFile(self):
        path, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", "Fichiers HTML (*.htm *.html);;Tous (*.*)")
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                tab = DocumentTab()
                tab.editor.setHtml(content)
                index = self.tabWidget.addTab(tab, os.path.basename(path))
                self.tabWidget.setCurrentIndex(index)
                self.statusbar.showMessage("Fichier ouvert", 2000)
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir le fichier : {e}")

    def saveFile(self):
        current = self.currentDocumentTab()
        if current is None:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Sauvegarder", "", "Fichiers HTML (*.htm *.html);;Tous (*.*)")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(current.editor.toHtml())
                self.tabWidget.setTabText(self.tabWidget.currentIndex(), os.path.basename(path))
                self.statusbar.showMessage("Fichier sauvegardé", 2000)
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de sauvegarder le fichier : {e}")

    def autoSave(self):
        current = self.currentDocumentTab()
        if current:
            try:
                with open("autosave_tmp.html", "w", encoding="utf-8") as f:
                    f.write(current.editor.toHtml())
                self.statusbar.showMessage("Document autosauvé", 1500)
            except Exception as e:
                print(f"Erreur d'autosave : {e}")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Quitter", "Voulez-vous sauvegarder avant de quitter ?",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.saveFile()
            event.accept()
        elif reply == QMessageBox.No:
            event.accept()
        else:
            event.ignore()