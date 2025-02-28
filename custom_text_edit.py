# custom_text_edit.py
from PyQt5.QtWidgets import QTextEdit, QDialog
from PyQt5.QtGui import QTextImageFormat
from image_editor import ImageEditorDialog

class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def mouseDoubleClickEvent(self, event):
        cursor = self.cursorForPosition(event.pos())
        fmt = cursor.charFormat()
        if fmt.isImageFormat():
            # Récupérer le chemin de l'image
            imgFormat = fmt.toImageFormat()
            imgSrc = imgFormat.property(QTextImageFormat.ImageName)
            dialog = ImageEditorDialog(imgSrc, self)
            if dialog.exec_() == QDialog.Accepted:
                editedPixmap = dialog.getEditedPixmap()
                if editedPixmap:
                    # Sauvegarder l'image éditée dans un fichier temporaire
                    tempPath = "temp_image.png"
                    editedPixmap.save(tempPath, "PNG")
                    cursor.deleteChar()
                    cursor.insertImage(tempPath)
            return
        super().mouseDoubleClickEvent(event)

    def toggleItalicFormat(self):
        """Toggle italic format for selected text or at current cursor position"""
        cursor = self.textCursor()
        format = cursor.charFormat()
        format.setFontItalic(not format.fontItalic())
        
        if cursor.hasSelection():
            cursor.mergeCharFormat(format)
        else:
            self.setCurrentCharFormat(format)

    def toggleBoldFormat(self):
        """Toggle bold format for selected text or at current cursor position"""
        cursor = self.textCursor()
        format = cursor.charFormat()
        format.setFontWeight(700 if format.fontWeight() == 400 else 400)  # 400=normal, 700=bold
        
        if cursor.hasSelection():
            cursor.mergeCharFormat(format)
        else:
            self.setCurrentCharFormat(format)

    def toggleUnderlineFormat(self):
        """Toggle underline format for selected text or at current cursor position"""
        cursor = self.textCursor()
        format = cursor.charFormat()
        format.setFontUnderline(not format.fontUnderline())
        
        if cursor.hasSelection():
            cursor.mergeCharFormat(format)
        else:
            self.setCurrentCharFormat(format)

    def toggleSuperscriptFormat(self):
        """Toggle superscript format for selected text or at current cursor position"""
        cursor = self.textCursor()
        format = cursor.charFormat()
        current = format.verticalAlignment()
        new = (QTextCharFormat.AlignNormal 
               if current == QTextCharFormat.AlignSuperScript 
               else QTextCharFormat.AlignSuperScript)
        format.setVerticalAlignment(new)
        
        if cursor.hasSelection():
            cursor.mergeCharFormat(format)
        else:
            self.setCurrentCharFormat(format)

    def toggleSubscriptFormat(self):
        """Toggle subscript format for selected text or at current cursor position"""
        cursor = self.textCursor()
        format = cursor.charFormat()
        current = format.verticalAlignment()
        new = (QTextCharFormat.AlignNormal 
               if current == QTextCharFormat.AlignSubScript 
               else QTextCharFormat.AlignSubScript)
        format.setVerticalAlignment(new)
        
        if cursor.hasSelection():
            cursor.mergeCharFormat(format)
        else:
            self.setCurrentCharFormat(format)
