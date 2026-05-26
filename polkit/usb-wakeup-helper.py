#!/usr/bin/env python3
import sys
import os

if len(sys.argv) < 3:
    print("Error: Missing arguments. Usage: helper.py <path> <enabled|disabled>")
    sys.exit(1)

target_path = sys.argv[1]
status = sys.argv[2]

# Security check: Ensure the path is actually inside sysfs USB devices
if not target_path.startswith("/sys/bus/usb/devices/"):
    print("Error: Invalid path!")
    sys.exit(1)

wakeup_file = os.path.join(target_path, "power", "wakeup")

if not os.path.exists(wakeup_file):
    print("Error: Device does not support wakeup.")
    sys.exit(1)

if status not in ["enabled", "disabled"]:
    print("Error: Status must be 'enabled' or 'disabled'.")
    sys.exit(1)

# Write the status to the file
try:
    with open(wakeup_file, "w") as f:
        f.write(status)
    print(f"Success: Set {wakeup_file} to {status}")
except Exception as e:
    print(f"Error writing to file: {e}")
    sys.exit(1)
