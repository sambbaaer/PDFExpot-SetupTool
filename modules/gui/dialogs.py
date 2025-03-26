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
    dialog.geometry("680x550")  # Optimierte Größe im Apple-Stil
    dialog.transient(parent)  # Dialog gehört zum Hauptfenster
    dialog.grab_set()  # Modal machen
    
    # Zentrieren des Dialogs auf dem Bildschirm
    dialog.update_idletasks()
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width - 680) // 2
    y = (screen_height - 550) // 2
    dialog.geometry(f"680x550+{x}+{y}")
    
    # Hauptcontainer
    main_frame = ctk.CTkFrame(dialog, fg_color="#F5F5F7", corner_radius=0)
    main_frame.pack(fill="both", expand=True)
    
    # Inhalt mit Abstand
    content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Header im Apple-Stil
    header_frame = ctk.CTkFrame(content_frame, fg_color="transparent", height=60)
    header_frame.pack(fill="x", pady=(0, 20))
    
    # Erfolgs-Icon (im Apple-Stil) - Grüner Kreis mit Häkchen
    success_frame = ctk.CTkFrame(header_frame, width=60, height=60, corner_radius=30, fg_color="#34C759")
    success_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Das Häkchen
    success_label = ctk.CTkLabel(success_frame, text="✓", font=ctk.CTkFont(size=32), text_color="#FFFFFF")
    success_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # Titel im Apple-Stil (zentriert)
    title_label = ctk.CTkLabel(
        content_frame, 
        text=titel, 
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#000000"
    )
    title_label.pack(pady=(0, 5))
    
    # Kurze Beschreibung
    subtitle_label = ctk.CTkLabel(
        content_frame, 
        text="Die Installation wurde erfolgreich abgeschlossen. Hier finden Sie die Details:", 
        font=ctk.CTkFont(size=13),
        text_color="#666666"
    )
    subtitle_label.pack(pady=(0, 20))
    
    # TabView für die verschiedenen Inhalte
    tab_view = ctk.CTkTabview(
        content_frame, 
        width=640, 
        height=330,
        fg_color="#FFFFFF",
        segmented_button_fg_color="#F5F5F7",
        segmented_button_selected_color="#FFFFFF",
        segmented_button_selected_hover_color="#F5F5F7",
        segmented_button_unselected_color="#F5F5F7",
        segmented_button_unselected_hover_color="#E5E5EA",
        text_color="#000000"
    )
    tab_view.pack(fill="both", expand=True)
    
    # Tabs erstellen
    details_tab = tab_view.add("Installationsdetails")
    bridge_tab = tab_view.add("Adobe Bridge Anleitung")
    
    # Tab 1: Installationsdetails
    details_frame = ctk.CTkScrollableFrame(
        details_tab, 
        fg_color="transparent",
        scrollbar_fg_color="#E5E5EA",
        scrollbar_button_color="#BABABA",
        scrollbar_button_hover_color="#999999"
    )
    details_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Text mit den Installationsdetails
    details_text = ctk.CTkTextbox(
        details_frame, 
        font=ctk.CTkFont(size=13),
        text_color="#333333",
        fg_color="transparent",
        border_width=0,
        wrap="word"
    )
    details_text.pack(fill="both", expand=True)
    details_text.insert("1.0", bericht)
    details_text.configure(state="disabled")  # Schreibschutz
    
    # Tab 2: Adobe Bridge Anleitung
    bridge_frame = ctk.CTkScrollableFrame(
        bridge_tab, 
        fg_color="transparent",
        scrollbar_fg_color="#E5E5EA",
        scrollbar_button_color="#BABABA",
        scrollbar_button_hover_color="#999999"
    )
    bridge_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Anleitung für Adobe Bridge - Einleitung
    intro_label = ctk.CTkLabel(
        bridge_frame, 
        text="Farbeinstellungen mit Adobe Bridge synchronisieren",
        font=ctk.CTkFont(size=15, weight="bold"),
        text_color="#000000",
        anchor="w"
    )
    intro_label.pack(fill="x", pady=(0, 5))
    
    intro_text = ctk.CTkLabel(
        bridge_frame,
        text="Damit Ihre Farben in allen Adobe-Programmen gleich aussehen, sollten Sie die Farbeinstellungen synchronisieren:",
        font=ctk.CTkFont(size=13),
        text_color="#333333",
        wraplength=620,
        justify="left",
        anchor="w"
    )
    intro_text.pack(fill="x", pady=(0, 15))
    
    # Schritte im Apple-Design-Stil
    steps = [
        {
            "title": "Schritt 1: Adobe Bridge öffnen",
            "content": "Öffnen Sie Adobe Bridge über das Startmenü oder aus einem Adobe-Programm heraus über 'Datei > Durchsuchen in Bridge'."
        },
        {
            "title": "Schritt 2: Farbeinstellungen aufrufen",
            "content": "Klicken Sie im Menü auf 'Bearbeiten' (Windows) oder 'Bridge' (Mac) und wählen Sie 'Creative Cloud-Einstellungen > Farbeinstellungen...'."
        },
        {
            "title": "Schritt 3: Einstellung auswählen",
            "content": "Wählen Sie die passende Einstellung aus der Liste:\n• Printex - coated: Für gestrichenes Papier (glänzend)\n• Printex - uncoated: Für ungestrichenes Papier (Naturpapier)\n\nAktivieren Sie das Kontrollkästchen 'Alle Creative Cloud-Anwendungen synchronisieren'."
        },
        {
            "title": "Schritt 4: Anwenden und bestätigen",
            "content": "Klicken Sie auf 'Anwenden'. Sie erhalten eine Bestätigung, dass die Einstellungen in allen Adobe-Programmen synchronisiert wurden."
        }
    ]
    
    # Jeden Schritt hinzufügen
    for i, step in enumerate(steps):
        # Container für jeden Schritt
        step_frame = ctk.CTkFrame(bridge_frame, fg_color="#F8F8F8", corner_radius=6)
        step_frame.pack(fill="x", pady=(0, 10))
        
        # Titel des Schritts
        step_title = ctk.CTkLabel(
            step_frame, 
            text=step["title"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000",
            anchor="w"
        )
        step_title.pack(fill="x", padx=15, pady=(10, 5))
        
        # Inhalt des Schritts
        step_content = ctk.CTkLabel(
            step_frame, 
            text=step["content"],
            font=ctk.CTkFont(size=13),
            text_color="#333333",
            wraplength=580,
            justify="left",
            anchor="w"
        )
        step_content.pack(fill="x", padx=15, pady=(0, 10))
    
    # Hinweis für Nutzer ohne Bridge
    note_frame = ctk.CTkFrame(bridge_frame, fg_color="#FFF7ED", corner_radius=6)
    note_frame.pack(fill="x", pady=(0, 5))
    
    note_label = ctk.CTkLabel(
        note_frame, 
        text="Hinweis: Falls Sie Adobe Bridge nicht installiert haben, müssen Sie die Farbeinstellungen in jedem Adobe-Programm einzeln unter 'Bearbeiten > Farbeinstellungen' auswählen.",
        font=ctk.CTkFont(size=13, slant="italic"),
        text_color="#9A3412",
        wraplength=580,
        justify="left"
    )
    note_label.pack(fill="x", padx=15, pady=10)
    
    # Schließen-Button im macOS-Stil
    close_button = ctk.CTkButton(
        content_frame, 
        text="Schließen",
        command=dialog.destroy,
        width=120,
        height=32,
        fg_color="#007AFF",  # Apple Blau
        hover_color="#0062CC",
        corner_radius=6,
        border_width=0,
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#FFFFFF"
    )
    close_button.pack(pady=(15, 0))


def zeige_info_dialog(parent):
    """
    Zeigt einen Dialog mit Informationen zur Anwendung an.
    
    Args:
        parent (ctk.CTk): Elternelement des Dialogs
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Über PDF-Export Einstellungen")
    dialog.geometry("480x440")  # Optimierte Größe im Apple-Stil
    dialog.transient(parent)
    dialog.grab_set()
    
    # Zentrieren des Dialogs
    dialog.update_idletasks()
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width - 480) // 2
    y = (screen_height - 440) // 2
    dialog.geometry(f"480x440+{x}+{y}")
    
    # Hauptrahmen mit typischem Apple-Grau
    main_frame = ctk.CTkFrame(dialog, fg_color="#F5F5F7", corner_radius=0)
    main_frame.pack(fill="both", expand=True)
    
    # Inhaltsbereich
    content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # App-Icon im Apple-Stil (runder Rahmen)
    icon_frame = ctk.CTkFrame(content_frame, width=80, height=80, corner_radius=20, fg_color="#FF3B30")
    icon_frame.pack(pady=(0, 15))
    
    # Icon-Inhalt (PDF-Text)
    icon_label = ctk.CTkLabel(icon_frame, text="PDF", font=ctk.CTkFont(size=22, weight="bold"), text_color="#FFFFFF")
    icon_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # App-Name und Version
    title_label = ctk.CTkLabel(
        content_frame, 
        text="PDF-Export Einstellungen", 
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#000000"
    )
    title_label.pack(pady=(0, 5))
    
    version_label = ctk.CTkLabel(
        content_frame, 
        text="Version 1.0", 
        font=ctk.CTkFont(size=13),
        text_color="#666666"
    )
    version_label.pack(pady=(0, 20))
    
    # App-Info im Apple-Stil (weißer Rahmen mit abgerundeten Ecken)
    info_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF", corner_radius=10)
    info_frame.pack(fill="both", expand=True)
    
    # Info-Text
    info_text = (
        "Dieses Programm installiert vordefinierte Einstellungen für Adobe-Programme und gewährleistet "
        "konsistente, professionelle Druckergebnisse.\n\n"
        "Es installiert folgende Dateitypen an den korrekten Systemorten:\n"
        "• Adobe PDF-Exporteinstellungen (.joboptions)\n"
        "• Farbeinstellungen für Adobe-Programme (.csf)\n"
        "• ICC-Farbprofile (.icc)\n\n"
        "Copyright © 2025 sambbaer\n"
        "Veröffentlicht unter der MIT-Lizenz"
    )
    
    # Scrollbarer Textbereich für Info
    info_text_box = ctk.CTkTextbox(
        info_frame, 
        font=ctk.CTkFont(size=13),
        text_color="#333333",
        fg_color="#FFFFFF",
        border_width=0,
        wrap="word"
    )
    info_text_box.pack(fill="both", expand=True, padx=15, pady=15)
    info_text_box.insert("1.0", info_text)
    info_text_box.configure(state="disabled")  # Schreibschutz
    
    # Schließen-Button
    close_button = ctk.CTkButton(
        content_frame, 
        text="Schließen",
        command=dialog.destroy,
        width=120,
        height=32,
        fg_color="#007AFF",  # Apple Blau
        hover_color="#0062CC",
        corner_radius=6,
        border_width=0,
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#FFFFFF"
    )
    close_button.pack(pady=(15, 0))


def zeige_hilfe_dialog(parent):
    """
    Zeigt einen Dialog mit Hilfe zur Anwendung an.
    
    Args:
        parent (ctk.CTk): Elternelement des Dialogs
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Hilfe")
    dialog.geometry("500x560")  # Optimierte Größe im Apple-Stil
    dialog.transient(parent)
    dialog.grab_set()
    
    # Zentrieren des Dialogs
    dialog.update_idletasks()
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width - 500) // 2
    y = (screen_height - 560) // 2
    dialog.geometry(f"500x560+{x}+{y}")
    
    # Hauptcontainer
    main_frame = ctk.CTkFrame(dialog, fg_color="#F5F5F7", corner_radius=0)
    main_frame.pack(fill="both", expand=True)
    
    # Inhalt mit Abstand
    content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Titel
    title_label = ctk.CTkLabel(
        content_frame, 
        text="Hilfe & Anleitung", 
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#000000"
    )
    title_label.pack(pady=(0, 5))
    
    subtitle_label = ctk.CTkLabel(
        content_frame, 
        text="Eine kurze Einführung zur Verwendung dieser Anwendung", 
        font=ctk.CTkFont(size=13),
        text_color="#666666"
    )
    subtitle_label.pack(pady=(0, 15))
    
    # Hilfethemen im Apple-Stil
    help_topics = [
        {
            "title": "Einstellungen auswählen",
            "content": "Aktivieren Sie die Kontrollkästchen bei den Einstellungen, die Sie installieren möchten. "
                      "Sie können einzelne oder mehrere Einstellungen auswählen."
        },
        {
            "title": "Installation starten",
            "content": "Klicken Sie auf den blauen 'Einstellungen installieren' Button, um die ausgewählten "
                      "Einstellungen zu installieren. Nach Abschluss erhalten Sie eine Bestätigung."
        },
        {
            "title": "Farbeinstellungen synchronisieren",
            "content": "Für eine konsistente Farbdarstellung in allen Adobe-Programmen sollten Sie "
                      "Adobe Bridge verwenden. Nach der Installation werden Sie eine Anleitung dazu sehen."
        },
        {
            "title": "Verwendung der Einstellungen",
            "content": "In Adobe InDesign finden Sie die PDF-Exporteinstellungen unter 'Datei > Exportieren > Adobe PDF'. "
                      "Die Farbeinstellungen sind in allen Adobe-Programmen unter 'Bearbeiten > Farbeinstellungen' verfügbar."
        },
        {
            "title": "Gestrichenes vs. ungestrichenes Papier",
            "content": "• Gestrichenes Papier (coated): Für glänzende oder matte Drucksorten wie Hochglanzmagazine, Prospekte\n"
                      "• Ungestrichenes Papier (uncoated): Für Naturpapiere wie Büropapier, Zeitungspapier, Visitenkarten"
        }
    ]
    
    # Scrollbarer Bereich für alle Hilfethemen
    help_scroll = ctk.CTkScrollableFrame(
        content_frame, 
        fg_color="transparent",
        scrollbar_fg_color="#E5E5EA",
        scrollbar_button_color="#BABABA",
        scrollbar_button_hover_color="#999999"
    )
    help_scroll.pack(fill="both", expand=True, pady=(0, 15))
    
    # Jedes Hilfethema hinzufügen
    for topic in help_topics:
        # Container für das Thema
        topic_frame = ctk.CTkFrame(help_scroll, fg_color="#FFFFFF", corner_radius=10)
        topic_frame.pack(fill="x", pady=(0, 10), padx=3)
        
        # Titel des Themas
        topic_title = ctk.CTkLabel(
            topic_frame, 
            text=topic["title"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000",
            anchor="w"
        )
        topic_title.pack(fill="x", padx=15, pady=(10, 5))
        
        # Inhalt des Themas
        topic_content = ctk.CTkLabel(
            topic_frame, 
            text=topic["content"],
            font=ctk.CTkFont(size=13),
            text_color="#333333",
            wraplength=440,
            justify="left",
            anchor="w"
        )
        topic_content.pack(fill="x", padx=15, pady=(0, 10))
    
    # Schließen-Button
    close_button = ctk.CTkButton(
        content_frame, 
        text="Schließen",
        command=dialog.destroy,
        width=120,
        height=32,
        fg_color="#007AFF",  # Apple Blau
        hover_color="#0062CC",
        corner_radius=6,
        border_width=0,
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#FFFFFF"
    )
    close_button.pack(pady=(0, 0))