"""
Right Panel Modul für PDF-Export-Einstellungen-Installer

Dieses Modul enthält die Komponenten für die rechte Seite der GUI-Anwendung.
"""

import customtkinter as ctk
import os
import logging

try:
    from .. import joboptions_parser
    joboptions_verfuegbar = True
except ImportError:
    joboptions_verfuegbar = False
    logging.warning("Joboptions-Parser konnte nicht importiert werden. Beschreibungen werden nicht angezeigt.")

from ..utils import find_resource_path


class RightPanel(ctk.CTkFrame):
    """
    Panel für die rechte Seite der Anwendung.
    Enthält Beschreibungsbereich für ausgewählte Einstellungen und Hilfe-Buttons.
    """
    
    def __init__(self, parent, main_app):
        """Initialisiert das Panel."""
        super().__init__(parent, corner_radius=8, fg_color="#F1F5F9")
        self.main_app = main_app
        self.beschreibungen = {}  # Cache für geladene Beschreibungen
        self._erstelle_ui()
    
    def _erstelle_ui(self):
        """Erstellt die UI-Elemente für das Panel."""
        # Beschreibungsframe mit abgerundeten Ecken - kompakter
        self.beschreibung_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=8)
        self.beschreibung_frame.pack(fill="both", expand=True, padx=15, pady=(8, 8))
        
        # Beschreibungstitel - kompakter
        self.beschreibung_titel = ctk.CTkLabel(self.beschreibung_frame, 
                                             text="Beschreibung",
                                             font=ctk.CTkFont(size=15, weight="bold"),
                                             text_color="#1E40AF")
        self.beschreibung_titel.pack(anchor="w", padx=15, pady=(8, 2))
        
        # Untertitel für die Beschreibung (wird dynamisch aktualisiert) - kompakter
        self.beschreibung_untertitel = ctk.CTkLabel(self.beschreibung_frame, 
                                                 text="Bitte wählen Sie eine Einstellung aus der Liste.",
                                                 font=ctk.CTkFont(size=13, slant="italic"),
                                                 text_color="#6B7280")
        self.beschreibung_untertitel.pack(anchor="w", padx=15, pady=(0, 5))
        
        # Trennlinie - dünner
        self.separator = ctk.CTkFrame(self.beschreibung_frame, height=1, fg_color="#E5E7EB")
        self.separator.pack(fill="x", padx=15, pady=(0, 5))
        
        # Scrollbarer Beschreibungsbereich
        self.beschreibung_scroll = ctk.CTkScrollableFrame(self.beschreibung_frame, fg_color="transparent")
        self.beschreibung_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Beschreibungstext (wird dynamisch aktualisiert)
        default_desc = (
            "Hier erscheint die Beschreibung der ausgewählten Einstellung. "
            "Die Einstellungen enthalten vordefinierte Werte für den professionellen Druck."
        )
        
        self.beschreibung_label = ctk.CTkLabel(self.beschreibung_scroll, 
                                             text=default_desc,
                                             font=ctk.CTkFont(size=13),
                                             justify="left",
                                             wraplength=440)
        self.beschreibung_label.pack(anchor="w", fill="x")
        
        # Hilfe- und Info-Buttons im unteren Bereich - kompakter
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=15, pady=(3, 8))
        
        # Buttons in einer Reihe - kleiner
        self.info_button = ctk.CTkButton(self.button_frame, 
                                      text="Info", 
                                      command=self._zeige_info,
                                      width=110,
                                      height=30,
                                      fg_color="#6366F1", 
                                      hover_color="#4F46E5",
                                      corner_radius=6,
                                      font=ctk.CTkFont(size=13))
        self.info_button.pack(side="left", padx=(0, 10))
        
        self.hilfe_button = ctk.CTkButton(self.button_frame, 
                                       text="Hilfe", 
                                       command=self._zeige_hilfe,
                                       width=110,
                                       height=30,
                                       fg_color="#8B5CF6", 
                                       hover_color="#7C3AED",
                                       corner_radius=6,
                                       font=ctk.CTkFont(size=13))
        self.hilfe_button.pack(side="left")
    
    def _zeige_info(self):
        """Zeigt Informationen zur Anwendung an."""
        from .dialogs import zeige_info_dialog
        zeige_info_dialog(self.main_app)
    
    def _zeige_hilfe(self):
        """Zeigt Hilfe zur Anwendung an."""
        from .dialogs import zeige_hilfe_dialog
        zeige_hilfe_dialog(self.main_app)
    
    def zeige_beschreibung(self, selected_name, selected_index, selection):
        """
        Zeigt die Beschreibung der ausgewählten Einstellung an.
        
        Args:
            selected_name (str): Name der ausgewählten Einstellung oder None
            selected_index (int): Index der ausgewählten Einstellung oder None
            selection (tuple): Tupel aller ausgewählten Indices oder None
        """
        if not selected_name:
            # Keine Auswahl - Standardtext anzeigen
            self.beschreibung_untertitel.configure(
                text="Bitte wählen Sie eine Einstellung aus der Liste.",
                text_color="#6B7280"
            )
            self.beschreibung_label.configure(
                text="Hier erscheint die Beschreibung der ausgewählten Einstellung.",
                text_color="#6B7280"
            )
            
            # Hinweisrahmen entfernen, falls vorhanden
            if hasattr(self, 'hinweis_frame'):
                self.hinweis_frame.pack_forget()
            
            return
        
        # Prüfen, ob die Beschreibung bereits im Cache ist
        if selected_name not in self.beschreibungen:
            # Beschreibung noch nicht geladen, jetzt laden
            self._lade_beschreibung(selected_name, selected_index)
        
        # Beschreibung aus dem Cache abrufen
        beschreibung = self.beschreibungen.get(selected_name, f"Keine Beschreibung für '{selected_name}' verfügbar.")
        
        # Mehrfachauswahl-Hinweis zeigen oder verstecken
        if selection and len(selection) > 1:
            self._zeige_mehrfachauswahl_hinweis(selected_name, len(selection))
        else:
            # Bei Einzelauswahl den Hinweisrahmen entfernen
            if hasattr(self, 'hinweis_frame'):
                self.hinweis_frame.pack_forget()
            
            self.beschreibung_untertitel.configure(
                text=f"Detaillierte Beschreibung von '{selected_name}':",
                text_color="#4B5563"
            )
        
        # Beschreibung anzeigen
        self.beschreibung_label.configure(
            text=beschreibung,
            text_color="#374151"
        )
    
    def _zeige_mehrfachauswahl_hinweis(self, selected_name, selected_count):
        """
        Zeigt einen gelben Hinweis an, wenn mehrere Einstellungen ausgewählt wurden.
        
        Args:
            selected_name (str): Name der ersten ausgewählten Einstellung
            selected_count (int): Anzahl der ausgewählten Einstellungen
        """
        anzahl_text = f"Sie haben {selected_count} Einstellungen ausgewählt. "
        anzahl_text += f"Hier sehen Sie die Beschreibung für '{selected_name}':"
        
        # Erstelle Hinweisrahmen mit gelbem Hintergrund für Mehrfachauswahl
        if not hasattr(self, 'hinweis_frame'):
            self.hinweis_frame = ctk.CTkFrame(
                self.beschreibung_frame, 
                fg_color="#FEF9C3", 
                corner_radius=6
            )
            self.hinweis_text = ctk.CTkLabel(
                self.hinweis_frame, 
                text=anzahl_text,
                text_color="#854D0E",
                font=ctk.CTkFont(size=13, slant="italic"),
                wraplength=440
            )
            self.hinweis_text.pack(padx=10, pady=8)
        else:
            self.hinweis_text.configure(text=anzahl_text)
        
        # Paket den Frame vor dem Beschreibungslabel
        if self.hinweis_frame.winfo_manager() != 'pack':
            self.hinweis_frame.pack(fill="x", padx=15, pady=(0, 10), before=self.separator)
        
        # Normale Untertitelanzeige setzen
        self.beschreibung_untertitel.configure(
            text=f"Detaillierte Beschreibung von '{selected_name}':",
            text_color="#4B5563"
        )
    
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
            einstellung = self.main_app.einstellungen_daten[index]
            
            # Prüfen, ob PDF-Einstellungen vorhanden sind
            if "Adobe PDF Settings" in einstellung and einstellung["Adobe PDF Settings"]:
                joboptions_pfad = find_resource_path(os.path.join("resources", einstellung["Adobe PDF Settings"]))
                
                # Statusmeldung aktualisieren
                self.main_app.update_status(f"⏳ Lade Beschreibung für {name}...")
                
                # Beschreibung extrahieren
                beschreibung = joboptions_parser.get_readable_description(joboptions_pfad)
                
                if beschreibung:
                    self.beschreibungen[name] = beschreibung
                else:
                    self.beschreibungen[name] = standard_beschreibung
            else:
                self.beschreibungen[name] = f"Diese Einstellung enthält keine PDF-Exporteinstellungen."
                
            # Status zurücksetzen
            self.main_app.update_status("✓ Bereit")
            
        except Exception as e:
            # Bei Fehlern Standard-Beschreibung verwenden und Fehler loggen
            logging.error(f"Fehler beim Laden der Beschreibung für {name}: {e}")
            self.beschreibungen[name] = standard_beschreibung
            
    def set_buttons_state(self, state):
        """
        Setzt den Zustand aller Buttons.
        
        Args:
            state (str): "normal" oder "disabled"
        """
        self.info_button.configure(state=state)
        self.hilfe_button.configure(state=state)