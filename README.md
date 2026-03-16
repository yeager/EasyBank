# EasyBank - Visuell Budgetapp

En tillgänglig budgetapp med piktogram, designad för personer med intellektuella funktionshinder.

## Funktioner

- Visuell budgetvisning med piktogram och ikoner
- Stora, tydliga knappar för enkel navigering
- Färgkodad saldovisning (grön/orange/röd)
- Visuella och audiella varningar när pengarna tar slut
- Utgiftskategorier med bilder: Mat, Hem, Transport, Kläder, Nöje, Hälsa
- Svenska som huvudspråk med stöd för engelska
- Lokal datalagring i JSON-format

## Installation

### Systemkrav

- Python 3.10+
- GTK4
- libadwaita

### macOS

```bash
brew install gtk4 libadwaita pygobject3
pip install -r requirements.txt
```

### Ubuntu/Debian

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1
pip install -r requirements.txt
```

### Fedora

```bash
sudo dnf install python3-gobject gtk4 libadwaita
pip install -r requirements.txt
```

## Användning

```bash
# Kör direkt
python -m easybank

# Eller installera och kör
pip install .
easybank
```

## Projektstruktur

```
EasyBank/
├── easybank/
│   ├── __init__.py      # Paketdefinition
│   ├── __main__.py      # Entry point
│   ├── app.py           # Gtk.Application
│   ├── window.py        # Huvudfönster och UI
│   ├── budget.py        # Datamodell och JSON-persistens
│   └── icons.py         # Inline SVG-piktogram
├── po/
│   ├── easybank.pot     # Översättningsmall
│   └── sv/LC_MESSAGES/
│       └── easybank.po  # Svenska översättningar
├── easybank.desktop     # Desktop-integration
├── setup.py             # Paketinstallation
├── requirements.txt     # Python-beroenden
└── README.md            # Dokumentation
```

## Tillgänglighet

Appen är designad med fokus på kognitiv tillgänglighet:

- **Piktogram** istället för enbart text
- **Stora knappar** (minst 48px) för enkel interaktion
- **Färgkodning** med tydliga kontraster
- **Enkla siffror** utan decimaler
- **Visuella varningar** med ansiktsikoner (glad/ledsen)
- **Ljudvarning** när pengarna nästan tar slut

## Licens

GPL-3.0
