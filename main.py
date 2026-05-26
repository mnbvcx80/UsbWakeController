import os
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Property, QAbstractListModel, QModelIndex, Qt

class USBListModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    IdRole = Qt.UserRole + 2
    StatusRole = Qt.UserRole + 3
    PathRole = Qt.UserRole + 4

    def __init__(self, parent=None):
        super().__init__(parent)
        self.devices = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.devices)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.devices)):
            return None

        device = self.devices[index.row()]
        if role == self.NameRole:
            return device['name']
        elif role == self.IdRole:
            return device['id']
        elif role == self.StatusRole:
            return device['status'] == "enabled"
        elif role == self.PathRole:
            return device['path']
        return None

    def roleNames(self):
        return {
            self.NameRole: b"deviceName",
            self.IdRole: b"deviceId",
            self.StatusRole: b"wakeupEnabled",
            self.PathRole: b"devicePath"
        }

    def update_devices(self, new_devices):
        self.beginResetModel()
        self.devices = new_devices
        self.endResetModel()


class USBBackend(QObject):
    def __init__(self):
        super().__init__()
        self._model = USBListModel()
        self.scan_usb_devices()

    @Property(QObject, constant=True)
    def usbModel(self):
        return self._model

    @Slot()
    def scan_usb_devices(self):
        """Skanner sysfs etter USB-enheter."""
        found_devices = []
        base_path = "/sys/bus/usb/devices"

        if not os.path.exists(base_path):
            return

        for device_dir in os.listdir(base_path):
            full_path = os.path.join(base_path, device_dir)
            wakeup_file = os.path.join(full_path, "power", "wakeup")
            product_file = os.path.join(full_path, "product")
            id_vendor_file = os.path.join(full_path, "idVendor")
            id_product_file = os.path.join(full_path, "idProduct")

            if os.path.exists(wakeup_file):
                name = "Ukjent enhet"
                if os.path.exists(product_file):
                    with open(product_file, "r") as f:
                        name = f.read().strip()

                if not name or "root hub" in name.lower():
                    continue

                usb_id = "Systemkontroller"
                if os.path.exists(id_vendor_file) and os.path.exists(id_product_file):
                    with open(id_vendor_file, "r") as f:
                        vid = f.read().strip()
                    with open(id_product_file, "r") as f:
                        pid = f.read().strip()
                    usb_id = f"{vid}:{pid}"

                with open(wakeup_file, "r") as f:
                    status = f.read().strip()

                found_devices.append({
                    "name": name,
                    "id": usb_id,
                    "status": status,
                    "path": full_path
                })

        self._model.update_devices(found_devices)

    @Slot(str, bool)
    def toggleWakeup(self, path, enabled):
        status = "enabled" if enabled else "disabled"
        print(f"Mottok ønske om å endre {path} til {status}")

        # Vi bruker pkexec for å kjøre helper-skriptet vårt med Polkit-rettigheter
        import subprocess
        cmd = ["pkexec", "/usr/local/bin/usb-wakeup-helper.py", path, status]

        try:
            # Kjører kommandoen i bakgrunnen
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("Endring utført i systemet.")
            else:
                print(f"Polkit-feil: {result.stderr}")
                # Tips: Her kan du i fremtiden trigge en feilmelding i QML-grensesnittet
                # slik at bryteren flipper tilbake hvis brukeren avbrøt passord-dialogen.
        except Exception as e:
            print(f"Kunne ikke kjøre Polkit-helper: {e}")

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    backend = USBBackend()
    engine.rootContext().setContextProperty("usbBackend", backend)

    # Finn QML-filen i samme mappe
    qml_file = os.path.join(os.path.dirname(__file__), "main.qml")
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
