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

        if filename == "ENUM_AttachmentID.json":
            subcategory = categorize_attachment(name)
            match = re.match(r"NewEnumerator(\d+)", key)
            enum_id = int(match.group(1)) if match else None
            if enum_id is not None:
                output[subcategory][name] = enum_id
        elif filename in ("ENUM_WeaponID.json", "ENUM_DeviceID.json", "ENUM_ShellID.json"):
            final_id = names_map.get(key)
            if final_id is not None:
                output[category][name] = final_id
            else:
                match = re.match(r"NewEnumerator(\d+)", key)
                enum_id = int(match.group(1)) if match else None
                if enum_id is not None:
                    output[category][name] = enum_id
        else:
            match = re.match(r"NewEnumerator(\d+)", key)
            enum_id = int(match.group(1)) if match else None
            if enum_id is not None:
                output[category][name] = enum_id

with open("id_db.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print("IDs Parsed")
