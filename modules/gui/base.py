"""
Basis-GUI-Modul für PDF-Export-Einstellungen-Installer

Dieses Modul enthält die Hauptklasse für die GUI-Anwendung.
"""

import tkinter as tk
import customtkinter as ctk
import logging
import threading
import sys
import os
from tkinter import messagebox

from ..utils import ist_adobe_bridge_installiert, lade_konfigurationen
from ..installer import EinstellungsInstaller
from .left_panel import LeftPanel
from .right_panel import RightPanel


class PDFExportEinstellungenGUI(ctk.CTk):
    """
    Hauptklasse für die PDF-Export-Einstellungen-Anwendung GUI.
    Optimiert für zweispaltiges Layout mit modernem, vertrauenswürdigem Design.
    """
    
    def __init__(self):
        """Initialisiert die Anwendung und erstellt die GUI."""
        super().__init__()
        
        # Anwendungsdesign konfigurieren
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Fensterkonfiguration
        self.title("PDF-Export Einstellungen Installer")
        self.geometry("1250x910")  # 25% breiter und 30% höher
        self.minsize(1125, 910)    # Entsprechend angepasste Mindestgröße
        
        # Fenster zentrieren
        self._center_window()
        
        # App-Icon setzen (wenn verfügbar)
        self._set_app_icon()
        
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
    
    def _center_window(self):
        """Zentriert das Fenster auf dem Bildschirm."""
        # Warte, bis das Fenster gerendert wurde, um korrekte Abmessungen zu erhalten
        self.update_idletasks()
        
        # Bildschirmabmessungen abrufen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Fensterabmessungen abrufen
        width = self.winfo_width()
        height = self.winfo_height()
        
        # Position berechnen (Bildschirmmitte)
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Fensterposition setzen
        self.geometry(f"+{x}+{y}")
    
    def _set_app_icon(self):
        """Setzt das Anwendungssymbol, wenn verfügbar."""
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))), "links", "Icon.svg")
        
        # Fallback zu anderen möglichen Icon-Formaten, falls SVG nicht unterstützt wird
        if not os.path.exists(icon_path):
            for ext in ['.ico', '.png']:
                alt_path = icon_path.replace('.svg', ext)
                if os.path.exists(alt_path):
                    icon_path = alt_path
                    break
        
        if os.path.exists(icon_path):
            try:
                if sys.platform == "win32":
                    self.iconbitmap(icon_path.replace('.svg', '.ico'))
                elif sys.platform == "darwin":
                    # macOS verwendet .icns Format
                    pass
                else:
                    # Linux unterstützt .png über tk.PhotoImage
                    icon = tk.PhotoImage(file=icon_path.replace('.svg', '.png'))
                    self.iconphoto(True, icon)
            except Exception as e:
                logging.warning(f"Konnte App-Icon nicht setzen: {e}")
    
    def _erstelle_ui(self):
        """Erstellt alle UI-Elemente der Anwendung im zweispaltigen Layout."""
        # Hauptcontainer mit schmaleren Abständen
        self.haupt_container = ctk.CTkFrame(self, corner_radius=10, fg_color="#F8F9FA")
        self.haupt_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Konfiguration des Grid-Layouts
        self.haupt_container.grid_columnconfigure(0, weight=5)  # Linke Spalte
        self.haupt_container.grid_columnconfigure(1, weight=6)  # Rechte Spalte
        self.haupt_container.grid_rowconfigure(1, weight=1)    # Hauptinhalt soll sich ausdehnen
        
        # ----- KOPFBEREICH (über beiden Spalten) -----
        self._erstelle_kopfbereich()
        
        # ----- LINKE SPALTE -----
        self.left_panel = LeftPanel(self.haupt_container, self)
        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # ----- RECHTE SPALTE -----
        self.right_panel = RightPanel(self.haupt_container, self)
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)
        
        # ----- STATUSBEREICH (unter beiden Spalten) -----
        self._erstelle_statusbereich()
    
    def _erstelle_kopfbereich(self):
        """Erstellt den Kopfbereich der Anwendung."""
        # Header-Frame mit reduzierter Höhe
        self.header_frame = ctk.CTkFrame(self.haupt_container, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(8, 2))
        
        # Horizontales Layout für Logo und Titel
        self.header_content = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.header_content.pack(fill="x")
        
        # Versuche, das Logo zu laden - platzieren wir links neben dem Titel
        try:
            # SVG-Logo-Pfad
            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__)))), "links", "Icon.svg")
                
            # Placeholder für Logo (kann später erweitert werden)
            logo_label = ctk.CTkLabel(
                self.header_content, 
                text="🖨️", 
                font=ctk.CTkFont(size=32),
                text_color="#1E3A8A"
            )
            logo_label.pack(side="left", padx=(10, 5))
        except Exception as e:
            logging.warning(f"Konnte Logo nicht laden: {e}")
        
        # Titel mit größerem Font und Farbe - direkt neben dem Logo
        self.logo_label = ctk.CTkLabel(
            self.header_content, 
            text="PDF-Export Einstellungen", 
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#1E3A8A"
        )
        self.logo_label.pack(side="left", pady=0)
        
        # Untertitel direkt unter dem Header-Content mit minimalem Abstand
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame, 
            text="Professionelle Druckeinstellungen für Adobe-Programme",
            font=ctk.CTkFont(size=14),
            text_color="#4B5563"
        )
        self.subtitle_label.pack(pady=(0, 5))
        
        # Trennlinie für visuelle Abgrenzung - mit minimalem Abstand
        self.separator = ctk.CTkFrame(self.header_frame, height=1, fg_color="#E5E7EB")
        self.separator.pack(fill="x", padx=10, pady=(0, 2))
    
    def _erstelle_statusbereich(self):
        """Erstellt den Statusbereich am unteren Rand mit modernem Design."""
        # Statusanzeige am unteren Rand - kompakter
        self.status_frame = ctk.CTkFrame(self.haupt_container, fg_color="#F3F4F6", corner_radius=6)
        self.status_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        
        # Status-Label mit Icon-Simulation - kleinerer Innenabstand
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="⏺ Bereit", 
            anchor="w",
            font=ctk.CTkFont(size=13),
            text_color="#4B5563"
        )
        self.status_label.pack(padx=15, pady=5, anchor="w", side="left")
    
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
        
        # Einstellungen an das linke Panel übergeben
        self.left_panel.lade_einstellungen(self.einstellungen_daten)
        
        # Status aktualisieren
        self.update_status(f"✓ {len(self.einstellungen_daten)} Einstellungen verfügbar")
        
        # Bridge-Hinweis anzeigen, falls nicht installiert
        if not self.bridge_installiert:
            self._zeige_bridge_hinweis()
    
    def _zeige_bridge_hinweis(self):
        """Zeigt den Hinweis an, wenn Adobe Bridge nicht installiert ist."""
        self.bridge_hinweis_frame = ctk.CTkFrame(
            self.haupt_container, 
            fg_color="#FFF7ED", 
            corner_radius=6
        )
        self.bridge_hinweis_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        
        bridge_hinweis_text = (
            "⚠️ Adobe Bridge nicht installiert. Farbeinstellungen müssen in jedem Adobe-Programm "
            "unter 'Bearbeiten > Farbeinstellungen' manuell ausgewählt werden."
        )
        
        self.bridge_hinweis_text = ctk.CTkLabel(
            self.bridge_hinweis_frame, 
            text=bridge_hinweis_text,
            text_color="#9A3412",
            font=ctk.CTkFont(size=13),
            wraplength=960
        )
        self.bridge_hinweis_text.pack(padx=15, pady=6)
    
    def update_status(self, message):
        """
        Aktualisiert die Statusanzeige mit visuellen Indikatoren.
        
        Args:
            message (str): Die anzuzeigende Nachricht
        """
        # Status-Icon basierend auf Nachrichteninhalt setzen
        if "fehler" in message.lower() or "error" in message.lower():
            icon = "⛔ "
            color = "#B91C1C"  # Rot für Fehler
        elif "erfolg" in message.lower() or "fertig" in message.lower() or "✓" in message:
            icon = "✅ "
            color = "#15803D"  # Grün für Erfolg
        elif "warte" in message.lower() or "läuft" in message.lower() or "installation" in message.lower():
            icon = "⏳ "
            color = "#0369A1"  # Blau für laufende Prozesse
        else:
            icon = "ℹ️ "
            color = "#4B5563"  # Neutral
        
        # Wenn das Icon bereits in der Nachricht ist, nicht nochmal hinzufügen
        if not any(symbol in message[:2] for symbol in ["⛔", "✅", "⏳", "ℹ️", "⏺", "✓", "⚠️"]):
            message = icon + message
        
        # Status aktualisieren mit entsprechender Farbe
        self.status_label.configure(text=message, text_color=color)
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
        self.update_status("⏳ Installation wird vorbereitet...")
        
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
            self.update_status("✅ Installation erfolgreich abgeschlossen")
            zeige_ergebnis_dialog(self, "Installation abgeschlossen", detaillierter_bericht)
        elif fehlgeschlagene_installationen and not erfolgreiche_installationen:
            self.update_status("⛔ Installation fehlgeschlagen")
            messagebox.showerror("Installation fehlgeschlagen", nachricht)
        else:
            self.update_status("⚠️ Installation teilweise erfolgreich")
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