"""
PDF-Export Einstellungen Installer

Dieses Programm installiert vordefinierte PDF-Export-Einstellungen für Adobe-Programme,
einschließlich Farbprofilen, PDF-Einstellungen und Adobe-Farbeinstellungen.
Es unterstützt verschiedene Druckumgebungen wie beschichtetes und unbeschichtetes Papier.

Copyright (c) 2025 sambbaer
"""

# --------------------------------
# Imports und Module
# --------------------------------
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import shutil
import os
import json
import logging
from datetime import datetime
import getpass
import sys
import pathlib
import subprocess
import glob

# Eigene Module (versuche zu importieren, aber lasse die Anwendung trotzdem starten)
try:
    import joboptions_parser
    joboptions_verfuegbar = True
except ImportError:
    joboptions_verfuegbar = False
    logging.warning("Joboptions-Parser konnte nicht importiert werden. Beschreibungen werden nicht angezeigt.")

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

# --------------------------------
# Hilfsfunktionen
# --------------------------------

def lade_konfigurationen(datei_pfad):
    """
    Lädt JSON-Konfigurationsdateien von verschiedenen möglichen Pfaden.
    
    Args:
        datei_pfad (str): Der relative oder absolute Pfad zur JSON-Datei.
        
    Returns:
        dict: Die geladenen Konfigurationen oder None bei Fehler.
    """
    # Prüfe verschiedene mögliche Pfadvarianten
    pfade_zu_pruefen = [
        datei_pfad,  # Original-Pfad wie angegeben
        os.path.join(os.path.dirname(os.path.abspath(__file__)), datei_pfad),  # Relativ zum Skriptverzeichnis
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


# --------------------------------
# Hauptklasse für die GUI-Anwendung
# --------------------------------

class PDFExportEinstellungen(ctk.CTk):
    """
    Hauptklasse für die PDF-Export-Einstellungen-Anwendung.
    Stellt eine benutzerfreundliche GUI zur Verfügung, mit der Benutzer Adobe-Einstellungen
    für verschiedene Druckumgebungen installieren können.
    """
    
    def __init__(self):
        """Initialisiert die Anwendung und erstellt die GUI."""
        super().__init__()
        
        # Fensterkonfiguration
        self.title("PDF-Export Einstellungen Installer")
        self.geometry("700x1000")  # Größere Höhe für alle Elemente
        self.minsize(650, 1000)    # Mindestgröße angepasst
        
        # Fenster auf dem Bildschirm zentrieren
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 700) // 2
        y = (screen_height - 600) // 2
        self.geometry(f"700x600+{x}+{y}")
        
        # Prüfe, ob Adobe Bridge installiert ist
        self.bridge_installiert = ist_adobe_bridge_installiert()
        
        # UI-Elemente erstellen
        self._erstelle_ui()
        
        # Einstellungen laden
        self.lade_einstellungen()
    
    def _erstelle_ui(self):
        """Erstellt alle UI-Elemente der Anwendung mit Fokus auf Benutzerfreundlichkeit für Laien."""
        # Hauptcontainer mit Scrollbar für alle Inhalte
        self.haupt_container = ctk.CTkScrollableFrame(self)
        self.haupt_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ----- KOPFBEREICH -----
        # Titel und Logo-Bereich
        self.logo_label = ctk.CTkLabel(self.haupt_container, text="PDF-Export Einstellungen", 
                                      font=ctk.CTkFont(size=28, weight="bold"))
        self.logo_label.pack(pady=(10, 0))
        
        # Untertitel
        self.subtitle_label = ctk.CTkLabel(self.haupt_container, 
                                         text="Professionelle Druckeinstellungen für Adobe-Programme",
                                         font=ctk.CTkFont(size=16))
        self.subtitle_label.pack(pady=(0, 5))
        
        # ----- ERKLÄRUNGSBEREICH -----
        # Erklärungsrahmen
        self.erklaerung_frame = ctk.CTkFrame(self.haupt_container)
        self.erklaerung_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        self.erklaerung_titel = ctk.CTkLabel(self.erklaerung_frame, 
                                          text="Was macht dieses Programm?",
                                          font=ctk.CTkFont(size=16, weight="bold"))
        self.erklaerung_titel.pack(anchor="w", padx=15, pady=(10, 5))
        
        erklaerung_text = (
            "Dieses Programm installiert vordefinierte Einstellungen für Adobe-Programme wie InDesign, "
            "Photoshop und Illustrator. Diese Einstellungen sind speziell auf professionelle "
            "Druckanforderungen abgestimmt und sorgen für beste Druckergebnisse.\n\n"
            "Mit einem Klick werden alle nötigen Dateien an den richtigen Stellen auf Ihrem System installiert."
        )
        
        self.erklaerung_label = ctk.CTkLabel(self.erklaerung_frame, 
                                          text=erklaerung_text,
                                          font=ctk.CTkFont(size=14),
                                          justify="left",
                                          wraplength=640)
        self.erklaerung_label.pack(anchor="w", padx=15, pady=(0, 15))
        
        # ----- AUSWAHL-BEREICH -----
        # Hauptframe für die Einstellungen
        self.main_frame = ctk.CTkFrame(self.haupt_container)
        self.main_frame.pack(fill="x", padx=10, pady=10)
        
        # Erklärung für die Listbox
        self.info_label = ctk.CTkLabel(self.main_frame, 
                                      text="Bitte wählen Sie die gewünschten Einstellungen:",
                                      font=ctk.CTkFont(size=16, weight="bold"),
                                      anchor="w")
        self.info_label.pack(padx=15, pady=(15, 5), anchor="w")
        
        # Hilfetext für die Mehrfachauswahl
        self.help_label = ctk.CTkLabel(self.main_frame, 
                                     text="• Mit Strg-Taste (Windows) oder Cmd-Taste (Mac) können Sie mehrere Einträge auswählen\n"
                                     "• Mit der Shift-Taste können Sie einen Bereich auswählen",
                                     text_color="gray60",
                                     font=ctk.CTkFont(size=13),
                                     justify="left",
                                     anchor="w")
        self.help_label.pack(padx=15, pady=(0, 10), anchor="w")
        
        # Frame für die Listbox
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.pack(padx=15, pady=5, fill="both")
        
        # Einstellungen Listbox (Standard-Tkinter, da CTk keine Listbox hat)
        self.einstellungs_liste = tk.Listbox(self.list_frame, height=12, selectmode=tk.MULTIPLE,
                                          font=("Segoe UI", 13), 
                                          activestyle="none",
                                          bg="#F9F9F9", fg="#333333",
                                          selectbackground="#3B8ED0", selectforeground="white")
        self.einstellungs_liste.pack(padx=5, pady=5, fill="both", expand=False)
        
        # Scrollbar für die Listbox
        self.scrollbar = ctk.CTkScrollbar(self.list_frame, command=self.einstellungs_liste.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.einstellungs_liste.config(yscrollcommand=self.scrollbar.set)
        
        # Button-Frame für Auswahloperationen
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(padx=15, pady=(10, 15), fill="x")
        
        # Button-Grid konfigurieren
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        
        # Buttons für Auswahl
        self.alle_button = ctk.CTkButton(self.button_frame, text="Alle auswählen", 
                                       command=self.alle_auswaehlen,
                                       width=200,
                                       font=ctk.CTkFont(size=14))
        self.alle_button.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.keine_button = ctk.CTkButton(self.button_frame, text="Auswahl aufheben", 
                                        command=self.keine_auswaehlen,
                                        fg_color="gray70", hover_color="gray50",
                                        width=200,
                                        font=ctk.CTkFont(size=14))
        self.keine_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # ----- BESCHREIBUNG DER EINSTELLUNGEN -----
        self.beschreibung_frame = ctk.CTkFrame(self.haupt_container)
        self.beschreibung_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        self.beschreibung_titel = ctk.CTkLabel(self.beschreibung_frame, 
                                             text="Welche Einstellungen werden installiert?",
                                             font=ctk.CTkFont(size=16, weight="bold"))
        self.beschreibung_titel.pack(anchor="w", padx=15, pady=(10, 5))
        
        beschreibung_text = (
            "Bei der Installation werden folgende Dateien installiert:\n\n"
            "• Adobe PDF-Exporteinstellungen (.joboptions)\n"
            "• Farbeinstellungen für Adobe-Programme (.csf)\n"
            "• ICC-Farbprofile für professionellen Druck (.icc)\n\n"
            "Diese Einstellungen werden an den richtigen Stellen Ihres Systems platziert, "
            "damit alle Adobe-Programme darauf zugreifen können."
        )
        
        self.beschreibung_label = ctk.CTkLabel(self.beschreibung_frame, 
                                             text=beschreibung_text,
                                             font=ctk.CTkFont(size=14),
                                             justify="left",
                                             wraplength=640)
        self.beschreibung_label.pack(anchor="w", padx=15, pady=(0, 15))
        
        # ----- INSTALLATIONSBEREICH -----
        # Info und Installationsbutton
        self.install_frame = ctk.CTkFrame(self.haupt_container)
        self.install_frame.pack(fill="x", padx=10, pady=(10, 20))
        
        self.install_label = ctk.CTkLabel(self.install_frame, 
                                       text="Klicken Sie auf den Button, um die ausgewählten Einstellungen zu installieren:",
                                       font=ctk.CTkFont(size=14),
                                       anchor="w")
        self.install_label.pack(padx=15, pady=(15, 10), anchor="w")
        
        # Installieren-Button
        self.install_button = ctk.CTkButton(self.install_frame, 
                                          text="Ausgewählte Einstellungen installieren", 
                                          command=self.installiere_einstellungen,
                                          font=ctk.CTkFont(size=16, weight="bold"),
                                          height=50,
                                          fg_color="#2B7D2B", hover_color="#246A24")
        self.install_button.pack(padx=15, pady=(0, 15), fill="x")
        
        # ----- STATUSBEREICH -----
        # Statusanzeige am unteren Rand
        self.status_frame = ctk.CTkFrame(self.haupt_container)
        self.status_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="Bereit", anchor="w")
        self.status_label.pack(padx=15, pady=10, anchor="w")
    
    def lade_einstellungen(self):
        """
        Lädt die verfügbaren Einstellungen aus der Konfigurationsdatei
        und füllt die Listbox mit den Einstellungsnamen.
        """
        self.einstellungen_daten = lade_konfigurationen("config/settings.json")
        if self.einstellungen_daten is None:
            # Wenn das Laden der Konfiguration fehlschlägt, wird das Programm beendet.
            messagebox.showerror("Kritischer Fehler", "Die Konfigurationsdateien konnten nicht geladen werden. Das Programm wird beendet.")
            self.destroy()
            exit()
            
        # Cache für beschreibungen initialisieren, aber nicht sofort laden
        self.beschreibungen = {}
        
        # Füge die Namen der Einstellungen hinzu.
        for einstellung in self.einstellungen_daten:
            self.einstellungs_liste.insert(tk.END, einstellung["Name"])
        
        # Auswahlhandler für Beschreibungsanzeige
        self.einstellungs_liste.bind('<<ListboxSelect>>', self.zeige_beschreibung)
            
        # Status aktualisieren
        self.status_label.configure(text=f"{len(self.einstellungen_daten)} Einstellungen verfügbar")
        
        # Bridge-Hinweis anzeigen, falls nicht installiert
        if not self.bridge_installiert:
            self.bridge_hinweis_frame = ctk.CTkFrame(self.haupt_container, fg_color="#FFF3CD", corner_radius=6)
            self.bridge_hinweis_frame.pack(fill="x", padx=10, pady=(10, 20))
            
            self.bridge_hinweis_icon = ctk.CTkLabel(self.bridge_hinweis_frame, 
                                                 text="⚠️", 
                                                 font=ctk.CTkFont(size=20),
                                                 text_color="#856404")
            self.bridge_hinweis_icon.pack(side="left", padx=(15, 5), pady=15)
            
            bridge_hinweis_text = (
                "Adobe Bridge ist nicht installiert. Was bedeutet das?\n\n"
                "Adobe Bridge ist ein Programm, das hilft, Einstellungen zwischen Adobe-Programmen zu "
                "synchronisieren. Ohne Bridge müssen Sie in jedem Adobe-Programm (wie InDesign, Photoshop, "
                "Illustrator) einmalig die Farbeinstellungen unter 'Bearbeiten > Farbeinstellungen' auswählen."
            )
            
            self.bridge_hinweis_text = ctk.CTkLabel(self.bridge_hinweis_frame, 
                                                 text=bridge_hinweis_text,
                                                 text_color="#856404",
                                                 font=ctk.CTkFont(size=13),
                                                 justify="left",
                                                 wraplength=640)
            self.bridge_hinweis_text.pack(side="left", padx=(0, 15), pady=15, fill="x")
    
    def alle_auswaehlen(self):
        """Wählt alle Einstellungen in der Listbox aus."""
        self.einstellungs_liste.select_set(0, tk.END)
    
    def keine_auswaehlen(self):
        """Hebt alle Auswahlen in der Listbox auf."""
        self.einstellungs_liste.selection_clear(0, tk.END)
        
    def zeige_beschreibung(self, event):
        """
        Zeigt die Beschreibung der ausgewählten Einstellung(en) an.
        Wird aufgerufen, wenn sich die Auswahl in der Listbox ändert.
        Die Beschreibung wird erst geladen, wenn sie benötigt wird.
        """
        # Ausgewählte Einträge abrufen
        selection = self.einstellungs_liste.curselection()
        if not selection:
            # Keine Auswahl - Standardtext anzeigen
            self.beschreibung_label.configure(
                text="Bitte wählen Sie eine Einstellung aus der Liste, um deren Beschreibung zu sehen."
            )
            return
        
        # Erste ausgewählte Einstellung für die Beschreibung verwenden
        selected_index = selection[0]
        selected_name = self.einstellungs_liste.get(selected_index)
        
        # Prüfen, ob die Beschreibung bereits im Cache ist
        if selected_name not in self.beschreibungen:
            # Beschreibung noch nicht geladen, jetzt laden
            self._lade_beschreibung(selected_name, selected_index)
        
        # Beschreibung aus dem Cache abrufen
        beschreibung = self.beschreibungen.get(selected_name, f"Keine Beschreibung für '{selected_name}' verfügbar.")
        
        # Anzahl der ausgewählten Einstellungen anzeigen
        if len(selection) > 1:
            anzahl_text = f"Sie haben {len(selection)} Einstellungen ausgewählt. "
            anzahl_text += f"Hier sehen Sie die Beschreibung für '{selected_name}':"
            self.beschreibung_untertitel.configure(text=anzahl_text)
        else:
            self.beschreibung_untertitel.configure(text=f"Detaillierte Beschreibung von '{selected_name}':")
        
        # Beschreibung anzeigen
        self.beschreibung_label.configure(text=beschreibung)
    
    def _lade_beschreibung(self, name, index):
        """
        Lädt die Beschreibung für eine bestimmte Einstellung und speichert sie im Cache.
        
        Args:
            name (str): Name der Einstellung
            index (int): Index der Einstellung in der Liste
        """
        # Standardbeschreibung für den Fall, dass keine geladen werden kann
        standard_beschreibung = (
            f"Die Einstellung '{name}' enthält vordefinierte Werte für den professionellen Druck. "
            f"Sie wurden speziell für optimale Druckergebnisse konfiguriert."
        )
        
        try:
            # Wenn der Joboptions-Parser nicht verfügbar ist, verwende die Standardbeschreibung
            if not joboptions_verfuegbar:
                self.beschreibungen[name] = standard_beschreibung
                return
            
            # Zugehörige Einstellung finden
            einstellung = self.einstellungen_daten[index]
            
            # Prüfen, ob PDF-Einstellungen vorhanden sind
            if "Adobe PDF Settings" in einstellung and einstellung["Adobe PDF Settings"]:
                joboptions_pfad = os.path.join("resources", einstellung["Adobe PDF Settings"])
                
                # Statusmeldung aktualisieren
                self.status_label.configure(text=f"Lade Beschreibung für {name}...")
                self.update_idletasks()  # GUI aktualisieren
                
                # Beschreibung extrahieren
                beschreibung = joboptions_parser.get_readable_description(joboptions_pfad)
                
                if beschreibung:
                    self.beschreibungen[name] = beschreibung
                else:
                    self.beschreibungen[name] = standard_beschreibung
            else:
                self.beschreibungen[name] = f"Diese Einstellung enthält keine PDF-Exporteinstellungen."
                
            # Status zurücksetzen
            self.status_label.configure(text="Bereit")
            
        except Exception as e:
            # Bei Fehlern Standard-Beschreibung verwenden und Fehler loggen
            logging.error(f"Fehler beim Laden der Beschreibung für {name}: {e}")
            self.beschreibungen[name] = standard_beschreibung
    
    def installiere_einstellungen(self):
        """
        Hauptfunktion zur Installation der ausgewählten Einstellungen.
        
        Diese Funktion:
        1. Prüft, ob Einstellungen ausgewählt wurden
        2. Bereitet die Zielverzeichnisse vor
        3. Kopiert die ausgewählten Dateien an die richtigen Orte
        4. Zeigt eine Zusammenfassung der Installation an
        """
        # Button deaktivieren während der Installation
        self.install_button.configure(state="disabled", text="Installation läuft...")
        self.alle_button.configure(state="disabled")
        self.keine_button.configure(state="disabled")
        
        # GUI aktualisieren, damit die Änderungen sofort sichtbar sind
        self.update_idletasks()
        
        # Überprüfen, ob Einstellungen ausgewählt wurden
        ausgewaehlte_indices = self.einstellungs_liste.curselection()
        if not ausgewaehlte_indices:
            messagebox.showwarning("Hinweis", "Bitte wählen Sie mindestens eine Einstellung aus.")
            # Buttons wieder aktivieren
            self.install_button.configure(state="normal", text="Ausgewählte Einstellungen installieren")
            self.alle_button.configure(state="normal")
            self.keine_button.configure(state="normal")
            return
        
        # Status aktualisieren
        self.status_label.configure(text="Installation läuft...")
        self.update_idletasks()  # GUI aktualisieren
        
        # Lade die notwendigen Konfigurationen
        einstellungen = self.einstellungen_daten
        verzeichnisse = lade_konfigurationen("config/currentDirectories.json")

        if einstellungen is None or verzeichnisse is None:
            self.status_label.configure(text="Fehler beim Laden der Konfigurationen")
            self.install_button.configure(state="normal", text="Ausgewählte Einstellungen installieren")
            self.alle_button.configure(state="normal")
            self.keine_button.configure(state="normal")
            return
        
        # Ermittle Betriebssystem und Standardverzeichnisse
        # Benutzername ermitteln
        benutzername = getpass.getuser()

        # Betriebssystem ermitteln und entsprechende Verzeichnisse wählen
        if sys.platform == "win32":
            betriebssystem = "windows"
        elif sys.platform == "darwin":
            betriebssystem = "mac"
        else:
            messagebox.showerror("Fehler", "Unbekanntes Betriebssystem. Installation abgebrochen.")
            logging.error(f"Unbekanntes Betriebssystem: {sys.platform}")
            self.status_label.configure(text="Installation fehlgeschlagen")
            self.install_button.configure(state="normal", text="Ausgewählte Einstellungen installieren")
            self.alle_button.configure(state="normal")
            self.keine_button.configure(state="normal")
            return
        
        # Zielverzeichnisse aus der Konfiguration laden und anpassen
        pdf_settings_zielverzeichnis = verzeichnisse[betriebssystem]["adobe_pdf_settings_pfad"].replace("%USERNAME%", benutzername)
        color_settings_zielverzeichnis = verzeichnisse[betriebssystem]["color_settings_pfad"].replace("%USERNAME%", benutzername)
        icc_profile_zielverzeichnis = verzeichnisse[betriebssystem]["icc_profile_pfad"].replace("%USERNAME%", benutzername)
        
        # Backslashes in Pfaden normalisieren für konsistente Handhabung
        pdf_settings_zielverzeichnis = os.path.normpath(pdf_settings_zielverzeichnis)
        color_settings_zielverzeichnis = os.path.normpath(color_settings_zielverzeichnis)
        icc_profile_zielverzeichnis = os.path.normpath(icc_profile_zielverzeichnis)

        # Prüfen, ob die Zielverzeichnisse existieren, und ggf. erstellen
        for ziel_verzeichnis in [pdf_settings_zielverzeichnis, color_settings_zielverzeichnis, icc_profile_zielverzeichnis]:
            if ziel_verzeichnis and not os.path.exists(ziel_verzeichnis):
                try:
                    os.makedirs(ziel_verzeichnis)
                    logging.info(f"Verzeichnis erstellt: {ziel_verzeichnis}")
                except Exception as e:
                    messagebox.showerror("Fehler", f"Verzeichnis konnte nicht erstellt werden: {ziel_verzeichnis} - {e}")
                    logging.error(f"Verzeichnis konnte nicht erstellt werden: {ziel_verzeichnis} - {e}")
                    self.status_label.configure(text="Installation fehlgeschlagen")
                    self.install_button.configure(state="normal", text="Ausgewählte Einstellungen installieren")
                    self.alle_button.configure(state="normal")
                    self.keine_button.configure(state="normal")
                    return
        
        # Listen für erfolgreiche und fehlgeschlagene Installationen
        erfolgreiche_installationen = []
        fehlgeschlagene_installationen = []
        
        # Für alle ausgewählten Einstellungen
        for index in ausgewaehlte_indices:
            ausgewaehlte_einstellung = self.einstellungs_liste.get(index)
            einstellung_gefunden = False
            
            # Status aktualisieren
            self.status_label.configure(text=f"Installiere {ausgewaehlte_einstellung}...")
            self.update_idletasks()  # GUI aktualisieren
            
            for einstellung in einstellungen:
                if einstellung["Name"] == ausgewaehlte_einstellung:
                    einstellung_gefunden = True
                    adobe_pdf_setting_name = einstellung["Adobe PDF Settings"]
                    color_setting_name = einstellung["Color Setting"]
                    icc_profil_name = einstellung["ICC-Profil"]

                    # Kopieroperationen mit Fehlerbehandlung und Logging
                    try:
                        # Kopiere nur, wenn der Dateiname nicht leer ist
                        if adobe_pdf_setting_name:
                            quelle_pdf_setting = os.path.join("resources", adobe_pdf_setting_name)
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
                        
                        erfolgreiche_installationen.append(ausgewaehlte_einstellung)
                        logging.info(f"Einstellungen für '{ausgewaehlte_einstellung}' installiert.")
                        
                    except FileNotFoundError as e:
                        fehlgeschlagene_installationen.append(f"{ausgewaehlte_einstellung} (Datei nicht gefunden: {e.filename})")
                        logging.error(f"Datei nicht gefunden für '{ausgewaehlte_einstellung}': {e}")
                    except shutil.Error as e:
                        fehlgeschlagene_installationen.append(f"{ausgewaehlte_einstellung} (Kopierfehler)")
                        logging.error(f"Kopierfehler für '{ausgewaehlte_einstellung}': {e}")
                    except Exception as e:
                        fehlgeschlagene_installationen.append(f"{ausgewaehlte_einstellung} (Unerwarteter Fehler)")
                        logging.error(f"Unerwarteter Fehler für '{ausgewaehlte_einstellung}': {e}")
                    
                    break  # Diese Einstellung wurde verarbeitet
            
            if not einstellung_gefunden:
                fehlgeschlagene_installationen.append(f"{ausgewaehlte_einstellung} (Einstellung nicht gefunden)")
                logging.error(f"Einstellung '{ausgewaehlte_einstellung}' nicht gefunden.")
        
        # Zeige ein Zusammenfassungsfenster an
        nachricht = ""
        if erfolgreiche_installationen:
            nachricht += "Erfolgreich installierte Einstellungen:\n"
            nachricht += "\n".join([f"✓ {name}" for name in erfolgreiche_installationen])
        
        if fehlgeschlagene_installationen:
            if erfolgreiche_installationen:
                nachricht += "\n\n"
            nachricht += "Fehlgeschlagene Installationen:\n"
            nachricht += "\n".join([f"✗ {name}" for name in fehlgeschlagene_installationen])
        
        # Status aktualisieren
        if erfolgreiche_installationen and not fehlgeschlagene_installationen:
            self.status_label.configure(text="Installation erfolgreich abgeschlossen")
            messagebox.showinfo("Installation abgeschlossen", nachricht)
        elif fehlgeschlagene_installationen and not erfolgreiche_installationen:
            self.status_label.configure(text="Installation fehlgeschlagen")
            messagebox.showerror("Installation fehlgeschlagen", nachricht)
        else:
            self.status_label.configure(text="Installation teilweise erfolgreich")
            messagebox.showwarning("Installation teilweise erfolgreich", nachricht)
            
        # Buttons wieder aktivieren
        self.install_button.configure(state="normal", text="Ausgewählte Einstellungen installieren")
        self.alle_button.configure(state="normal")
        self.keine_button.configure(state="normal")


# --------------------------------
# Programm starten
# --------------------------------

if __name__ == "__main__":
    app = PDFExportEinstellungen()
    app.mainloop()