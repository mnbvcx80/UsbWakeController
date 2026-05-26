import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Kirigami.ApplicationWindow {
    id: root
    title: "USB Wakeup Manager"
    width: 500
    height: 600

    pageStack.initialPage: Kirigami.ScrollablePage {
        title: "USB Devices for Wakeup"

        // Button to reload the device list
        actions: [
            Kirigami.Action {
                icon.name: "view-refresh"
                text: "Refresh"
                onTriggered: usbBackend.scan_usb_devices()
            }
        ]

        Kirigami.CardsListView {
            model: usbBackend.usbModel

            delegate: Kirigami.AbstractCard {
                contentItem: RowLayout {
                    spacing: 15

                    Kirigami.Icon {
                        // Matches the translated string from main.py to show the correct icon
                        source: deviceId === "System Controller" ? "computer" : "input-mouse"
                        Layout.preferredWidth: 32
                        Layout.preferredHeight: 32
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        Label {
                            text: deviceName
                            font.bold: true
                            elide: Text.ElideRight
                        }
                        Label {
                            text: "ID: " + deviceId
                            font.pointSize: 9
                            opacity: 0.6
                        }
                    }

                    Switch {
                        checked: wakeupEnabled
                        onCheckedChanged: {
                            // Pass the device path and the new toggle status to Python
                            usbBackend.toggleWakeup(devicePath, checked)
                        }
                    }
                }
            }
        }
    }
}
