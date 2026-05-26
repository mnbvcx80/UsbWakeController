#!/usr/bin/env python3
import sys
import os

if len(sys.argv) < 3:
    print("Feil: Mangler argumenter. Bruk: helper.py <sti> <enabled|disabled>")
    sys.exit(1)

target_path = sys.argv[1]
status = sys.argv[2]

# Sikkerhetssjekk: Sørg for at stien faktisk ligger under /sys/bus/usb/devices/
if not target_path.startswith("/sys/bus/usb/devices/"):
    print("Feil: Ugyldig sti!")
    sys.exit(1)

wakeup_file = os.path.join(target_path, "power", "wakeup")

if not os.path.exists(wakeup_file):
    print("Feil: Enheten har ikke støtte for wakeup.")
    sys.exit(1)

if status not in ["enabled", "disabled"]:
    print("Feil: Status må være 'enabled' eller 'disabled'.")
    sys.exit(1)

# Skriv statusen til filen
try:
    with open(wakeup_file, "w") as f:
        f.write(status)
    print(f"Suksess: Satt {wakeup_file} til {status}")
except Exception as e:
    print(f"Feil under skriving: {e}")
    sys.exit(1)
