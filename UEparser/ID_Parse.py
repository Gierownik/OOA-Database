import json
import os
import re

file_map = {
    r"Raw Data\ENUM_ShellID.json": "Shells",
    r"Raw Data\ENUM_PerkID.json": "Augments",
    r"Raw Data\ENUM_DeviceID.json": "Devices",
    r"Raw Data\ENUM_WeaponID.json": "Weapons",
    r"Raw Data\ENUM_AttachmentID.json": "Attachments"
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

def categorize_attachment(name):
    if (name.endswith("Sight") or name.endswith("Sights")) and name != "Laser Sight":
        return "Optics"
    elif name.endswith("Ammo") or name.endswith("Grenade"):
        return "Ammo"
    else:
        return "Mods"

for filename, category in file_map.items():
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found")
        continue

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data[0].get("Properties", {}).get("DisplayNameMap", [])
    names_map_raw = data[0].get("Names", {})
    names_map = {}
    for full_key, final_id in names_map_raw.items():
        parts = full_key.split("::")
        if len(parts) == 2:
            names_map[parts[1]] = final_id

    for entry in entries:
        key = entry.get("Key", "")
        value = entry.get("Value", {})
        name = value.get("SourceString", "").strip()

        if not name or name == "-":
            continue

        # Try to resolve Final ID from names_map
        final_id = names_map.get(key)
        if final_id is None:
            match = re.match(r"NewEnumerator(\d+)", key)
            final_id = int(match.group(1)) if match else None

        if final_id is None:
            continue  # Skip if we couldn't resolve an ID at all

        # Handle attachments with category mapping
        if filename == r"Raw Data\ENUM_AttachmentID.json":
            subcategory = categorize_attachment(name)
            output[subcategory][name] = final_id
        else:
            output[category][name] = final_id

with open("id.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print("IDs Parsed")
