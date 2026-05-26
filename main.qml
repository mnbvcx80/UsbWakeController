import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Kirigami.ApplicationWindow {
    id: root
    title: "USB Vekkings-behandler"
    width: 500
    height: 600

    pageStack.initialPage: Kirigami.ScrollablePage {
        title: "USB-enheter for oppvåkning"

        // Button to reload
        actions: [
            Kirigami.Action {
                icon.name: "view-refresh"
                text: "Oppdater"
                onTriggered: usbBackend.scan_usb_devices()
            }
        ]

        Kirigami.CardsListView {
            model: usbBackend.usbModel

            delegate: Kirigami.AbstractCard {
                contentItem: RowLayout {
                    spacing: 15

                    Kirigami.Icon {
                        source: deviceId === "Systemkontroller" ? "computer" : "input-mouse"
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
                            // Vi sender stien til enheten og den nye statusen til Python
                            usbBackend.toggleWakeup(devicePath, checked)
                        }
                    }
                }
            }
        }
    }
}
