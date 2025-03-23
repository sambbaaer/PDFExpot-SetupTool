"""
Utilities-Modul für PDF-Export-Einstellungen-Installer

Dieses Modul enthält Hilfsfunktionen, die von anderen Modulen der Anwendung 
verwendet werden, wie z.B. Funktionen zum Laden von Konfigurationen, 
zur Pfadvalidierung und zur Systemerkennung.
"""

import os
import json
import sys
import logging
import getpass
import glob
import subprocess
from tkinter import messagebox
import pathlib
import shutil

def get_application_path():
    """
    Ermittelt den Pfad, in dem die Anwendung ausgeführt wird,
    unabhängig davon, ob es sich um eine .py-Datei oder eine kompilierte EXE handelt.
    
    Returns:
        str: Pfad zum Anwendungsverzeichnis
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller erzeugt einen temporären Ordner und speichert den Pfad in _MEIPASS
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS
        else:
            # Wenn es eine kompilierte ausführbare Datei ist, aber kein _MEIPASS
            return os.path.dirname(sys.executable)
    else:
        # Normales Python-Skript
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_config_search_paths(config_filename):
    """
    Ermittelt alle Pfade, in denen nach Konfigurationsdateien gesucht werden soll.
    
    Args:
        config_filename (str): Der Name der Konfigurationsdatei
        
    Returns:
        list: Liste mit möglichen Pfaden, in priorisierter Reihenfolge
    """
    app_path = get_application_path()
    
    # Benutzerverzeichnis für Konfigurationsdateien
    if sys.platform == "win32":
        user_config_dir = os.path.join(os.environ.get('APPDATA', ''), "PDFExportInstaller", "config")
    elif sys.platform == "darwin":  # macOS
        user_config_dir = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "PDFExportInstaller", "config")
    else:  # Linux und andere
        user_config_dir = os.path.join(os.path.expanduser("~"), ".config", "PDFExportInstaller", "config")
    
    # Pfade in der Reihenfolge der Priorität
    search_paths = [
        os.path.join(os.path.dirname(app_path), "config", config_filename),  # Neben der EXE im "config"-Ordner
        os.path.join(app_path, "config", config_filename),                   # Im App-Verzeichnis
        os.path.join(user_config_dir, config_filename),                      # Im Benutzerverzeichnis
        os.path.join(os.getcwd(), "config", config_filename)                 # Im aktuellen Arbeitsverzeichnis
    ]
    
    # Für Debugging
    debug_info = "Suche Konfiguration in folgenden Pfaden:\n"
    for path in search_paths:
        exists = os.path.exists(path)
        debug_info += f" - {path} {'(gefunden)' if exists else '(nicht gefunden)'}\n"
    logging.info(debug_info)
    
    return search_paths

def ensure_user_config_directory():
    """
    Stellt sicher, dass das Benutzer-Konfigurationsverzeichnis existiert.
    Erstellt es, falls es nicht existiert.
    
    Returns:
        str: Pfad zum Benutzer-Konfigurationsverzeichnis
    """
    if sys.platform == "win32":
        user_config_dir = os.path.join(os.environ.get('APPDATA', ''), "PDFExportInstaller", "config")
    elif sys.platform == "darwin":  # macOS
        user_config_dir = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "PDFExportInstaller", "config")
    else:  # Linux und andere
        user_config_dir = os.path.join(os.path.expanduser("~"), ".config", "PDFExportInstaller", "config")
    
    if not os.path.exists(user_config_dir):
        try:
            os.makedirs(user_config_dir, exist_ok=True)
            logging.info(f"Benutzer-Konfigurationsverzeichnis erstellt: {user_config_dir}")
        except Exception as e:
            logging.error(f"Fehler beim Erstellen des Benutzer-Konfigurationsverzeichnisses: {e}")
            return None
    
    return user_config_dir

def copy_default_configs_if_needed():
    """
    Kopiert die Standard-Konfigurationsdateien in das Benutzerverzeichnis,
    falls sie dort noch nicht existieren.
    """
    user_config_dir = ensure_user_config_directory()
    if not user_config_dir:
        return
    
    app_path = get_application_path()
    default_config_path = os.path.join(app_path, "config")
    
    # Überprüfen, ob der Standard-Konfigurationsordner existiert
    if not os.path.exists(default_config_path):
        default_config_path = os.path.join(os.path.dirname(app_path), "config")
        if not os.path.exists(default_config_path):
            logging.warning("Standard-Konfigurationsordner nicht gefunden.")
            return
    
    # Alle JSON-Dateien im Standard-Konfigurationsordner kopieren
    for config_file in glob.glob(os.path.join(default_config_path, "*.json")):
        target_file = os.path.join(user_config_dir, os.path.basename(config_file))
        
        # Nur kopieren, wenn die Datei noch nicht existiert
        if not os.path.exists(target_file):
            try:
                shutil.copy2(config_file, target_file)
                logging.info(f"Konfigurationsdatei in Benutzerverzeichnis kopiert: {target_file}")
            except Exception as e:
                logging.error(f"Fehler beim Kopieren der Konfigurationsdatei: {e}")

def find_resource_path(resource_path):
    """
    Findet den korrekten absoluten Pfad zu einer Ressource, unabhängig davon, 
    ob die Anwendung als Skript oder als ausführbare Datei ausgeführt wird.
    
    Args:
        resource_path (str): Relativer Pfad zur Ressource
        
    Returns:
        str: Korrekter absoluter Pfad zur Ressource
    """
    app_path = get_application_path()
    
    # Verschiedene mögliche Pfade in Prioritätsreihenfolge
    possible_paths = [
        os.path.join(os.path.dirname(app_path), resource_path),  # Neben der EXE
        os.path.join(app_path, resource_path),                   # Im App-Verzeichnis
        os.path.join(os.getcwd(), resource_path)                 # Im aktuellen Arbeitsverzeichnis
    ]
    
    # Den ersten existierenden Pfad zurückgeben
    for path in possible_paths:
        if os.path.exists(path):
            return os.path.normpath(path)
    
    # Wenn keine Datei gefunden wurde, den ersten Pfad zurückgeben (für Fehlermeldungen)
    logging.warning(f"Ressource nicht gefunden: {resource_path}")
    return os.path.normpath(possible_paths[0])

def lade_konfigurationen(datei_pfad):
    """
    Lädt JSON-Konfigurationsdateien von verschiedenen möglichen Pfaden.
    
    Args:
        datei_pfad (str): Der relative oder absolute Pfad zur JSON-Datei.
        
    Returns:
        dict: Die geladenen Konfigurationen oder None bei Fehler.
    """
    # Stelle sicher, dass benutzerspezifische Konfigurationen vorhanden sind
    copy_default_configs_if_needed()
    
    # Extrahiere den Dateinamen aus dem Pfad
    config_filename = os.path.basename(datei_pfad)
    
    # Alle möglichen Pfade für die Konfigurationsdatei ermitteln
    pfade_zu_pruefen = get_config_search_paths(config_filename)
    
    # Durch alle möglichen Pfade iterieren und den ersten verfügbaren verwenden
    for pfad in pfade_zu_pruefen:
        try:
            if os.path.exists(pfad):
                with open(pfad, 'r', encoding='utf-8') as f:
                    konfigurationen = json.load(f)
                logging.info(f"Konfigurationen erfolgreich von {pfad} geladen.")
                return konfigurationen
        except json.JSONDecodeError:
            logging.error(f"Fehler beim Lesen der JSON-Datei: {pfad}")
            continue
        except Exception as e:
            logging.error(f"Unerwarteter Fehler beim Laden der Konfigurationen von {pfad}: {e}")
            continue
    
    # Wenn keine Konfigurationsdatei gefunden wurde
    fehler_nachricht = f"Konfigurationsdatei nicht gefunden: {datei_pfad}\n\nGeprüfte Pfade:\n" + "\n".join(pfade_zu_pruefen)
    messagebox.showerror("Fehler", fehler_nachricht)
    logging.error(f"Konfigurationsdatei nicht gefunden: Geprüfte Pfade: {pfade_zu_pruefen}")
    return None

def ist_adobe_bridge_installiert():
    """
    Prüft, ob Adobe Bridge auf dem System installiert ist.
    Diese Information wird benötigt, um den Benutzer zu warnen, wenn die Farbeinstellungen 
    nicht automatisch über alle Adobe-Programme synchronisiert werden können.
    
    Returns:
        bool: True, wenn Adobe Bridge installiert ist, sonst False
    """
    if sys.platform == "win32":
        # Windows: Prüfe typische Installationspfade
        typische_pfade = [
            os.path.join(os.environ.get('PROGRAMFILES', ''), "Adobe", "Adobe Bridge [0-9]*"),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), "Adobe", "Adobe Bridge [0-9]*"),
            "C:\\Program Files\\Adobe\\Adobe Bridge *",
            "C:\\Program Files (x86)\\Adobe\\Adobe Bridge *"
        ]
        
        for pfad_muster in typische_pfade:
            if glob.glob(pfad_muster):
                return True
        
        # Registry-Prüfung
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Adobe\Bridge") as key:
                return True
        except (ImportError, FileNotFoundError, WindowsError):
            pass
            
    elif sys.platform == "darwin":
        # macOS: Prüfe typische Installationspfade
        typische_pfade = [
            "/Applications/Adobe Bridge*.app",
            f"/Users/{getpass.getuser()}/Applications/Adobe Bridge*.app"
        ]
        
        for pfad_muster in typische_pfade:
            if glob.glob(pfad_muster):
                return True
        
        # Zusätzlich mit mdfind suchen (Spotlight)
        try:
            result = subprocess.run(["mdfind", "kMDItemCFBundleIdentifier == 'com.adobe.bridge*'"], 
                                   capture_output=True, text=True, check=False)
            if result.stdout.strip():
                return True
        except (FileNotFoundError, subprocess.SubprocessError):
            pass
    
    # Wenn keine der obigen Methoden Bridge findet
    return False

def get_system_directories():
    """
    Ermittelt die korrekten Systemverzeichnisse basierend auf dem Betriebssystem.
    
    Returns:
        tuple: (betriebssystem, pdf_settings_zielverzeichnis, color_settings_zielverzeichnis, icc_profile_zielverzeichnis)
    """
    # Benutzername ermitteln
    benutzername = getpass.getuser()
    
    # Konfigurationen laden
    verzeichnisse = lade_konfigurationen("currentDirectories.json")
    
    # Betriebssystem ermitteln
    if sys.platform == "win32":
        betriebssystem = "windows"
    elif sys.platform == "darwin":
        betriebssystem = "mac"
    else:
        logging.error(f"Unbekanntes Betriebssystem: {sys.platform}")
        return None, None, None, None
    
    if verzeichnisse is None:
        return betriebssystem, None, None, None
    
    # Zielverzeichnisse aus der Konfiguration laden und anpassen
    pdf_settings_zielverzeichnis = verzeichnisse[betriebssystem]["adobe_pdf_settings_pfad"].replace("%USERNAME%", benutzername)
    color_settings_zielverzeichnis = verzeichnisse[betriebssystem]["color_settings_pfad"].replace("%USERNAME%", benutzername)
    icc_profile_zielverzeichnis = verzeichnisse[betriebssystem]["icc_profile_pfad"].replace("%USERNAME%", benutzername)
    
    # Backslashes in Pfaden normalisieren für konsistente Handhabung
    pdf_settings_zielverzeichnis = os.path.normpath(pdf_settings_zielverzeichnis)
    color_settings_zielverzeichnis = os.path.normpath(color_settings_zielverzeichnis)
    icc_profile_zielverzeichnis = os.path.normpath(icc_profile_zielverzeichnis)
    
    return betriebssystem, pdf_settings_zielverzeichnis, color_settings_zielverzeichnis, icc_profile_zielverzeichnis