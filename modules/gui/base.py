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
    Optimiert für zweispaltiges Layout mit Apple-Design-Stil.
    """
    
    def __init__(self):
        """Initialisiert die Anwendung und erstellt die GUI."""
        super().__init__()
        
        # Anwendungsdesign konfigurieren (Apple-Stil)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Fensterkonfiguration
        self.title("PDF-Export Einstellungen")
        self.geometry("1100x760")  # Breiter als hoch (typisch für Apple)
        self.minsize(950, 650)
        
        # System erkennen
        self.is_mac = sys.platform == "darwin"
        
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
        """Erstellt alle UI-Elemente der Anwendung im zweispaltigen Apple-Design-Stil."""
        # Hauptcontainer mit spezifischen Apple-Farben
        self.haupt_container = ctk.CTkFrame(self, corner_radius=0, fg_color="#F5F5F7")  # Apple Hintergrundfarbe
        self.haupt_container.pack(fill=tk.BOTH, expand=True)
        
        # Konfiguration des Grid-Layouts
        self.haupt_container.grid_columnconfigure(0, weight=2)  # Linke Spalte
        self.haupt_container.grid_columnconfigure(1, weight=3)  # Rechte Spalte
        self.haupt_container.grid_rowconfigure(1, weight=1)     # Hauptinhalt soll sich ausdehnen
        
        # ----- KOPFBEREICH (über beiden Spalten) -----
        self._erstelle_kopfbereich()
        
        # ----- LINKE SPALTE -----
        self.left_panel = LeftPanel(self.haupt_container, self)
        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(0, 20))
        
        # ----- RECHTE SPALTE -----
        self.right_panel = RightPanel(self.haupt_container, self)
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(0, 20))
        
        # ----- STATUSBEREICH (unter beiden Spalten) -----
        self._erstelle_statusbereich()
    
    def _erstelle_kopfbereich(self):
        """Erstellt den Kopfbereich der Anwendung im Apple-Stil."""
        # Header-Frame
        self.header_frame = ctk.CTkFrame(self.haupt_container, fg_color="transparent", height=60)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(20, 15))
        
        # Titel im Apple-Stil (zentriert, größere Schrift)
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="PDF-Export Einstellungen", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#000000"  # Apple verwendet Schwarz für Überschriften
        )
        self.title_label.place(relx=0.5, rely=0.5, anchor="center")  # Zentriert
        
        # Untertitel (falls benötigt)
        # self.subtitle_label = ctk.CTkLabel(...)
    
    def _erstelle_statusbereich(self):
        """Erstellt den Statusbereich am unteren Rand im Apple-Stil."""
        # Statusbalken
        self.status_frame = ctk.CTkFrame(self.haupt_container, fg_color="#E5E5EA", height=30, corner_radius=0)
        self.status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        
        # Status-Label im Apple-Stil
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="• Bereit", 
            anchor="w",
            font=ctk.CTkFont(size=12),
            text_color="#8E8E93"  # Apple Grau
        )
        self.status_label.pack(padx=20, fill="both")
    
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
            fg_color="#FEF7E5",  # Helles Gelb (Apple Warning Style)
            corner_radius=0,
            height=36
        )
        self.bridge_hinweis_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
        
        bridge_hinweis_text = (
            "⚠️ Adobe Bridge nicht installiert. Farbeinstellungen müssen in jedem Adobe-Programm "
            "manuell ausgewählt werden."
        )
        
        self.bridge_hinweis_text = ctk.CTkLabel(
            self.bridge_hinweis_frame, 
            text=bridge_hinweis_text,
            text_color="#B25000",  # Orange-Braun für Warnungen
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self.bridge_hinweis_text.pack(padx=20, pady=0, fill="both")
    
    def update_status(self, message):
        """
        Aktualisiert die Statusanzeige im Apple-Stil mit visuellen Indikatoren.
        
        Args:
            message (str): Die anzuzeigende Nachricht
        """
        # Status-Icon basierend auf Nachrichteninhalt setzen
        if "fehler" in message.lower() or "error" in message.lower():
            icon = "• "
            color = "#FF3B30"  # Apple Rot für Fehler
        elif "erfolg" in message.lower() or "fertig" in message.lower() or "✓" in message:
            icon = "• "
            color = "#34C759"  # Apple Grün für Erfolg
        elif "warte" in message.lower() or "läuft" in message.lower() or "installation" in message.lower():
            icon = "• "
            color = "#007AFF"  # Apple Blau für laufende Prozesse
        else:
            icon = "• "
            color = "#8E8E93"  # Apple Grau für normale Meldungen
        
        # Wenn das Icon bereits in der Nachricht ist, nicht nochmal hinzufügen
        if not any(symbol in message[:2] for symbol in ["•", "✓", "⚠️", "⏺"]):
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
        self.update_status("• Installation wird vorbereitet...")
        
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
            self.update_status("• Installation erfolgreich abgeschlossen")
            zeige_ergebnis_dialog(self, "Installation abgeschlossen", detaillierter_bericht)
        elif fehlgeschlagene_installationen and not erfolgreiche_installationen:
            self.update_status("• Installation fehlgeschlagen")
            messagebox.showerror("Installation fehlgeschlagen", nachricht)
        else:
            self.update_status("• Installation teilweise erfolgreich")
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
                    bericht += f"    → Ziel: {file_info['destination']}\n\n"
            else:
                bericht += "  Keine Details verfügbar.\n\n"
        
        return bericht