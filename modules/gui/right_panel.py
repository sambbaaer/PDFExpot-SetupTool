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
        super().__init__(parent, corner_radius=6, fg_color="#F5F5F7")  # Helles Apple-Grau
        self.main_app = main_app
        self.beschreibungen = {}  # Cache für geladene Beschreibungen
        self._erstelle_ui()
    
    def _erstelle_ui(self):
        """Erstellt die UI-Elemente für das Panel im Apple-Design-Stil."""
        # Hauptcontainer mit mehr Weißraum
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Einstellungsinformationen im oberen Bereich
        self.info_frame = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color="#FFFFFF", height=120)
        self.info_frame.pack(fill="x", pady=(0, 15))
        
        # Grid-Layout für Infos
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure(1, weight=0)
        
        # Icon-/Titel-Bereich
        self.icon_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.icon_frame.grid(row=0, column=0, sticky="nw", padx=15, pady=15)
        
        # PDF-Icon (simuliert mit Text)
        self.icon_label = ctk.CTkLabel(
            self.icon_frame, 
            text="PDF", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FF3B30",  # Apple Rot
            width=45,
            height=45,
            fg_color="#FFF5F5",
            corner_radius=8
        )
        self.icon_label.pack(side="left", padx=(0, 10))
        
        # Titel & Untertitel für ausgewählte Einstellung
        self.title_frame = ctk.CTkFrame(self.icon_frame, fg_color="transparent")
        self.title_frame.pack(side="left", fill="y", pady=3)
        
        self.title_label = ctk.CTkLabel(
            self.title_frame, 
            text="Keine Auswahl", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#000000",  # Schwarz für Titel
            anchor="w"
        )
        self.title_label.pack(anchor="w")
        
        self.subtitle_label = ctk.CTkLabel(
            self.title_frame, 
            text="Wählen Sie eine Einstellung", 
            font=ctk.CTkFont(size=13),
            text_color="#86868B",  # Apple Grau
            anchor="w"
        )
        self.subtitle_label.pack(anchor="w")
        
        # Installationstyp-Badges
        self.badges_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.badges_frame.grid(row=1, column=0, sticky="sw", padx=15, pady=(0, 15))
        
        # Badges für die verschiedenen Dateitypen
        self.badge_pdf = self._create_badge("PDF", "#FF9500")  # Apple Orange
        self.badge_pdf.pack(side="left", padx=(0, 5))
        
        self.badge_color = self._create_badge("Farbe", "#007AFF")  # Apple Blau
        self.badge_color.pack(side="left", padx=5)
        
        self.badge_icc = self._create_badge("ICC", "#5AC8FA")  # Apple Hellblau
        self.badge_icc.pack(side="left", padx=5)
        
        # Kompakte Beschreibung im mittleren Bereich
        self.beschreibung_frame = self._create_section("Beschreibung", True)
        
        # Scrollbarer Beschreibungstext
        self.beschreibung_text = ctk.CTkTextbox(
            self.beschreibung_frame, 
            wrap="word",
            font=ctk.CTkFont(size=13),
            text_color="#000000",
            fg_color="#FFFFFF",
            border_width=0,
            height=100  # Reduzierte Höhe!
        )
        self.beschreibung_text.pack(fill="both", expand=True, padx=2, pady=(0, 5))
        
        # Default-Text setzen
        self.beschreibung_text.insert("1.0", "Hier erscheint die Beschreibung der ausgewählten Einstellung. "
                                      "Wählen Sie eine Einstellung aus der Liste.")
        self.beschreibung_text.configure(state="disabled")  # Schreibschutz
        
        # Technische Details im unteren Bereich
        self.details_frame = self._create_section("Technische Details", False)
        
        # Infozeilen im Apple-Stil
        self.info_lines = [
            {"label": "Papiertyp", "value": "-"},
            {"label": "ICC-Profil", "value": "-"},
            {"label": "PDF-Standard", "value": "-"}
        ]
        
        # Info-Zeilen erstellen
        for i, info in enumerate(self.info_lines):
            self._create_info_line(self.details_frame, info["label"], info["value"], i)
        
        # Button-Bereich im Footer
        self.footer_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", height=40)
        self.footer_frame.pack(fill="x", pady=(10, 0))
        
        # Buttons für Hilfe und Info
        self.hilfe_button = ctk.CTkButton(
            self.footer_frame, 
            text="Hilfe", 
            command=self._zeige_hilfe,
            width=100,
            height=32,
            fg_color="#E9E9EB",  # Helles Grau
            text_color="#000000",  # Schwarz
            hover_color="#DEDEE0",
            corner_radius=6,
            border_width=0,
            font=ctk.CTkFont(size=13)
        )
        self.hilfe_button.pack(side="left")
        
        self.info_button = ctk.CTkButton(
            self.footer_frame, 
            text="Info", 
            command=self._zeige_info,
            width=100,
            height=32,
            fg_color="#E9E9EB",  # Helles Grau
            text_color="#000000",  # Schwarz
            hover_color="#DEDEE0",
            corner_radius=6,
            border_width=0,
            font=ctk.CTkFont(size=13)
        )
        self.info_button.pack(side="left", padx=(10, 0))
    
    def _create_badge(self, text, color):
        """Erstellt ein Badge im Apple-Stil."""
        badge = ctk.CTkLabel(
            self.badges_frame,  # Master-Widget
            text=text,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=color,
            text_color="#FFFFFF",
            corner_radius=4,
            width=0,
            height=24,
            padx=8
        )
        return badge
    
    def _create_section(self, title, with_border=True):
        """Erstellt einen Abschnittsrahmen im Apple-Stil."""
        # Container
        frame = ctk.CTkFrame(
            self.main_container, 
            corner_radius=10, 
            fg_color="#FFFFFF",
            border_width=1 if with_border else 0,
            border_color="#E5E5EA"  # Apple Separator
        )
        frame.pack(fill="x", pady=(0, 10))
        
        # Titelzeile
        title_label = ctk.CTkLabel(
            frame, 
            text=title, 
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#000000",
            anchor="w"
        )
        title_label.pack(anchor="w", padx=15, pady=(12, 8))
        
        # Trennlinie (optional)
        if with_border:
            separator = ctk.CTkFrame(frame, height=1, fg_color="#E5E5EA")
            separator.pack(fill="x", padx=0, pady=(0, 5))
            
        return frame
    
    def _create_info_line(self, parent, label, value, row):
        """Erstellt eine Infozeile im Apple-Stil."""
        # Label-Spalte
        label_frame = ctk.CTkFrame(parent, fg_color="transparent")
        label_frame.pack(fill="x", padx=15, pady=4)
        
        # Zweispaltiges Layout
        label_frame.grid_columnconfigure(0, weight=1)
        label_frame.grid_columnconfigure(1, weight=1)
        
        # Label
        label_text = ctk.CTkLabel(
            label_frame, 
            text=label,
            font=ctk.CTkFont(size=13),
            text_color="#86868B",  # Apple Grau
            anchor="w"
        )
        label_text.grid(row=0, column=0, sticky="w")
        
        # Wert
        value_text = ctk.CTkLabel(
            label_frame, 
            text=value,
            font=ctk.CTkFont(size=13),
            text_color="#000000",  # Schwarz
            anchor="e"
        )
        value_text.grid(row=0, column=1, sticky="e")
        
        # Diese Referenz speichern, um später aktualisieren zu können
        setattr(self, f"value_{row}", value_text)
    
    def _zeige_info(self):
        """Zeigt Informationen zur Anwendung an."""
        from .dialogs import zeige_info_dialog
        zeige_info_dialog(self.main_app)
    
    def _zeige_hilfe(self):
        """Zeigt Hilfe zur Anwendung an."""
        from .dialogs import zeige_hilfe_dialog
        zeige_hilfe_dialog(self.main_app)
    
    def _update_badges(self, einstellung):
        """Aktualisiert die Badges basierend auf der ausgewählten Einstellung."""
        # Alle Badges sichtbar machen
        self.badge_pdf.pack(side="left", padx=(0, 5))
        self.badge_color.pack(side="left", padx=5)
        self.badge_icc.pack(side="left", padx=5)
        
        # Badges ausblenden, wenn die zugehörige Einstellung nicht vorhanden ist
        if einstellung:
            if not einstellung.get("Adobe PDF Settings"):
                self.badge_pdf.pack_forget()
            if not einstellung.get("Color Setting"):
                self.badge_color.pack_forget()
            if not einstellung.get("ICC-Profil"):
                self.badge_icc.pack_forget()
    
    def _update_tech_details(self, einstellung):
        """Aktualisiert die technischen Details basierend auf der ausgewählten Einstellung."""
        if einstellung:
            # Papiertyp aus der JSON-Datei verwenden
            paper_type = einstellung.get("Paper Type", "unknown")
            
            # Benutzerfreundliche Bezeichnung für den Papiertyp
            papiertyp_map = {
                "coated": "Gestrichenes Papier",
                "uncoated": "Ungestrichenes Papier",
                "recycled": "Recycling-Papier",
                "specialty": "Spezialmedium",
                "newspaper": "Zeitungspapier"
            }
            
            # Papiertyp-Text oder Fallback
            papiertyp = papiertyp_map.get(paper_type, "Spezialmedium")
            
            # Werte aktualisieren
            self.value_0.configure(text=papiertyp)
            self.value_1.configure(text=einstellung.get("ICC-Profil", "-"))
            
            # PDF Standard aus der Joboptions-Datei ermitteln (vereinfacht)
            pdf_standard = "PDF/X-4"  # Standardwert
            self.value_2.configure(text=pdf_standard)
        else:
            # Auf Standardwerte zurücksetzen
            self.value_0.configure(text="-")
            self.value_1.configure(text="-")
            self.value_2.configure(text="-")
    
    def zeige_beschreibung(self, selected_name, selected_index, selection):
        """
        Zeigt die Beschreibung der ausgewählten Einstellung an.
        
        Args:
            selected_name (str): Name der ausgewählten Einstellung oder None
            selected_index (int): Index der ausgewählten Einstellung oder None
            selection (tuple): Tupel aller ausgewählten Indices oder None
        """
        # TextBox auf bearbeitbar setzen
        self.beschreibung_text.configure(state="normal")
        # Text löschen
        self.beschreibung_text.delete("1.0", "end")
        
        if not selected_name:
            # Keine Auswahl - Standardtext anzeigen
            self.title_label.configure(text="Keine Auswahl")
            self.subtitle_label.configure(text="Wählen Sie eine Einstellung")
            
            self.beschreibung_text.insert("1.0", "Hier erscheint die Beschreibung der ausgewählten Einstellung. "
                                         "Wählen Sie eine Einstellung aus der Liste.")
            
            # Auch technische Details zurücksetzen
            self._update_tech_details(None)
            # Badges aktualisieren
            self._update_badges(None)
            
        else:
            # Einstellung gefunden
            einstellung = None if selected_index is None else self.main_app.einstellungen_daten[selected_index]
            
            # Titel setzen
            self.title_label.configure(text=selected_name)
            
            # Untertitel basierend auf der Mehrfachauswahl oder der Description
            if selection and len(selection) > 1:
                self.subtitle_label.configure(text=f"{len(selection)} Einstellungen ausgewählt")
            else:
                # Beschreibung aus der JSON-Datei verwenden
                beschreibung = einstellung.get("Description", "")
                if not beschreibung:
                    # Fallback zur alten Logik, wenn keine Beschreibung vorhanden
                    paper_type = einstellung.get("Paper Type", "")
                    if paper_type == "coated":
                        beschreibung = "Für gestrichenes Papier"
                    elif paper_type == "uncoated":
                        beschreibung = "Für ungestrichenes Papier"
                    else:
                        beschreibung = f"Einstellung für {paper_type}"
                
                self.subtitle_label.configure(text=beschreibung)
            
            # Prüfen, ob die Beschreibung bereits im Cache ist
            if selected_name not in self.beschreibungen:
                # Beschreibung noch nicht geladen, jetzt laden
                self._lade_beschreibung(selected_name, selected_index)
            
            # Beschreibung aus dem Cache abrufen
            beschreibung = self.beschreibungen.get(selected_name, f"Keine Beschreibung für '{selected_name}' verfügbar.")
            
            # Beschreibung anzeigen
            self.beschreibung_text.insert("1.0", beschreibung)
            
            # Technische Details aktualisieren
            self._update_tech_details(einstellung)
            
            # Badges aktualisieren
            self._update_badges(einstellung)
        
        # TextBox wieder auf schreibgeschützt setzen
        self.beschreibung_text.configure(state="disabled")
    
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
                    # Beschreibung kürzen, falls sie zu lang ist
                    if len(beschreibung) > 500:
                        beschreibung = beschreibung[:497] + "..."
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