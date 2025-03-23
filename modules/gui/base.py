"""
Basis-GUI-Modul für PDF-Export-Einstellungen-Installer

Dieses Modul enthält die Hauptklasse für die GUI-Anwendung.
"""

import tkinter as tk
import customtkinter as ctk
import logging
import threading
import sys
from tkinter import messagebox

from ..utils import ist_adobe_bridge_installiert, lade_konfigurationen
from ..installer import EinstellungsInstaller
from .left_panel import LeftPanel
from .right_panel import RightPanel


class PDFExportEinstellungenGUI(ctk.CTk):
    """
    Hauptklasse für die PDF-Export-Einstellungen-Anwendung GUI.
    Optimiert für zweispaltiges Layout ohne Scrolling.
    """
    
    def __init__(self):
        """Initialisiert die Anwendung und erstellt die GUI."""
        super().__init__()
        
        # Fensterkonfiguration
        self.title("PDF-Export Einstellungen Installer")
        self.minsize(1000, 650)    # Mindestgröße festlegen
        
        # Fenster im Vollbild öffnen - betriebssystemübergreifend
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Betriebssystemspezifische Vollbildanpassungen
        if sys.platform == "win32":
            self.state("zoomed")  # Windows-spezifisch
        elif sys.platform == "darwin":
            self.attributes("-zoomed", 1)  # macOS-spezifisch
        else:
            # Für Linux und andere Systeme
            self.attributes("-fullscreen", True)
            # Escape-Taste zum Beenden des Vollbildmodus ermöglichen
            self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
        
        # Installer initialisieren
        self.installer = EinstellungsInstaller(self.update_status)
        
        # Beschreibungen-Cache initialisieren
        self.beschreibungen = {}
        
        # Prüfe, ob Adobe Bridge installiert ist
        self.bridge_installiert = ist_adobe_bridge_installiert()
        
        # UI-Elemente erstellen
        self._erstelle_ui()
        
        # Einstellungen laden
        self.lade_einstellungen()
    
    def _erstelle_ui(self):
        """Erstellt alle UI-Elemente der Anwendung im zweispaltigen Layout."""
        # Hauptcontainer für alle Inhalte (ohne Scrollbar)
        self.haupt_container = ctk.CTkFrame(self, fg_color="transparent")
        self.haupt_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Konfiguration des Grid-Layouts
        self.haupt_container.grid_columnconfigure(0, weight=1)  # Linke Spalte
        self.haupt_container.grid_columnconfigure(1, weight=1)  # Rechte Spalte
        
        # ----- KOPFBEREICH (über beiden Spalten) -----
        self._erstelle_kopfbereich()
        
        # ----- LINKE SPALTE -----
        self.left_panel = LeftPanel(self.haupt_container, self)
        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # ----- RECHTE SPALTE -----
        self.right_panel = RightPanel(self.haupt_container, self)
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        
        # ----- STATUSBEREICH (unter beiden Spalten) -----
        self._erstelle_statusbereich()
    
    def _erstelle_kopfbereich(self):
        """Erstellt den Kopfbereich der Anwendung."""
        # Header-Frame
        self.header_frame = ctk.CTkFrame(self.haupt_container, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # Titel und Logo-Bereich
        self.logo_label = ctk.CTkLabel(self.header_frame, text="PDF-Export Einstellungen", 
                                      font=ctk.CTkFont(size=28, weight="bold"))
        self.logo_label.pack(pady=(0, 5))
        
        # Untertitel
        self.subtitle_label = ctk.CTkLabel(self.header_frame, 
                                         text="Professionelle Druckeinstellungen für Adobe-Programme",
                                         font=ctk.CTkFont(size=16))
        self.subtitle_label.pack(pady=(0, 5))
    
    def _erstelle_statusbereich(self):
        """Erstellt den Statusbereich am unteren Rand."""
        # Statusanzeige am unteren Rand
        self.status_frame = ctk.CTkFrame(self.haupt_container)
        self.status_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(15, 0))
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="Bereit", anchor="w")
        self.status_label.pack(padx=15, pady=10, anchor="w", side="left")
    
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
        
        # Einstellungen an die linke Panel übergeben
        self.left_panel.lade_einstellungen(self.einstellungen_daten)
        
        # Status aktualisieren
        self.status_label.configure(text=f"{len(self.einstellungen_daten)} Einstellungen verfügbar")
        
        # Bridge-Hinweis anzeigen, falls nicht installiert
        if not self.bridge_installiert:
            self._zeige_bridge_hinweis()
    
    def _zeige_bridge_hinweis(self):
        """Zeigt den Hinweis an, wenn Adobe Bridge nicht installiert ist."""
        self.bridge_hinweis_frame = ctk.CTkFrame(self.haupt_container, fg_color="#FFF3CD", corner_radius=6)
        self.bridge_hinweis_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(15, 0))
        
        bridge_hinweis_text = (
            "⚠️ Adobe Bridge ist nicht installiert: Ohne Bridge müssen Sie in jedem Adobe-Programm die "
            "Farbeinstellungen unter 'Bearbeiten > Farbeinstellungen' manuell auswählen."
        )
        
        self.bridge_hinweis_text = ctk.CTkLabel(self.bridge_hinweis_frame, 
                                             text=bridge_hinweis_text,
                                             text_color="#856404",
                                             font=ctk.CTkFont(size=13),
                                             wraplength=960)
        self.bridge_hinweis_text.pack(padx=15, pady=10)
    
    def update_status(self, message):
        """
        Aktualisiert die Statusanzeige.
        
        Args:
            message (str): Die anzuzeigende Nachricht
        """
        self.status_label.configure(text=message)
        self.update_idletasks()  # GUI aktualisieren
    
    def installiere_einstellungen(self, ausgewaehlte_einstellungen):
        """
        Hauptfunktion zur Installation der ausgewählten Einstellungen.
        
        Args:
            ausgewaehlte_einstellungen (list): Namen der zu installierenden Einstellungen
        """
        # Buttons über das Left Panel deaktivieren
        self.left_panel.set_buttons_state("disabled")
        
        # Status aktualisieren
        self.update_status("Installation wird vorbereitet...")
        
        # Installation in einem separaten Thread ausführen, um die GUI reaktiv zu halten
        threading.Thread(target=self._installiere_im_hintergrund, 
                       args=(ausgewaehlte_einstellungen,), 
                       daemon=True).start()
    
    def _installiere_im_hintergrund(self, ausgewaehlte_einstellungen):
        """
        Führt die Installation im Hintergrund aus.
        
        Args:
            ausgewaehlte_einstellungen (list): Namen der zu installierenden Einstellungen
        """
        # Installation durchführen
        erfolgreiche_installationen, fehlgeschlagene_installationen, installations_details = self.installer.install_settings(ausgewaehlte_einstellungen)
        
        # GUI-Updates müssen im Hauptthread erfolgen
        self.after(0, lambda: self._zeige_installation_ergebnis(
            erfolgreiche_installationen, 
            fehlgeschlagene_installationen,
            installations_details
        ))
    
    def _zeige_installation_ergebnis(self, erfolgreiche_installationen, fehlgeschlagene_installationen, installations_details):
        """
        Zeigt das Ergebnis der Installation an und aktiviert die Buttons wieder.
        
        Args:
            erfolgreiche_installationen (list): Liste der erfolgreich installierten Einstellungen
            fehlgeschlagene_installationen (list): Liste der fehlgeschlagenen Installationen
            installations_details (dict): Details zu den kopierten Dateien
        """
        from .dialogs import zeige_ergebnis_dialog
        
        # Detaillierte Installationsbericht erstellen
        detaillierter_bericht = self._erstelle_detaillierten_bericht(erfolgreiche_installationen, installations_details)
        
        # Nachricht für die Messagebox zusammenstellen
        nachricht = ""
        if erfolgreiche_installationen:
            nachricht += "Erfolgreich installierte Einstellungen:\n"
            nachricht += "\n".join([f"✓ {name}" for name in erfolgreiche_installationen])
        
        if fehlgeschlagene_installationen:
            if erfolgreiche_installationen:
                nachricht += "\n\n"
            nachricht += "Fehlgeschlagene Installationen:\n"
            nachricht += "\n".join([f"✗ {name}" for name in fehlgeschlagene_installationen])
        
        # Status aktualisieren und Messagebox anzeigen
        if erfolgreiche_installationen and not fehlgeschlagene_installationen:
            self.update_status("Installation erfolgreich abgeschlossen")
            zeige_ergebnis_dialog(self, "Installation abgeschlossen", detaillierter_bericht)
        elif fehlgeschlagene_installationen and not erfolgreiche_installationen:
            self.update_status("Installation fehlgeschlagen")
            messagebox.showerror("Installation fehlgeschlagen", nachricht)
        else:
            self.update_status("Installation teilweise erfolgreich")
            zeige_ergebnis_dialog(self, "Installation teilweise erfolgreich", detaillierter_bericht)
        
        # Buttons wieder aktivieren
        self.left_panel.set_buttons_state("normal")
    
    def _erstelle_detaillierten_bericht(self, erfolgreiche_installationen, installations_details):
        """
        Erstellt einen detaillierten Bericht über die Installation.
        
        Args:
            erfolgreiche_installationen (list): Liste der erfolgreich installierten Einstellungen
            installations_details (dict): Details zu den kopierten Dateien
            
        Returns:
            str: Detaillierter Bericht zur Installation
        """
        bericht = ""
        
        if not erfolgreiche_installationen:
            return "Keine Einstellungen wurden installiert."
        
        bericht += "Folgende Dateien wurden installiert:\n\n"
        
        for setting_name in erfolgreiche_installationen:
            bericht += f"Einstellung: {setting_name}\n"
            bericht += "-" * 30 + "\n"
            
            if setting_name in installations_details:
                for file_info in installations_details[setting_name]:
                    bericht += f"  • {file_info['type']}: {file_info['file']}\n"
                    bericht += f"    ➔ Ziel: {file_info['destination']}\n\n"
            else:
                bericht += "  Keine Details verfügbar.\n\n"
        
        return bericht