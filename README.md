# USB Wakeup Manager for KDE Linux (Fedora)

Et lite og enkelt grafisk verktøy skrevet i Python (PySide6) og Kirigami for å aktivere eller deaktivere hvilke USB-enheter som har lov til å vekke datamaskinen fra dvale.

## Funksjoner
- Viser en oversikt over tilkoblede USB-enheter (mus, tastatur, adaptere).
- Enkel av/på-bryter for hver enhet.
- Integrert med Polkit for sikker systemendring uten å kjøre hele appen som root.

## Forutsetninger (Fedora)
Før du installerer, må du sørge for at du har installert PySide6 og Kirigami:
```bash
sudo dnf install python3-pyside6 kf6-kirigami-devel
