#!/bin/bash

# Check if the script is being run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run the installation script with sudo: sudo ./install.sh"
  exit 1
fi

echo "Installing USB Wakeup Manager..."

# 1. Create a directory for the app files and copy them
mkdir -p /usr/local/share/usb-wakeup-manager
cp src/main.py /usr/local/share/usb-wakeup-manager/
cp src/main.qml /usr/local/share/usb-wakeup-manager/

# 2. Install the Polkit helper and make it executable
cp polkit/usb-wakeup-helper.py /usr/local/bin/
chmod +x /usr/local/bin/usb-wakeup-helper.py

# 3. Install the Polkit policy file
cp polkit/org.kde.usbwakemanager.policy /usr/share/polkit-1/actions/

# 4. Install the desktop shortcut for the start menu
cp org.kde.usbwakemanager.desktop /usr/share/applications/

echo "Installation completed successfully! You can now find the app in your system menu."
