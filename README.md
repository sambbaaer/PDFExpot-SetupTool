# PDF Export Settings Installer 🖨️ 🎨

A professional tool for automatically installing PDF export settings, color profiles, and configuration files for Adobe applications such as InDesign, Photoshop, and Illustrator.

## Features ✨

- **One-click installation** of all necessary files for professional print workflows
- **Multi-platform support** for Windows and macOS
- **Pre-configured settings** for different printing environments (coated and uncoated paper)
- **Automatic detection** of system directories for Adobe applications
- **Professional color management** with ICC profiles

## What Does It Install? 📦

The application installs three types of files:

- **Adobe PDF export settings** (.joboptions)
- **Color settings** for Adobe applications (.csf)
- **ICC color profiles** for professional printing (.icc)

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
3. Click "Install Selected Settings"
4. The settings will be installed to the correct locations on your system

## Structure 🏗️

- `main.py` - Main entry point for the application
- `modules/` - Contains all the program modules:
  - `gui/` - GUI implementation
  - `installer.py` - Core installation logic
  - `joboptions_parser.py` - Parses Adobe .joboptions files
  - `utils.py` - Utility functions
- `resources/` - Contains the settings files to be installed
- `config/` - Configuration files

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

## Was wird installiert? 📦

Die Anwendung installiert drei Arten von Dateien:

- **Adobe PDF-Exporteinstellungen** (.joboptions)
- **Farbeinstellungen** für Adobe-Anwendungen (.csf)
- **ICC-Farbprofile** für professionellen Druck (.icc)

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
3. Klicken Sie auf "Ausgewählte Einstellungen installieren"
4. Die Einstellungen werden an den richtigen Stellen auf Ihrem System installiert

## Struktur 🏗️

- `main.py` - Haupteinstiegspunkt für die Anwendung
- `modules/` - Enthält alle Programmmodule:
  - `gui/` - GUI-Implementierung
  - `installer.py` - Kern-Installationslogik
  - `joboptions_parser.py` - Parser für Adobe .joboptions-Dateien
  - `utils.py` - Hilfsfunktionen
- `resources/` - Enthält die zu installierenden Einstellungsdateien
- `config/` - Konfigurationsdateien

## Lizenz 📄

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die LICENSE-Datei für Details.