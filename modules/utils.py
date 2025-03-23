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

def find_resource_path(resource_path):
    """
    Findet den korrekten absoluten Pfad zu einer Ressource, unabhängig davon, 
    ob die Anwendung als Skript oder als ausführbare Datei ausgeführt wird.
    
    Args:
        resource_path (str): Relativer Pfad zur Ressource
        
    Returns:
        str: Korrekter absoluter Pfad zur Ressource
    """
    # Ermittle das Basis-Verzeichnis des Programms
    if getattr(sys, 'frozen', False):
        # Ausführbare Datei (z.B. PyInstaller)
        base_path = os.path.dirname(sys.executable)
    else:
        # Normales Python-Skript
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.normpath(os.path.join(base_path, resource_path))

def lade_konfigurationen(datei_pfad):
    """
    Lädt JSON-Konfigurationsdateien von verschiedenen möglichen Pfaden.
    
    Args:
        datei_pfad (str): Der relative oder absolute Pfad zur JSON-Datei.
        
    Returns:
        dict: Die geladenen Konfigurationen oder None bei Fehler.
    """
    # Überprüfe zuerst den für ausführbare Dateien korrigierten Pfad
    korrigierter_pfad = find_resource_path(datei_pfad)
    
    # Prüfe verschiedene mögliche Pfadvarianten
    pfade_zu_pruefen = [
        korrigierter_pfad,  # Korrigierter Pfad für ausführbare Dateien
        datei_pfad,  # Original-Pfad wie angegeben
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), datei_pfad),  # Relativ zum Überverzeichnis des Moduls
        os.path.join(os.path.abspath('.'), datei_pfad),  # Relativ zum aktuellen Arbeitsverzeichnis
    ]
    
    for pfad in pfade_zu_pruefen:
        try:
            with open(pfad, 'r', encoding='utf-8') as f:
                konfigurationen = json.load(f)
            logging.info(f"Konfigurationen erfolgreich von {pfad} geladen.")
            return konfigurationen
        except FileNotFoundError:
            continue  # Versuche den nächsten Pfad
        except json.JSONDecodeError:
            messagebox.showerror("Fehler", f"Fehler beim Lesen der JSON-Datei: {pfad}")
            logging.error(f"Fehler beim Lesen der JSON-Datei: {pfad}")
            return None
        except Exception as e:
            messagebox.showerror("Fehler", f"Unerwarteter Fehler beim Laden der Konfigurationen: {e}")
            logging.error(f"Unerwarteter Fehler beim Laden der Konfigurationen: {e}")
            return None
    
    # Wenn alle Pfade fehlschlagen, zeige eine Fehlermeldung mit allen versuchten Pfaden
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
    verzeichnisse = lade_konfigurationen("config/currentDirectories.json")
    
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