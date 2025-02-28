# format_handler.py
from PyQt5.QtGui import QFont, QTextCharFormat

def applyFormatToEditor(editor, format_type):
    """
    Applique un formatage spécifique au texte dans l'éditeur
    """
    if not editor:
        return
    
    cursor = editor.textCursor()
    fmt = cursor.charFormat()
    
    if format_type == "bold":
        fmt.setFontWeight(QFont.Bold if fmt.fontWeight() != QFont.Bold else QFont.Normal)
    elif format_type == "italic":
        fmt.setFontItalic(not fmt.fontItalic())
    elif format_type == "underline":
        fmt.setFontUnderline(not fmt.fontUnderline())
    elif format_type == "subscript":
        if fmt.verticalAlignment() == QTextCharFormat.AlignSubScript:
            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)
            fmt.setFontPointSize(editor.default_font_size)
        else:
            fmt.setVerticalAlignment(QTextCharFormat.AlignSubScript)
            fmt.setFontPointSize(editor.default_font_size * 0.8)
    elif format_type == "superscript":
        if fmt.verticalAlignment() == QTextCharFormat.AlignSuperScript:
            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)
            fmt.setFontPointSize(editor.default_font_size)
        else:
            fmt.setVerticalAlignment(QTextCharFormat.AlignSuperScript)
            fmt.setFontPointSize(editor.default_font_size * 0.8)
    
    if cursor.hasSelection():
        cursor.mergeCharFormat(fmt)
    else:
        editor.mergeCurrentCharFormat(fmt)