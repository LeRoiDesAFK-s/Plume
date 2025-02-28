# launcher.py
import sys
from PyQt5.QtWidgets import QApplication
import qdarkstyle
from mainwindow import MainWindow
import settings

def main():
    app = QApplication(sys.argv)
    app_settings = settings.load_settings()

    # Appliquer le thème
    applyTheme(app, app_settings)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

def applyTheme(app, settings):
    theme = settings.get("theme", "dark")
    if theme == "dark":
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    else:
        app.setStyleSheet("")

if __name__ == '__main__':
    main()