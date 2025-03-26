import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox


class CheckboxFrame(ctk.CTkScrollableFrame):
    """Ein anpassbarer Frame mit Checkboxen im Apple-Stil."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.checkboxes = {}
        self.checkbox_vars = {}
        self.callback = None
    
    def add_item(self, item_text, item_id=None):
        """Fügt eine Checkbox zum Frame hinzu."""
        if item_id is None:
            item_id = item_text
            
        # Variable für Checkbox-Status
        var = tk.BooleanVar(value=False)
        self.checkbox_vars[item_id] = var
        
        # Container für die Checkbox-Zeile im Apple-Stil
        row_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=8, height=36)
        row_frame.pack(fill="x", padx=2, pady=4)
        
        # Checkbox im Apple-Stil
        checkbox = ctk.CTkCheckBox(
            row_frame, 
            text=item_text,
            variable=var,
            onvalue=True, 
            offvalue=False,
            text_color="#000000",  # Schwarz für Text
            fg_color="#007AFF",    # Apple Blau für ausgewählte Checkboxen
            hover_color="#0063CC", # Dunkleres Blau für Hover
            checkbox_width=20,
            checkbox_height=20,
            border_width=1,
            corner_radius=4,
            font=ctk.CTkFont(size=13),
            command=lambda: self._on_checkbox_change(item_id)
        )
        checkbox.pack(side="left", padx=10, pady=8, fill="x", expand=True, anchor="w")
        
        # Zeile und Checkbox speichern
        self.checkboxes[item_id] = {"checkbox": checkbox, "row": row_frame}
    
    def clear(self):
        """Entfernt alle Checkboxen."""
        for item in self.checkboxes.values():
            item["row"].destroy()
        self.checkboxes = {}
        self.checkbox_vars = {}
    
    def get_checked_items(self):
        """Gibt eine Liste der ausgewählten Items zurück."""
        return [item_id for item_id, var in self.checkbox_vars.items() if var.get()]
    
    def check_all(self):
        """Wählt alle Checkboxen aus."""
        for var in self.checkbox_vars.values():
            var.set(True)
        # Callback aufrufen, wenn registriert
        if self.callback:
            self.callback()
    
    def uncheck_all(self):
        """Hebt die Auswahl aller Checkboxen auf."""
        for var in self.checkbox_vars.values():
            var.set(False)
        # Callback aufrufen, wenn registriert
        if self.callback:
            self.callback()
    
    def set_callback(self, callback):
        """Setzt die Callback-Funktion für Änderungen."""
        self.callback = callback
    
    def _on_checkbox_change(self, item_id):
        """Interner Handler für Checkbox-Änderungen."""
        if self.callback:
            self.callback(item_id)


class LeftPanel(ctk.CTkFrame):
    """
    Panel für die linke Seite der Anwendung im Apple-Design-Stil.
    Enthält Erklärungstext, Einstellungsliste und Buttons.
    """
    
    def __init__(self, parent, main_app):
        """Initialisiert das Panel."""
        super().__init__(parent, corner_radius=10, fg_color="#F5F5F7")  # Helles Apple-Grau
        self.main_app = main_app
        self.einstellungen_daten = []
        self._erstelle_ui()
    
    def _erstelle_ui(self):
        """Erstellt die UI-Elemente für das Panel im Apple-Design-Stil."""
        # Hauptcontainer für bessere Ausrichtung
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Sektionsheader für Erklärung
        self.info_section = self._create_section_header("Über dieses Tool", "Dieses Tool installiert vordefinierte Einstellungen für Adobe-Programme.")
        self.info_section.pack(fill="x", pady=(0, 15))
        
        # Klarerer Hinweis statt "Files Box"
        self.hint_label = ctk.CTkLabel(
            self.content_frame,
            text="Das Tool installiert PDF-Einstellungen (.joboptions), Farbeinstellungen (.csf) und ICC-Profile.",
            font=ctk.CTkFont(size=12),
            text_color="#666666",
            wraplength=350,
            justify="left"
        )
        self.hint_label.pack(fill="x", pady=(0, 15))
        
        # Sektionsheader für Einstellungen
        self.settings_section = self._create_section_header("Verfügbare Einstellungen", "Wählen Sie die zu installierenden Einstellungen aus.")
        self.settings_section.pack(fill="x", pady=(0, 10))
        
        # Einstllungen-Container im Apple-Stil
        self.list_container = ctk.CTkFrame(self.content_frame, corner_radius=10, fg_color="#FFFFFF", border_width=1, border_color="#E5E5EA")
        self.list_container.pack(fill="both", expand=True, pady=(0, 15))
        
        # Checkbox-Liste mit größerem Abstand zwischen Elementen
        self.checkbox_frame = CheckboxFrame(
            self.list_container,
            fg_color="#FFFFFF",
            corner_radius=0,
            border_width=0,
            width=350
        )
        self.checkbox_frame.pack(padx=0, pady=5, fill="both", expand=True)
        self.checkbox_frame.set_callback(self.on_checkbox_change)
        
        # Button-Container im Apple-Stil
        self.button_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.button_container.pack(fill="x", pady=(0, 15))
        
        # Buttons im Apple-Stil
        self.alle_button = ctk.CTkButton(
            self.button_container, 
            text="Alle auswählen",
            command=self.alle_auswaehlen,
            fg_color="#E9E9EB",  # Helles Grau
            text_color="#000000", # Schwarz
            hover_color="#DEDEE0",
            corner_radius=6,
            height=32,
            border_width=0,
            font=ctk.CTkFont(size=13)
        )
        self.alle_button.pack(side="left", padx=(0, 5), fill="x", expand=True)
        
        self.keine_button = ctk.CTkButton(
            self.button_container, 
            text="Keine auswählen",
            command=self.keine_auswaehlen,
            fg_color="#E9E9EB",  # Helles Grau
            text_color="#000000", # Schwarz
            hover_color="#DEDEE0",
            corner_radius=6,
            height=32,
            border_width=0,
            font=ctk.CTkFont(size=13)
        )
        self.keine_button.pack(side="right", fill="x", expand=True)
        
        # Install-Button im Apple-Stil
        self.install_button = ctk.CTkButton(
            self.content_frame, 
            text="Einstellungen installieren",
            command=self.installiere_einstellungen,
            fg_color="#007AFF",  # Apple Blau
            text_color="#FFFFFF", # Weiß
            hover_color="#0062CC",
            corner_radius=6,
            height=38,
            border_width=0,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.install_button.pack(fill="x", pady=(0, 0))
    
    def _create_section_header(self, title, subtitle=None):
        """Erstellt einen Sektions-Header im Apple-Stil."""
        section = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        
        # Titel
        title_label = ctk.CTkLabel(
            section,
            text=title,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#000000",  # Schwarz
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(0, 2))
        
        # Untertitel (optional)
        if subtitle:
            subtitle_label = ctk.CTkLabel(
                section,
                text=subtitle,
                font=ctk.CTkFont(size=12),
                text_color="#666666",  # Grau
                anchor="w"
            )
            subtitle_label.pack(anchor="w")
        
        return section
    
    def lade_einstellungen(self, einstellungen_daten):
        """
        Lädt die Einstellungen in die Checkbox-Liste.
        
        Args:
            einstellungen_daten (list): Liste der Einstellungen
        """
        # Daten speichern
        self.einstellungen_daten = einstellungen_daten
        
        # Checkbox-Frame leeren
        self.checkbox_frame.clear()
        
        # Neue Einstellungen hinzufügen
        for einstellung in einstellungen_daten:
            self.checkbox_frame.add_item(einstellung["Name"])
    
    def alle_auswaehlen(self):
        """Wählt alle Einstellungen aus."""
        self.checkbox_frame.check_all()
    
    def keine_auswaehlen(self):
        """Hebt alle Auswahlen auf."""
        self.checkbox_frame.uncheck_all()
    
    def on_checkbox_change(self, item_id=None):
        """
        Handler für Änderungen an den Checkboxen.
        
        Args:
            item_id (str, optional): ID des geänderten Items
        """
        # Ausgewählte Einstellungen ermitteln
        selected_items = self.checkbox_frame.get_checked_items()
        
        # Beschreibung aktualisieren, wenn ein Item ausgewählt ist
        if selected_items:
            selected_name = selected_items[0]
            # Index des ausgewählten Elements finden
            selected_index = None
            for i, einstellung in enumerate(self.einstellungen_daten):
                if einstellung["Name"] == selected_name:
                    selected_index = i
                    break
                    
            if selected_index is not None:
                self.main_app.right_panel.zeige_beschreibung(selected_name, selected_index, selected_items)
        else:
            self.main_app.right_panel.zeige_beschreibung(None, None, None)
        
        # Install-Button aktualisieren
        if selected_items:
            count_text = f"Einstellungen installieren ({len(selected_items)})" if len(selected_items) > 1 else "Einstellung installieren"
            self.install_button.configure(text=count_text)
        else:
            self.install_button.configure(text="Einstellungen installieren")
    
    def installiere_einstellungen(self):
        """Startet die Installation der ausgewählten Einstellungen."""
        ausgewaehlte_einstellungen = self.checkbox_frame.get_checked_items()
        
        if not ausgewaehlte_einstellungen:
            messagebox.showwarning("Hinweis", "Bitte wählen Sie mindestens eine Einstellung aus.")
            return
        
        # Übergeben an die Hauptanwendung zur Installation
        self.main_app.installiere_einstellungen(ausgewaehlte_einstellungen)
    
    def set_buttons_state(self, state):
        """
        Setzt den Zustand aller Buttons.
        
        Args:
            state (str): "normal" oder "disabled"
        """
        self.alle_button.configure(state=state)
        self.keine_button.configure(state=state)
        
        if state == "disabled":
            self.install_button.configure(state=state, text="Installation läuft...")
        else:
            # Text basierend auf Anzahl ausgewählter Elemente zurücksetzen
            selected_items = self.checkbox_frame.get_checked_items()
            if selected_items:
                count_text = f"Einstellungen installieren ({len(selected_items)})" if len(selected_items) > 1 else "Einstellung installieren"
                self.install_button.configure(state=state, text=count_text)
            else:
                self.install_button.configure(state=state, text="Einstellungen installieren")