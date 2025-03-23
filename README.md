# PDF Export Settings Installer 🖨️ 🎨

A professional tool for automatically installing PDF export settings, color profiles, and configuration files for Adobe applications such as InDesign, Photoshop, and Illustrator.

## Features ✨

- **One-click installation** of all necessary files for professional print workflows
- **Multi-platform support** for Windows and macOS
- **Pre-configured settings** for different printing environments (coated and uncoated paper)
- **Automatic detection** of system directories for Adobe applications
- **Color management** with ICC profiles
- **Detailed descriptions** of each setting extracted from joboptions files
- **Multi-language support** for the user interface
- **Detailed installation reports** showing exactly what files were installed and where

## What Does It Install? 📦

The application installs three types of files to their correct system locations:

- **Adobe PDF export settings** (.joboptions) - For standardized PDF export configurations
- **Color settings** for Adobe applications (.csf) - For consistent color management across applications
- **ICC color profiles** for professional printing (.icc) - For accurate color representation

## Requirements 🔧

- Python 3.6 or higher
- CustomTkinter library (`pip install customtkinter`)
- Any Adobe application (InDesign, Photoshop, Illustrator, etc.)

## Installation 💻

1. Clone this repository:
   ```
   git clone https://github.com/sambbaer/pdf-export-settings-installer.git
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

## Usage 📝

1. Launch the application
2. Select one or more settings from the list
   - Use Ctrl/Cmd to select multiple items
   - Use Shift to select a range of items
3. Review the detailed description of the selected setting
4. Click "Install Selected Settings"
5. After installation, a detailed report shows what files were installed and where

## Adobe Bridge Integration 🔄

The application automatically detects if Adobe Bridge is installed. If not, it displays a warning that color settings will need to be manually selected in each Adobe application.

## Structure 🏗️

- `main.py` - Main entry point for the application
- `modules/` - Contains all the program modules:
  - `gui/` - GUI implementation with panels and dialogs
    - `base.py` - Main GUI implementation
    - `left_panel.py` - Left panel with settings list
    - `right_panel.py` - Right panel with descriptions
    - `dialogs.py` - Implementation of various dialog windows
  - `installer.py` - Core installation logic
  - `joboptions_parser.py` - Parses Adobe .joboptions files to extract readable descriptions
  - `utils.py` - Utility functions for file operations and system detection
- `resources/` - Contains the settings files to be installed
- `config/` - Configuration files:
  - `settings.json` - Defines available settings packages
  - `currentDirectories.json` - Defines system paths for different platforms

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

---

# PDF-Export Einstellungen Installer 🖨️ 🎨

Ein professionelles Tool zur automatischen Installation von PDF-Export-Einstellungen, Farbprofilen und Konfigurationsdateien für Adobe-Anwendungen wie InDesign, Photoshop und Illustrator.

## Funktionen ✨

- **Ein-Klick-Installation** aller notwendigen Dateien für professionelle Druck-Workflows
- **Multi-Plattform-Unterstützung** für Windows und macOS
- **Vorkonfigurierte Einstellungen** für verschiedene Druckumgebungen (gestrichenes und ungestrichenes Papier)
- **Automatische Erkennung** der Systemverzeichnisse für Adobe-Anwendungen
- **Professionelles Farbmanagement** mit ICC-Profilen
- **Detaillierte Beschreibungen** jeder Einstellung, extrahiert aus den joboptions-Dateien
- **Mehrsprachige Unterstützung** für die Benutzeroberfläche
- **Detaillierte Installationsberichte**, die genau zeigen, welche Dateien wo installiert wurden

## Was wird installiert? 📦

Die Anwendung installiert drei Arten von Dateien an den richtigen Systemorten:

- **Adobe PDF-Exporteinstellungen** (.joboptions) - Für standardisierte PDF-Export-Konfigurationen
- **Farbeinstellungen** für Adobe-Anwendungen (.csf) - Für konsistentes Farbmanagement über alle Anwendungen hinweg
- **ICC-Farbprofile** für professionellen Druck (.icc) - Für genaue Farbdarstellung

## Voraussetzungen 🔧

- Python 3.6 oder höher
- CustomTkinter-Bibliothek (`pip install customtkinter`)
- Eine Adobe-Anwendung (InDesign, Photoshop, Illustrator, etc.)

## Installation 💻

1. Repository klonen:
   ```
   git clone https://github.com/sambbaer/pdf-export-settings-installer.git
   ```

2. Erforderliche Pakete installieren:
   ```
   pip install -r requirements.txt
   ```

3. Anwendung starten:
   ```
   python main.py
   ```

## Verwendung 📝

1. Starten Sie die Anwendung
2. Wählen Sie eine oder mehrere Einstellungen aus der Liste
   - Verwenden Sie Strg/Cmd, um mehrere Elemente auszuwählen
   - Verwenden Sie Shift, um einen Bereich auszuwählen
3. Prüfen Sie die detaillierte Beschreibung der ausgewählten Einstellung
4. Klicken Sie auf "Ausgewählte Einstellungen installieren"
5. Nach der Installation zeigt ein detaillierter Bericht, welche Dateien wo installiert wurden

## Adobe Bridge Integration 🔄

Die Anwendung erkennt automatisch, ob Adobe Bridge installiert ist. Falls nicht, wird eine Warnung angezeigt, dass Farbeinstellungen in jeder Adobe-Anwendung manuell ausgewählt werden müssen.

## Struktur 🏗️

- `main.py` - Haupteinstiegspunkt für die Anwendung
- `modules/` - Enthält alle Programmmodule:
  - `gui/` - GUI-Implementierung mit Panels und Dialogen
    - `base.py` - Haupt-GUI-Implementierung
    - `left_panel.py` - Linkes Panel mit Einstellungsliste
    - `right_panel.py` - Rechtes Panel mit Beschreibungen
    - `dialogs.py` - Implementierung verschiedener Dialogfenster
  - `installer.py` - Kern-Installationslogik
  - `joboptions_parser.py` - Parser für Adobe .joboptions-Dateien zur Extraktion lesbarer Beschreibungen
  - `utils.py` - Hilfsfunktionen für Dateioperationen und Systemerkennung
- `resources/` - Enthält die zu installierenden Einstellungsdateien
- `config/` - Konfigurationsdateien:
  - `settings.json` - Definiert verfügbare Einstellungspakete
  - `currentDirectories.json` - Definiert Systempfade für verschiedene Plattformen

## Lizenz 📄

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die LICENSE-Datei für Details.