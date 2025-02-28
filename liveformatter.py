# liveformatter.py
import re
from html import escape

def auto_format_text(html):
    # Dictionnaire pour stocker les balises <img> trouvées
    img_tags = {}
    img_counter = 0
    
    def img_replacer(match):
        nonlocal img_counter
        key = f"<<<IMG_{img_counter}>>>"
        img_counter += 1
        img_tags[key] = match.group(0)
        return key

    # Remplacer temporairement les balises <img>
    temp_html = re.sub(r'<img[^>]+?/>', img_replacer, html)
    
    # Éviter le formatage à l'intérieur des balises HTML existantes
    def format_outside_tags(text, pattern, replacement):
        parts = re.split(r'(<[^>]*>)', text)
        for i in range(0, len(parts), 2):
            if not parts[i].strip():
                continue
            parts[i] = re.sub(pattern, replacement, parts[i])
        return ''.join(parts)
    
    # Effectuer les remplacements avec des regex non-gourmands
    replacements = [
        (r'\*\*([^\*\n]+?)\*\*', r'<b>\1</b>'),
        (r'__([^_\n]+?)__', r'<u>\1</u>'), 
        (r'--([^-\n]+?)--', r'<i>\1</i>'),
        (r'_([^_\n]+?)_', r'<sub>\1</sub>')
    ]
    
    for pattern, replacement in replacements:
        temp_html = format_outside_tags(temp_html, pattern, replacement)

    # Restaurer les balises <img>
    for key, tag in img_tags.items():
        temp_html = temp_html.replace(key, tag)
        
    return temp_html
