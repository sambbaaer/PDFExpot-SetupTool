"""
Installer-Modul für PDF-Export-Einstellungen

Dieses Modul enthält die Logik zur Installation der PDF-Export-Einstellungen
für Adobe-Programme.
"""

import os
import shutil
import logging
from tkinter import messagebox
from .utils import find_resource_path, lade_konfigurationen, get_system_directories

class EinstellungsInstaller:
    """
    Klasse zur Installation von PDF-Export-Einstellungen für Adobe-Programme.
    """
    
    def __init__(self, status_callback=None):
        """
        Initialisiert den Installer.
        
        Args:
            status_callback (callable, optional): Funktion zum Aktualisieren des Status in der GUI.
        """
        self.status_callback = status_callback
        self.einstellungen = lade_konfigurationen("config/settings.json")
    
    def update_status(self, message):
        """
        Aktualisiert den Status in der GUI, wenn ein Callback definiert ist.
        
        Args:
            message (str): Statusmeldung
        """
        if self.status_callback:
            self.status_callback(message)
    
    def create_directories(self, directories):
        """
        Erstellt die erforderlichen Verzeichnisse, falls sie nicht existieren.
        
        Args:
            directories (list): Liste der zu erstellenden Verzeichnisse
            
        Returns:
            bool: True, wenn alle Verzeichnisse erstellt wurden oder bereits existieren, sonst False
        """
        for directory in directories:
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                    logging.info(f"Verzeichnis erstellt: {directory}")
                except Exception as e:
                    messagebox.showerror("Fehler", f"Verzeichnis konnte nicht erstellt werden: {directory}\n\nFehler: {e}")
                    logging.error(f"Verzeichnis konnte nicht erstellt werden: {directory} - {e}")
                    return False
        return True
    
    def install_settings(self, selected_settings):
        """
        Installiert die ausgewählten Einstellungen.
        
        Args:
            selected_settings (list): Liste der Namen der zu installierenden Einstellungen
            
        Returns:
            tuple: (erfolgreiche_installationen, fehlgeschlagene_installationen, installations_details)
        """
        # Konfigurationen und Zielverzeichnisse ermitteln
        os_type, pdf_dir, color_dir, icc_dir = get_system_directories()
        
        if not all([pdf_dir, color_dir, icc_dir]):
            messagebox.showerror("Fehler", "Die Zielverzeichnisse konnten nicht ermittelt werden.")
            return [], ["Konnte Zielverzeichnisse nicht ermitteln"], {}
        
        # Verzeichnisse erstellen, falls sie nicht existieren
        if not self.create_directories([pdf_dir, color_dir, icc_dir]):
            return [], ["Konnte erforderliche Verzeichnisse nicht erstellen"], {}
        
        # Erfolgreiche und fehlgeschlagene Installationen
        erfolgreiche_installationen = []
        fehlgeschlagene_installationen = []
        # Details zu kopierten Dateien (key: Einstellungsname, value: Liste der kopierten Dateien)
        installations_details = {}
        
        # Einstellungen installieren
        for setting_name in selected_settings:
            self.update_status(f"Installiere {setting_name}...")
            
            # Einstellung in den Daten finden
            setting_found = False
            
            for setting in self.einstellungen:
                if setting["Name"] == setting_name:
                    setting_found = True
                    
                    # Dateipfade ermitteln
                    pdf_setting = setting.get("Adobe PDF Settings", "")
                    color_setting = setting.get("Color Setting", "")
                    icc_profile = setting.get("ICC-Profil", "")
                    
                    # Dateien kopieren
                    try:
                        # Liste der kopierten Dateien für diese Einstellung
                        copied_files = []
                        
                        if pdf_setting:
                            source_pdf = find_resource_path(os.path.join("resources", pdf_setting))
                            target_pdf = os.path.join(pdf_dir, pdf_setting)
                            self._copy_file(source_pdf, target_pdf)
                            copied_files.append({
                                "type": "PDF-Einstellung",
                                "file": pdf_setting,
                                "destination": target_pdf
                            })
                        
                        if color_setting:
                            source_color = find_resource_path(os.path.join("resources", color_setting))
                            target_color = os.path.join(color_dir, color_setting)
                            self._copy_file(source_color, target_color)
                            copied_files.append({
                                "type": "Farbeinstellung",
                                "file": color_setting,
                                "destination": target_color
                            })
                        
                        if icc_profile:
                            source_icc = find_resource_path(os.path.join("resources", icc_profile))
                            target_icc = os.path.join(icc_dir, icc_profile)
                            self._copy_file(source_icc, target_icc)
                            copied_files.append({
                                "type": "ICC-Profil",
                                "file": icc_profile,
                                "destination": target_icc
                            })
                        
                        erfolgreiche_installationen.append(setting_name)
                        installations_details[setting_name] = copied_files
                        logging.info(f"Einstellungen für '{setting_name}' installiert.")
                        
                    except FileNotFoundError as e:
                        fehlgeschlagene_installationen.append(f"{setting_name} (Datei nicht gefunden: {e.filename})")
                        logging.error(f"Datei nicht gefunden für '{setting_name}': {e}")
                    except shutil.Error as e:
                        fehlgeschlagene_installationen.append(f"{setting_name} (Kopierfehler)")
                        logging.error(f"Kopierfehler für '{setting_name}': {e}")
                    except Exception as e:
                        fehlgeschlagene_installationen.append(f"{setting_name} (Unerwarteter Fehler)")
                        logging.error(f"Unerwarteter Fehler für '{setting_name}': {e}")
                    
                    break  # Diese Einstellung wurde verarbeitet
            
            if not setting_found:
                fehlgeschlagene_installationen.append(f"{setting_name} (Einstellung nicht gefunden)")
                logging.error(f"Einstellung '{setting_name}' nicht gefunden.")
        
        return erfolgreiche_installationen, fehlgeschlagene_installationen, installations_details
    
    def _copy_file(self, source, destination):
        """
        Kopiert eine Datei von der Quelle zum Ziel.
        
        Args:
            source (str): Pfad zur Quelldatei
            destination (str): Pfad zur Zieldatei
            
        Raises:
            FileNotFoundError: Wenn die Quelldatei nicht gefunden wird
            shutil.Error: Wenn ein Fehler beim Kopieren auftritt
        """
        if not os.path.exists(source):
            raise FileNotFoundError(source)
        
        # Verzeichnis erstellen, falls es nicht existiert
        destination_dir = os.path.dirname(destination)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        # Datei kopieren
        shutil.copy2(source, destination)
        logging.info(f"Datei kopiert: {source} nach {destination}")