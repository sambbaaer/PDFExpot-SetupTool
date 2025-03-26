# --------------------------------
# Imports und Module
# --------------------------------
import logging
from datetime import datetime
import os
import sys

# Füge das Elternverzeichnis zum Pfad hinzu, damit die Module gefunden werden
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# CustomTkinter für die GUI (muss installiert sein)
try:
    import customtkinter as ctk
except ImportError:
    print("Fehler: CustomTkinter ist nicht installiert.")
    print("Bitte installieren Sie es mit: pip install customtkinter")
    sys.exit(1)

# --------------------------------
# Grundlegende Konfiguration
# --------------------------------

# CustomTkinter Konfiguration
ctk.set_appearance_mode("light")  # Helles Design für vertrauenswürdige Optik
ctk.set_default_color_theme("blue")  # Professionelles Farbschema

# Logging konfigurieren
log_file_name = "error_log.txt"
logging.basicConfig(
    filename=log_file_name, 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    filemode='a'  # Anhängen statt Überschreiben
)

# Module importieren
try:
    from modules.gui import PDFExportEinstellungenGUI
except ImportError as e:
    logging.critical(f"Fehler beim Importieren der Module: {e}")
    print(f"Kritischer Fehler: Module konnten nicht geladen werden: {e}")
    print("Bitte stellen Sie sicher, dass alle Dateien im richtigen Verzeichnis liegen.")
    sys.exit(1)

# --------------------------------
# Hauptfunktion
# --------------------------------

def main():
    """
    Hauptfunktion zur Ausführung der Anwendung.
    """
    try:
        logging.info("Anwendung gestartet")
        app = PDFExportEinstellungenGUI()
        app.mainloop()
    except Exception as e:
        logging.critical(f"Unbehandelte Ausnahme: {e}", exc_info=True)
        # Hier könnte eine Benachrichtigung an den Benutzer angezeigt werden
        raise

# --------------------------------
# Programm starten
# --------------------------------

if __name__ == "__main__":
    main()