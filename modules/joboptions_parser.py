"""
Joboptions Parser Modul

Dieses Modul extrahiert und dekodiert Beschreibungen aus Adobe .joboptions Dateien.
Es wandelt die hexadezimale UTF-16LE-Kodierung in lesbaren Text um und macht die
in den Dateien enthaltenen Beschreibungen für Benutzer zugänglich.
"""

import re
import os
import logging

def extract_description(joboptions_file_path):
    """
    Extrahiert die Beschreibung aus einer .joboptions-Datei und dekodiert sie in lesbaren Text.
    
    Args:
        joboptions_file_path (str): Pfad zur .joboptions-Datei
        
    Returns:
        dict: Wörterbuch mit Sprachcode-Schlüsseln und dekodierten Beschreibungen als Werten
              Beispiel: {'DEU': 'Deutsche Beschreibung', 'ENU': 'Englische Beschreibung'}
        None: Wenn keine Beschreibung gefunden oder ein Fehler aufgetreten ist
    """
    try:
        # Prüfen, ob die Datei existiert
        if not os.path.exists(joboptions_file_path):
            logging.error(f"Datei nicht gefunden: {joboptions_file_path}")
            return None
        
        # Datei öffnen und den Inhalt lesen
        with open(joboptions_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        
        # Nach dem Beschreibungsabschnitt suchen
        description_pattern = r'/Description\s*<<(.*?)>>'
        description_match = re.search(description_pattern, content, re.DOTALL)
        
        if not description_match:
            logging.info(f"Keine Beschreibung in der Datei gefunden: {joboptions_file_path}")
            return None
        
        description_content = description_match.group(1)
        
        # Alle Spracheinträge finden
        language_entries = re.finditer(r'/(\w{3})\s*<([^>]+)>', description_content)
        
        descriptions = {}
        
        for entry in language_entries:
            language_code = entry.group(1)  # z.B. 'DEU', 'ENU', etc.
            hex_description = entry.group(2)  # Hexadezimale Beschreibung
            
            # Den FFFE-Header entfernen, wenn vorhanden
            if hex_description.startswith('FFFE'):
                hex_description = hex_description[4:]
            
            # Hexadezimal in Bytes umwandeln
            try:
                # Alle nicht-hexadezimalen Zeichen entfernen (wie Leerzeichen)
                hex_description = ''.join(c for c in hex_description if c.isalnum())
                # In Bytes umwandeln
                byte_data = bytes.fromhex(hex_description)
                # Als UTF-16LE dekodieren (Little Endian)
                text = byte_data.decode('utf-16le')
                
                descriptions[language_code] = text
            except Exception as e:
                logging.error(f"Fehler beim Dekodieren der Beschreibung für {language_code}: {e}")
        
        return descriptions if descriptions else None
        
    except Exception as e:
        logging.error(f"Fehler beim Extrahieren der Beschreibung aus {joboptions_file_path}: {e}")
        return None

def get_readable_description(joboptions_file_path, preferred_languages=None):
    """
    Liefert eine lesbare Beschreibung aus einer .joboptions-Datei in der bevorzugten Sprache.
    
    Args:
        joboptions_file_path (str): Pfad zur .joboptions-Datei
        preferred_languages (list, optional): Liste der bevorzugten Sprachcodes in Reihenfolge der Präferenz
                                             z.B. ['DEU', 'ENU']. Standard ist ['DEU', 'ENU', 'FRA']
    
    Returns:
        str: Lesbare Beschreibung in der bevorzugten Sprache oder einer verfügbaren Alternative
        None: Wenn keine Beschreibung gefunden oder ein Fehler aufgetreten ist
    """
    if preferred_languages is None:
        preferred_languages = ['DEU', 'ENU', 'FRA']  # Deutsch, Englisch, Französisch als Standard
    
    descriptions = extract_description(joboptions_file_path)
    
    if not descriptions:
        return None
    
    # Versuche, eine Beschreibung in einer der bevorzugten Sprachen zu finden
    for lang in preferred_languages:
        if lang in descriptions:
            return descriptions[lang]
    
    # Wenn keine bevorzugte Sprache verfügbar ist, nimm die erste verfügbare
    return next(iter(descriptions.values()), None)

def get_all_descriptions(joboptions_file_path):
    """
    Gibt alle verfügbaren Beschreibungen aus einer .joboptions-Datei zurück.
    
    Args:
        joboptions_file_path (str): Pfad zur .joboptions-Datei
    
    Returns:
        dict: Wörterbuch mit Sprachcode-Schlüsseln und dekodierten Beschreibungen als Werten
        None: Wenn keine Beschreibung gefunden oder ein Fehler aufgetreten ist
    """
    return extract_description(joboptions_file_path)


# Beispielverwendung
if __name__ == "__main__":
    # Beispiel für die Verwendung des Moduls
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"Analysiere .joboptions-Datei: {file_path}")
        
        description = get_readable_description(file_path)
        if description:
            print("\nBeschreibung:")
            print("-" * 50)
            print(description)
            print("-" * 50)
        else:
            print("Keine lesbare Beschreibung gefunden.")
            
        all_descriptions = get_all_descriptions(file_path)
        if all_descriptions:
            print("\nAlle verfügbaren Beschreibungen:")
            for lang, desc in all_descriptions.items():
                print(f"\n{lang}:")
                print("-" * 50)
                print(desc)
                print("-" * 50)
    else:
        print("Bitte geben Sie den Pfad zu einer .joboptions-Datei an.")
        print("Beispiel: python joboptions_parser.py pfad/zur/datei.joboptions")