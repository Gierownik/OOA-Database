import json
import os
import re

file_map = {
    "ENUM_ShellID.json": "Shells",
    "ENUM_PerkID.json": "Augments",
    "ENUM_DeviceID.json": "Devices",
    "ENUM_WeaponID.json": "Weapons",
    "ENUM_AttachmentID.json": "Attachments"
}

output = {
    "Shells": {},
    "Augments": {},
    "Devices": {},
    "Weapons": {},
    "Optics": {},
    "Ammo": {},
    "Mods": {}
}

def extract_enum_id(key_string):
    match = re.match(r"NewEnumerator(\d+)", key_string)
    return int(match.group(1)) if match else None

def categorize_attachment(name):
    if (name.endswith("Sight") or name.endswith("Sights")) and name != "Laser Sight":
        return "Optics"
    elif name.endswith("Ammo") or name.endswith("Grenade"):
        return "Ammo"
    else:
        return "Mods"

for filename, category in file_map.items():
    if not os.path.exists(filename):
        print(f"Warnin {filename} not found")
        continue

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

        entries = data[0].get("Properties", {}).get("DisplayNameMap", [])
    for entry in entries:
        key = entry.get("Key", "")
        value = entry.get("Value", {})
        name = value.get("SourceString", "").strip()

        if not name or name == "-":
            continue

        enum_id = extract_enum_id(key)
        if enum_id is None:
            continue

        if filename == "ENUM_AttachmentID.json":
            subcategory = categorize_attachment(name)
            output[subcategory][name] = enum_id
        else:
            output[category][name] = enum_id

with open("id_db.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print("IDs Parsed")
