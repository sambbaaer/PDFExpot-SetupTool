"""
Dialog-Modul für PDF-Export-Einstellungen-Installer

Dieses Modul enthält die Dialog-Fenster, die in der Anwendung verwendet werden.
"""

import customtkinter as ctk
from tkinter import messagebox
import os


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
    
    # Container mit Rand
    main_frame = ctk.CTkFrame(dialog, fg_color="#F8F9FA")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Erfolgs-Icon (Grüner Haken) - hier würde normalerweise ein Bild stehen
    success_label = ctk.CTkLabel(main_frame, text="✅", font=ctk.CTkFont(size=36), text_color="#16A34A")
    success_label.pack(pady=(20, 0))
    
    # Headline für den Dialog
    headline = ctk.CTkLabel(main_frame, text=titel, 
                           font=ctk.CTkFont(size=22, weight="bold"),
                           text_color="#1E40AF")
    headline.pack(pady=(5, 5))
    
    # Unterüberschrift
    subheading = ctk.CTkLabel(main_frame, text="Details zur Installation", 
                            font=ctk.CTkFont(size=14),
                            text_color="#4B5563")
    subheading.pack(pady=(0, 15))
    
    # Trennlinie
    separator = ctk.CTkFrame(main_frame, height=1, fg_color="#E5E7EB")
    separator.pack(fill="x", padx=20, pady=(0, 15))
    
    # Scrollbarer Textbereich für den Bericht
    text_frame = ctk.CTkScrollableFrame(main_frame, width=660, height=280, fg_color="#FFFFFF", corner_radius=6)
    text_frame.pack(padx=20, pady=0, fill="both", expand=True)
    
    # Text mit den Installationsdetails
    details_text = ctk.CTkLabel(text_frame, text=bericht, 
                              font=ctk.CTkFont(size=13),
                              justify="left",
                              text_color="#374151",
                              wraplength=640)
    details_text.pack(padx=10, pady=10, anchor="w")
    
    # Button-Frame
    button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    button_frame.pack(fill="x", pady=(15, 5))
    
    # Schließen-Button
    close_button = ctk.CTkButton(button_frame, text="Schließen", 
                                command=dialog.destroy,
                                width=200,
                                fg_color="#3B82F6", 
                                hover_color="#2563EB",
                                corner_radius=6)
    close_button.pack(pady=0)


