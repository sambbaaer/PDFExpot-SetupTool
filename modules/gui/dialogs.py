"""
Dialog-Modul für PDF-Export-Einstellungen-Installer

Dieses Modul enthält die Dialog-Fenster, die in der Anwendung verwendet werden.
"""

import customtkinter as ctk
from tkinter import messagebox


def zeige_ergebnis_dialog(parent, titel, bericht):
    """
    Zeigt einen Dialog mit dem detaillierten Installationsbericht an.
    
    Args:
        parent (ctk.CTk): Elternelement des Dialogs
        titel (str): Titel des Dialogs
        bericht (str): Detaillierter Bericht
    """
    # Erstelle einen benutzerdefinierten Dialog
    dialog = ctk.CTkToplevel(parent)
    dialog.title(titel)
    dialog.geometry("700x500")
    dialog.transient(parent)  # Dialog gehört zum Hauptfenster
    dialog.grab_set()  # Modal machen
    
    # Zentrieren des Dialogs auf dem Bildschirm
    dialog.update_idletasks()
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width - 700) // 2
    y = (screen_height - 500) // 2
    dialog.geometry(f"700x500+{x}+{y}")
    
    # Headline für den Dialog
    headline = ctk.CTkLabel(dialog, text=titel, 
                           font=ctk.CTkFont(size=20, weight="bold"))
    headline.pack(pady=(20, 5))
    
    # Unterüberschrift
    subheading = ctk.CTkLabel(dialog, text="Details zur Installation", 
                            font=ctk.CTkFont(size=14))
    subheading.pack(pady=(0, 15))
    
    # Scrollbarer Textbereich für den Bericht
    text_frame = ctk.CTkScrollableFrame(dialog, width=660, height=350)
    text_frame.pack(padx=20, pady=10, fill="both", expand=True)
    
    # Text mit den Installationsdetails
    details_text = ctk.CTkLabel(text_frame, text=bericht, 
                              font=ctk.CTkFont(size=12),
                              justify="left",
                              wraplength=640)
    details_text.pack(padx=10, pady=10, anchor="w")
    
    # Schließen-Button
    close_button = ctk.CTkButton(dialog, text="Schließen", 
                                command=dialog.destroy,
                                width=200)
    close_button.pack(pady=(5, 20))


def zeige_info_dialog(parent):
    """
    Zeigt einen Dialog mit Informationen zur Anwendung an.
    
    Args:
        parent (ctk.CTk): Elternelement des Dialogs
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Über PDF-Export Einstellungen Installer")
    dialog.geometry("500x400")
    dialog.transient(parent)
    dialog.grab_set()
    
    # Zentrieren des Dialogs
    dialog.update_idletasks()
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width - 500) // 2
    y = (screen_height - 400) // 2
    dialog.geometry(f"500x400+{x}+{y}")
    
    # Info-Inhalt
    title_label = ctk.CTkLabel(dialog, text="PDF-Export Einstellungen", 
                             font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(pady=(20, 5))
    
    version_label = ctk.CTkLabel(dialog, text="Version 1.0.0", 
                               font=ctk.CTkFont(size=14))
    version_label.pack(pady=(0, 20))
    
    info_text = (
        "Dieses Programm installiert vordefinierte Einstellungen für Adobe-Programme.\n\n"
        "Es installiert automatisch drei Arten von Dateien:\n"
        "• Adobe PDF-Exporteinstellungen (.joboptions)\n"
        "• Farbeinstellungen für Adobe-Programme (.csf)\n"
        "• ICC-Farbprofile für professionellen Druck (.icc)\n\n"
        "Copyright © 2025 sambbaer\n"
        "Veröffentlicht unter der MIT-Lizenz"
    )
    
    info_label = ctk.CTkLabel(dialog, text=info_text, 
                            font=ctk.CTkFont(size=13),
                            justify="center",
                            wraplength=460)
    info_label.pack(pady=10, fill="both", expand=True)
    
    close_button = ctk.CTkButton(dialog, text="Schließen", 
                                command=dialog.destroy,
                                width=200)
    close_button.pack(pady=(0, 20))


def zeige_hilfe_dialog(parent):
    """
    Zeigt einen Dialog mit Hilfe zur Anwendung an.
    
    Args:
        parent (ctk.CTk): Elternelement des Dialogs
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Hilfe")
    dialog.geometry("550x480")
    dialog.transient(parent)
    dialog.grab_set()
    
    # Zentrieren des Dialogs
    dialog.update_idletasks()
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width - 550) // 2
    y = (screen_height - 480) // 2
    dialog.geometry(f"550x480+{x}+{y}")
    
    # Hilfe-Überschrift
    title_label = ctk.CTkLabel(dialog, text="Hilfe & Anleitung", 
                             font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(pady=(20, 15))
    
    # Scrollbarer Inhalt
    help_frame = ctk.CTkScrollableFrame(dialog, width=510, height=350)
    help_frame.pack(padx=20, pady=10, fill="both", expand=True)
    
    help_text = (
        "So verwenden Sie das Programm:\n\n"
        "1. Wählen Sie Einstellungen aus der Liste aus\n"
        "   - Einzelne Einstellung: Direkt anklicken\n"
        "   - Mehrere Einstellungen: Mit Strg-Taste (Windows) oder Cmd-Taste (Mac)\n"
        "   - Bereich auswählen: Mit der Shift-Taste\n\n"
        
        "2. Lesen Sie die Beschreibung\n"
        "   - Die Beschreibung der ausgewählten Einstellung wird rechts angezeigt\n"
        "   - Bei Mehrfachauswahl wird nur die Beschreibung der ersten Einstellung angezeigt\n\n"
        
        "3. Klicken Sie auf 'Ausgewählte Einstellungen installieren'\n"
        "   - Die ausgewählten Einstellungen werden an den richtigen Stellen installiert\n"
        "   - Nach der Installation wird ein Bericht angezeigt\n\n"
        
        "Weitere Informationen:\n\n"
        
        "• Adobe Bridge\n"
        "  Wenn Adobe Bridge nicht installiert ist, müssen Sie in jedem Adobe-Programm\n"
        "  unter 'Bearbeiten > Farbeinstellungen' die Farbeinstellungen manuell auswählen.\n\n"
        
        "• Verwendung der Einstellungen\n"
        "  - PDF-Exporteinstellungen: In InDesign unter 'Datei > Exportieren > Adobe PDF'\n"
        "  - Farbeinstellungen: In allen Adobe-Programmen unter 'Bearbeiten > Farbeinstellungen'\n\n"
        
        "• Fehlerbehebung\n"
        "  Bei Problemen prüfen Sie bitte die Logdatei 'error_log.txt' im Programmverzeichnis."
    )
    
    help_label = ctk.CTkLabel(help_frame, text=help_text, 
                            font=ctk.CTkFont(size=13),
                            justify="left",
                            wraplength=490)
    help_label.pack(padx=10, pady=10, anchor="w")
    
    # Schließen-Button
    close_button = ctk.CTkButton(dialog, text="Schließen", 
                                command=dialog.destroy,
                                width=200)
    close_button.pack(pady=(5, 20))