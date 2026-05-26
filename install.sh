#!/bin/bash

# Sjekk om skriptet kjøres som root
if [ "$EUID" -ne 0 ]; then
  echo "Vennligst kjør installasjonsskriptet med sudo: sudo ./install.sh"
  exit 1
fi

echo "Installerer USB Wakeup Manager..."

# 1. Opprett mappe for app-filene og kopier dem
mkdir -p /usr/local/share/usb-wakeup-manager
cp src/main.py /usr/local/share/usb-wakeup-manager/
cp src/main.qml /usr/local/share/usb-wakeup-manager/

# 2. Installer Polkit-helperen og gjør den kjørebar
cp polkit/usb-wakeup-helper.py /usr/local/bin/
chmod +x /usr/local/bin/usb-wakeup-helper.py

# 3. Installer Polkit-policyfilen
cp polkit/org.kde.usbwakemanager.policy /usr/share/polkit-1/actions/

# 4. Installer snarveien til startmenyen
cp org.kde.usbwakemanager.desktop /usr/share/applications/

echo "Installasjonen er fullført! Du finner nå appen i startmenyen din."
