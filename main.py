import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
import json
import logging
from datetime import datetime
import getpass  # Für den Benutzernamen
import sys  # Für die Erkennung des Betriebssystems

# Logging konfigurieren
log_file_name = "error_log.txt"  # Konstanten Dateinamen für die Logdatei verwenden
logging.basicConfig(filename=log_file_name, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a') #filemode='a' um anzuhängen

def lade_konfigurationen(datei_pfad):
    """
    Lädt Konfigurationen aus einer JSON-Datei.

    Args:
        datei_pfad (str): Der Pfad zur JSON-Datei.

    Returns:
        dict: Die geladenen Konfigurationen oder None bei Fehler.
    """
    try:
        with open(datei_pfad, 'r', encoding='utf-8') as f:
            konfigurationen = json.load(f)
        logging.info(f"Konfigurationen erfolgreich von {datei_pfad} geladen.")
        return konfigurationen
    except FileNotFoundError:
        messagebox.showerror("Fehler", f"Konfigurationsdatei nicht gefunden: {datei_pfad}")
        logging.error(f"Konfigurationsdatei nicht gefunden: {datei_pfad}")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Fehler", f"Fehler beim Lesen der JSON-Datei: {datei_pfad}")
        logging.error(f"Fehler beim Lesen der JSON-Datei: {datei_pfad}")
        return None
    except Exception as e:
        messagebox.showerror("Fehler", f"Unerwarteter Fehler beim Laden der Konfigurationen: {e}")
        logging.error(f"Unerwarteter Fehler beim Laden der Konfigurationen: {e}")
        return None

def installiere_einstellungen():
    """
    Installiert die ausgewählten PDF-Exporteinstellungen.
    """
    ausgewaehlte_einstellung = einstellungs_liste.get(einstellungs_liste.curselection())
    einstellungen = lade_konfigurationen("config/settings.json")
    verzeichnisse = lade_konfigurationen("config/currentDirectories.json")

    if einstellungen is None or verzeichnisse is None:
        return  # Beende die Funktion, wenn die Konfigurationen nicht geladen werden konnten.

    for einstellung in einstellungen:
        if einstellung["Name"] == ausgewaehlte_einstellung:
            adobe_pdf_setting_name = einstellung["Adobe PDF Settings"]
            color_setting_name = einstellung["Color Setting"]
            icc_profil_name = einstellung["ICC-Profil"]

            # Benutzername ermitteln
            benutzername = getpass.getuser()

            # Betriebssystem ermitteln und entsprechende Verzeichnisse wählen
            if sys.platform == "win32":
                betriebssystem = "windows"
            elif sys.platform == "darwin":
                betriebssystem = "mac"
            else:
                messagebox.showerror("Fehler", "Unbekanntes Betriebssystem.  Installation abgebrochen.")
                logging.error(f"Unbekanntes Betriebssystem: {sys.platform}")
                return

            # Zielverzeichnisse aus der Konfiguration laden und anpassen
            pdf_settings_zielverzeichnis = verzeichnisse[betriebssystem]["adobe_pdf_settings_pfad"].replace("%USERNAME%", benutzername)
            color_settings_zielverzeichnis = verzeichnisse[betriebssystem]["color_settings_pfad"].replace("%USERNAME%", benutzername)
            icc_profile_zielverzeichnis = verzeichnisse[betriebssystem]["icc_profile_pfad"].replace("%USERNAME%", benutzername)

            # Prüfen, ob die Zielverzeichnisse existieren, und ggf. erstellen
            for ziel_verzeichnis in [pdf_settings_zielverzeichnis, color_settings_zielverzeichnis, icc_profile_zielverzeichnis]:
                if ziel_verzeichnis and not os.path.exists(ziel_verzeichnis):
                    try:
                        os.makedirs(ziel_verzeichnis)
                        logging.info(f"Verzeichnis erstellt: {ziel_verzeichnis}")
                    except Exception as e:
                        messagebox.showerror("Fehler", f"Verzeichnis konnte nicht erstellt werden: {ziel_verzeichnis} - {e}")
                        logging.error(f"Verzeichnis konnte nicht erstellt werden: {ziel_verzeichnis} - {e}")
                        return  # Abbruch, wenn ein Verzeichnis nicht erstellt werden kann

            # Kopieroperationen mit Fehlerbehandlung und Logging
            try:
                # Kopiere nur, wenn der Dateiname nicht leer ist
                if adobe_pdf_setting_name:
                    quelle_pdf_setting = os.path.join("resources", adobe_pdf_setting_name) # Dateien liegen jetzt im Ordner "resources"
                    shutil.copy2(quelle_pdf_setting, pdf_settings_zielverzeichnis)
                    logging.info(f"Datei kopiert: {quelle_pdf_setting} nach {pdf_settings_zielverzeichnis}")
                if color_setting_name:
                    quelle_color_setting = os.path.join("resources", color_setting_name)
                    shutil.copy2(quelle_color_setting, color_settings_zielverzeichnis)
                    logging.info(f"Datei kopiert: {quelle_color_setting} nach {color_settings_zielverzeichnis}")
                if icc_profil_name:
                    quelle_icc_profil = os.path.join("resources", icc_profil_name)
                    shutil.copy2(quelle_icc_profil, icc_profile_zielverzeichnis)
                    logging.info(f"Datei kopiert: {quelle_icc_profil} nach {icc_profile_zielverzeichnis}")
            except FileNotFoundError as e:
                messagebox.showerror("Fehler", f"Datei nicht gefunden: {e.filename}")
                logging.error(f"Datei nicht gefunden: {e}")
                return  # Abbruch, wenn eine Datei nicht gefunden wird
            except shutil.Error as e:
                messagebox.showerror("Fehler", f"Kopierfehler: {e}")
                logging.error(f"Kopierfehler: {e}")
                return  # Abbruch bei einem Kopierfehler
            except Exception as e:
                messagebox.showerror("Fehler", f"Unerwarteter Fehler: {e}")
                logging.error(f"Unerwarteter Fehler: {e}")
                return  # Abbruch bei einem unerwarteten Fehler

            messagebox.showinfo("Installation", f"Einstellungen für '{ausgewaehlte_einstellung}' installiert.")
            logging.info(f"Einstellungen für '{ausgewaehlte_einstellung}' installiert.")
            return  # Wichtig: Nach erfolgreicher Installation die Funktion beenden

    # Wenn die Schleife durchlaufen wurde, ohne die Einstellung zu finden:
    messagebox.showerror("Fehler", f"Einstellung '{ausgewaehlte_einstellung}' nicht gefunden.")
    logging.error(f"Einstellung '{ausgewaehlte_einstellung}' nicht gefunden.")

# Hauptfenster erstellen
fenster = tk.Tk()
fenster.title("PDF-Export Einstellungen Installer")
fenster.geometry("600x400")  # Fenstergröße angepasst

# Konfigurationsdatei laden
einstellungen_daten = lade_konfigurationen("config/settings.json")
if einstellungen_daten is None:
    # Wenn das Laden der Konfiguration fehlschlägt, wird das Programm beendet.
    fenster.destroy()
    exit()

# Listbox für die Einstellungen
einstellungs_label = tk.Label(fenster, text="Verfügbare Einstellungen:")
einstellungs_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
einstellungs_liste = tk.Listbox(fenster, height=10, width=60, selectmode=tk.SINGLE)
einstellungs_liste.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Füge die Namen der Einstellungen hinzu.
for einstellung in einstellungen_daten:
    einstellungs_liste.insert(tk.END, einstellung["Name"])

# Button zum Installieren der Einstellungen
installieren_button = tk.Button(fenster, text="Installieren", command=installiere_einstellungen)
installieren_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Starte die GUI-Hauptschleife
fenster.mainloop()