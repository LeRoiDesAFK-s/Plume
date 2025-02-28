# image_handler.py
import base64
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from image_editor import ImageEditorDialog
from PyQt5.QtCore import QBuffer, QIODevice

def insert_image(editor):
    """
    Ouvre une boîte de dialogue pour sélectionner une image, permet à l'utilisateur
    de modifier l'image via l'éditeur d'image, puis insère l'image incrustée dans le texte
    sous forme d'un data URI dans une balise <img>.
    """
    path, _ = QFileDialog.getOpenFileName(editor, "Insérer une image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
    if not path:
        QMessageBox.information(editor, "Insertion d'image", "Aucune image sélectionnée.")
        return

    # Ouvrir le dialogue d'édition d'image
    dialog = ImageEditorDialog(path, editor)
    if dialog.exec_() == ImageEditorDialog.Accepted:
        edited_pixmap = dialog.getEditedPixmap()
        if edited_pixmap:
            # Convertir le pixmap en données PNG en mémoire
            buffer = QBuffer()
            buffer.open(QIODevice.WriteOnly)
            edited_pixmap.save(buffer, "PNG")
            img_bytes = buffer.data()
            # Encoder les données en base64
            base64_data = base64.b64encode(img_bytes).decode('utf-8')
            # Créer un data URI pour une image PNG
            data_uri = f"data:image/png;base64,{base64_data}"
            # Créer la balise HTML pour l'image
            img_tag = f'<img src="{data_uri}" alt="Image" />'
            cursor = editor.textCursor()
            cursor.insertHtml(img_tag)