def zeige_info_dialog(parent):
    """
    Zeigt einen Dialog mit Informationen zur Anwendung an.
    
    Args:
        parent (ctk.CTk): Elternelement des Dialogs
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Über PDF-Export Einstellungen Installer")
    dialog.geometry("500x480")
    dialog.transient(parent)
    dialog.grab_set()
    
    # Zentrieren des Dialogs
    dialog.update_idletasks()
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width - 500) // 2
    y = (screen_height - 480) // 2
    dialog.geometry(f"500x480+{x}+{y}")
    
    # Container mit Rand
    main_frame = ctk.CTkFrame(dialog, fg_color="#F8F9FA")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Logo/Icon Bereich
    try:
        # SVG-Logo-Pfad
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))), "links", "Icon.svg")
                
        # Wenn kein Logo gefunden wird, nur Text anzeigen
        if not os.path.exists(logo_path):
            logo_label = ctk.CTkLabel(main_frame, text="🖨️", 
                                   font=ctk.CTkFont(size=48),
                                   text_color="#3B82F6")
            logo_label.pack(pady=(20, 0))
        else:
            # Hier könnte ein Logo geladen werden, wenn verfügbar
            logo_label = ctk.CTkLabel(main_frame, text="🖨️", 
                                   font=ctk.CTkFont(size=48),
                                   text_color="#3B82F6")
            logo_label.pack(pady=(20, 0))
    except Exception:
        # Fallback zu reinem Text
        logo_label = ctk.CTkLabel(main_frame, text="🖨️", 
                               font=ctk.CTkFont(size=48),
                               text_color="#3B82F6")
        logo_label.pack(pady=(20, 0))
    
    # Info-Inhalt
    title_label = ctk.CTkLabel(main_frame, text="PDF-Export Einstellungen", 
                             font=ctk.CTkFont(size=24, weight="bold"),
                             text_color="#1E40AF")
    title_label.pack(pady=(5, 5))
    
    version_label = ctk.CTkLabel(main_frame, text="Version 1.0.0", 
                               font=ctk.CTkFont(size=14),
                               text_color="#6B7280")
    version_label.pack(pady=(0, 15))
    
    # Trennlinie
    separator = ctk.CTkFrame(main_frame, height=1, fg_color="#E5E7EB")
    separator.pack(fill="x", padx=20, pady=(0, 15))
    
    # Scrollbare Textbox für Informationen
    info_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#FFFFFF", corner_radius=6)
    info_frame.pack(padx=20, pady=0, fill="both", expand=True)
    
    info_text = (
        "Dieses Programm installiert vordefinierte Einstellungen für Adobe-Programme.\n\n"
        "Es installiert automatisch drei Arten von Dateien:\n"
        "• Adobe PDF-Exporteinstellungen (.joboptions)\n"
        "• Farbeinstellungen für Adobe-Programme (.csf)\n"
        "• ICC-Farbprofile für professionellen Druck (.icc)\n\n"
        "Diese Einstellungen gewährleisten konsistente und professionelle Druckergebnisse "
        "in allen Ihren Adobe-Anwendungen.\n\n"
        "Copyright © 2025 sambbaer\n"
        "Veröffentlicht unter der MIT-Lizenz"
    )
    
    info_label = ctk.CTkLabel(info_frame, text=info_text, 
                            font=ctk.CTkFont(size=13),
                            justify="left",
                            text_color="#374151",
                            wraplength=440)
    info_label.pack(padx=15, pady=15, fill="both")
    
    # Button-Frame
    button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    button_frame.pack(fill="x", pady=(15, 5))
    
    # Schließen-Button
    close_button = ctk.CTkButton(button_frame, text="Schließen", 
                                command=dialog.destroy,
                                width=200,
                                fg_color="#3B82F6", 
                                hover_color="#2563EB",
                                corner_radius=6)
    close_button.pack(pady=0)


def zeige_hilfe_dialog(parent):
    """
    Zeigt einen Dialog mit Hilfe zur Anwendung an.
    
    Args:
        parent (ctk.CTk): Elternelement des Dialogs
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Hilfe & Anleitung")
    dialog.geometry("550x550")
    dialog.transient(parent)
    dialog.grab_set()
    
    # Zentrieren des Dialogs
    dialog.update_idletasks()
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width - 550) // 2
    y = (screen_height - 550) // 2
    dialog.geometry(f"550x550+{x}+{y}")
    
    # Container mit Rand
    main_frame = ctk.CTkFrame(dialog, fg_color="#F8F9FA")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Icon
    help_icon = ctk.CTkLabel(main_frame, text="❓", font=ctk.CTkFont(size=36), text_color="#8B5CF6")
    help_icon.pack(pady=(20, 0))
    
    # Hilfe-Überschrift
    title_label = ctk.CTkLabel(main_frame, text="Hilfe & Anleitung", 
                             font=ctk.CTkFont(size=22, weight="bold"),
                             text_color="#6D28D9")
    title_label.pack(pady=(5, 5))
    
    # Unterüberschrift
    subtitle_label = ctk.CTkLabel(main_frame, text="So verwenden Sie die Anwendung", 
                             font=ctk.CTkFont(size=14),
                             text_color="#4B5563")
    subtitle_label.pack(pady=(0, 15))
    
    # Trennlinie
    separator = ctk.CTkFrame(main_frame, height=1, fg_color="#E5E7EB")
    separator.pack(fill="x", padx=20, pady=(0, 15))
    
    # Scrollbarer Inhalt
    help_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#FFFFFF", corner_radius=6)
    help_frame.pack(padx=20, pady=0, fill="both", expand=True)
    
    # Formatierter Hilfetext mit Abschnitten
    help_sections = [
        {
            "title": "1. Einstellungen auswählen",
            "content": (
                "• Einzelne Einstellung: Direkt anklicken\n"
                "• Mehrere Einstellungen: Mit Strg-Taste (Windows) oder Cmd-Taste (Mac)\n"
                "• Bereich auswählen: Mit der Shift-Taste"
            )
        },
        {
            "title": "2. Beschreibung lesen",
            "content": (
                "• Die Beschreibung der ausgewählten Einstellung wird rechts angezeigt\n"
                "• Bei Mehrfachauswahl wird nur die Beschreibung der ersten Einstellung angezeigt"
            )
        },
        {
            "title": "3. Installation starten",
            "content": (
                "• Klicken Sie auf 'Ausgewählte Einstellungen installieren'\n"
                "• Die ausgewählten Einstellungen werden an den richtigen Stellen installiert\n"
                "• Nach der Installation wird ein Bericht angezeigt"
            )
        },
        {
            "title": "4. Adobe Bridge",
            "content": (
                "Wenn Adobe Bridge nicht installiert ist, müssen Sie in jedem Adobe-Programm\n"
                "unter 'Bearbeiten > Farbeinstellungen' die Farbeinstellungen manuell auswählen."
            )
        },
        {
            "title": "5. Verwendung der Einstellungen",
            "content": (
                "• PDF-Exporteinstellungen: In InDesign unter 'Datei > Exportieren > Adobe PDF'\n"
                "• Farbeinstellungen: In allen Adobe-Programmen unter 'Bearbeiten > Farbeinstellungen'"
            )
        },
        {
            "title": "6. Fehlerbehebung",
            "content": (
                "Bei Problemen prüfen Sie bitte die Logdatei 'error_log.txt' im Programmverzeichnis."
            )
        }
    ]
    
    # Alle Hilfeabschnitte hinzufügen
    for i, section in enumerate(help_sections):
        # Abschnittstitel
        section_title = ctk.CTkLabel(help_frame, 
                                    text=section["title"],
                                    font=ctk.CTkFont(size=14, weight="bold"),
                                    text_color="#4F46E5",
                                    anchor="w")
        section_title.pack(padx=10, pady=(15 if i > 0 else 10, 5), anchor="w")
        
        # Abschnittsinhalt
        section_content = ctk.CTkLabel(help_frame, 
                                    text=section["content"],
                                    font=ctk.CTkFont(size=13),
                                    justify="left",
                                    text_color="#374151",
                                    anchor="w")
        section_content.pack(padx=20, pady=(0, 5), anchor="w")
    
    # Button-Frame
    button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    button_frame.pack(fill="x", pady=(15, 5))
    
    # Schließen-Button
    close_button = ctk.CTkButton(button_frame, text="Schließen", 
                                command=dialog.destroy,
                                width=200,
                                fg_color="#3B82F6", 
                                hover_color="#2563EB",
                                corner_radius=6)
    close_button.pack(pady=0)