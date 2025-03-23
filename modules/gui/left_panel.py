"""
Left Panel Modul für PDF-Export-Einstellungen-Installer

Dieses Modul enthält die Komponenten für die linke Seite der GUI-Anwendung.
"""

import tkinter as tk
import customtkinter as ctk


class LeftPanel(ctk.CTkFrame):
    """
    Panel für die linke Seite der Anwendung.
    Enthält Erklärungstext, Einstellungsliste und Buttons.
    """
    
    def __init__(self, parent, main_app):
        """Initialisiert das Panel."""
        super().__init__(parent)
        self.main_app = main_app
        self._erstelle_ui()
    
    def _erstelle_ui(self):
        """Erstellt die UI-Elemente für das Panel."""
        # Erklärung für die Anwendung
        self.erklaerung_titel = ctk.CTkLabel(self, 
                                          text="Was macht dieses Programm?",
                                          font=ctk.CTkFont(size=16, weight="bold"))
        self.erklaerung_titel.pack(anchor="w", padx=15, pady=(15, 5))
        
        erklaerung_text = (
            "Dieses Programm installiert vordefinierte Einstellungen für Adobe-Programme wie InDesign, "
            "Photoshop und Illustrator. Diese Einstellungen sind speziell auf professionelle "
            "Druckanforderungen abgestimmt und sorgen für beste Druckergebnisse.\n\n"
            "Mit einem Klick werden alle nötigen Dateien an den richtigen Stellen auf Ihrem System installiert:"
        )
        
        self.erklaerung_label = ctk.CTkLabel(self, 
                                          text=erklaerung_text,
                                          font=ctk.CTkFont(size=13),
                                          justify="left",
                                          wraplength=440)
        self.erklaerung_label.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Liste der installierten Dateien
        dateien_text = (
            "• Adobe PDF-Exporteinstellungen (.joboptions)\n"
            "• Farbeinstellungen für Adobe-Programme (.csf)\n"
            "• ICC-Farbprofile für professionellen Druck (.icc)"
        )
        
        self.dateien_label = ctk.CTkLabel(self,
                                       text=dateien_text,
                                       font=ctk.CTkFont(size=13),
                                       justify="left")
        self.dateien_label.pack(anchor="w", padx=25, pady=(0, 15))
        
        # Erklärung für die Listbox
        self.info_label = ctk.CTkLabel(self, 
                                      text="Bitte wählen Sie die gewünschten Einstellungen:",
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      anchor="w")
        self.info_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        # Hilfetext für die Mehrfachauswahl
        self.help_label = ctk.CTkLabel(self, 
                                     text="• Mit Strg-Taste (Win) oder Cmd-Taste (Mac): Mehrere auswählen\n"
                                     "• Mit der Shift-Taste: Bereich auswählen",
                                     text_color="gray60",
                                     font=ctk.CTkFont(size=12),
                                     justify="left",
                                     anchor="w")
        self.help_label.pack(padx=15, pady=(0, 5), anchor="w")
        
        # Frame für die Listbox
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(padx=15, pady=5, fill="both", expand=True)
        
        # Einstellungen Listbox (Standard-Tkinter, da CTk keine Listbox hat)
        self.einstellungs_liste = tk.Listbox(self.list_frame, height=12, selectmode=tk.MULTIPLE,
                                          font=("Segoe UI", 13), 
                                          activestyle="none",
                                          bg="#F9F9F9", fg="#333333",
                                          selectbackground="#3B8ED0", selectforeground="white")
        self.einstellungs_liste.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Scrollbar für die Listbox
        self.scrollbar = ctk.CTkScrollbar(self.list_frame, command=self.einstellungs_liste.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.einstellungs_liste.config(yscrollcommand=self.scrollbar.set)
        
        # Button-Row für Auswahloperationen
        self.button_row = ctk.CTkFrame(self, fg_color="transparent")
        self.button_row.pack(fill="x", padx=15, pady=(5, 15))
        
        # Buttons für Auswahl (nebeneinander)
        self.alle_button = ctk.CTkButton(self.button_row, text="Alle auswählen", 
                                       command=self.alle_auswaehlen,
                                       width=200,
                                       font=ctk.CTkFont(size=13))
        self.alle_button.pack(side="left", padx=(0, 5))
        
        self.keine_button = ctk.CTkButton(self.button_row, text="Auswahl aufheben", 
                                        command=self.keine_auswaehlen,
                                        fg_color="gray70", hover_color="gray50",
                                        width=200,
                                        font=ctk.CTkFont(size=13))
        self.keine_button.pack(side="right")
        
        # Installieren-Button
        self.install_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.install_button_frame.pack(fill="x", padx=15, pady=(10, 15))
        
        self.install_button = ctk.CTkButton(self.install_button_frame, 
                                          text="Ausgewählte Einstellungen installieren", 
                                          command=self.installiere_einstellungen,
                                          font=ctk.CTkFont(size=15, weight="bold"),
                                          height=45,
                                          fg_color="#2B7D2B", hover_color="#246A24")
        self.install_button.pack(fill="x")
    
    def lade_einstellungen(self, einstellungen_daten):
        """
        Lädt die Einstellungen in die Listbox.
        
        Args:
            einstellungen_daten (list): Liste der Einstellungen
        """
        # Listbox leeren
        self.einstellungs_liste.delete(0, tk.END)
        
        # Neue Einstellungen hinzufügen
        for einstellung in einstellungen_daten:
            self.einstellungs_liste.insert(tk.END, einstellung["Name"])
        
        # Handler für Listenauswahl einrichten
        self.einstellungs_liste.bind('<<ListboxSelect>>', self.on_einstellung_selected)
    
    def alle_auswaehlen(self):
        """Wählt alle Einstellungen in der Listbox aus."""
        self.einstellungs_liste.select_set(0, tk.END)
        # Nach der Auswahl Event auslösen, um Beschreibung zu aktualisieren
        self.on_einstellung_selected(None)
    
    def keine_auswaehlen(self):
        """Hebt alle Auswahlen in der Listbox auf."""
        self.einstellungs_liste.selection_clear(0, tk.END)
        # Nach dem Aufheben der Auswahl Event auslösen, um Beschreibung zurückzusetzen
        self.on_einstellung_selected(None)
    
    def on_einstellung_selected(self, event):
        """
        Handler für die Auswahl in der Listbox.
        
        Args:
            event: Das Event-Objekt (kann None sein)
        """
        # Ausgewählte Einstellungen an das Hauptfenster weitergeben, um die Beschreibung zu aktualisieren
        selection = self.einstellungs_liste.curselection()
        if selection:
            selected_index = selection[0]
            selected_name = self.einstellungs_liste.get(selected_index)
            self.main_app.right_panel.zeige_beschreibung(selected_name, selected_index, selection)
        else:
            self.main_app.right_panel.zeige_beschreibung(None, None, None)
    
    def installiere_einstellungen(self):
        """Startet die Installation der ausgewählten Einstellungen."""
        ausgewaehlte_indices = self.einstellungs_liste.curselection()
        if not ausgewaehlte_indices:
            tk.messagebox.showwarning("Hinweis", "Bitte wählen Sie mindestens eine Einstellung aus.")
            return
        
        # Ausgewählte Einstellungen ermitteln
        ausgewaehlte_einstellungen = [self.einstellungs_liste.get(index) for index in ausgewaehlte_indices]
        
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
            self.install_button.configure(state=state, text="Ausgewählte Einstellungen installieren")