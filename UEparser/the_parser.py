import json
import re
# i use perk instead of aug cuz why not
# Load ENUM_PerkID
with open("ENUM_PerkID.json", "r", encoding="utf-8") as f:
    enum_data = json.load(f)
with open("ENUM_DeviceID.json", "r", encoding="utf-8") as f:
    device_enum_data = json.load(f)
with open("ENUM_WeaponID.json", "r", encoding="utf-8") as f:
    weapon_enum_data = json.load(f)
with open("ENUM_ShellID.json", "r", encoding="utf-8") as f:
    shell_enum_data = json.load(f)
with open("DT_SkillTree.json", "r", encoding="utf-8") as f:
    skilltree_data = json.load(f)
with open("DT_DeviceData.json", "r", encoding="utf-8") as f:
    device_data = json.load(f)
with open("DT_WeaponData.json", "r", encoding="utf-8") as f:
    weapon_data = json.load(f)
with open("DT_ShellData.json", "r", encoding="utf-8") as f:
    shell_data = json.load(f)

with open("ENUM_WeaponClass.json", "r", encoding="utf-8") as f:
    weapon_class = json.load(f)
with open("ENUM_Category.json", "r", encoding="utf-8") as f:
    weapon_category = json.load(f)
with open("ENUM_FireMode.json", "r", encoding="utf-8") as f:
    weapon_mode = json.load(f)

enum_props = enum_data[0]["Properties"]
dev_props = device_data[0]["Properties"]
wep_props = weapon_data[0]["Properties"]

wep_class = weapon_class[0]["Properties"]
wep_cat = weapon_category[0]["Properties"]
wep_mode = weapon_mode[0]["Properties"]

perk_id_to_name = {
    f"ENUM_PerkID::{entry['Key']}": entry["Value"]["SourceString"]
    for entry in enum_props["DisplayNameMap"]
    if entry["Value"]["SourceString"] != "-"
}
device_id_to_name = {
    f"ENUM_DeviceID::{entry['Key']}": entry["Value"]["SourceString"]
    for entry in device_enum_data[0]["Properties"]["DisplayNameMap"]
    if entry["Value"]["SourceString"] != "-"
}
weapon_id_to_name = {
    f"ENUM_WeaponID::{entry['Key']}": entry["Value"]["SourceString"]
    for entry in weapon_enum_data[0]["Properties"]["DisplayNameMap"]
    if entry["Value"]["SourceString"] != "-"
}
shell_id_to_name = {
    f"ENUM_ShellID::{entry['Key']}": entry["Value"]["SourceString"]
    for entry in shell_enum_data[0]["Properties"]["DisplayNameMap"]
    if entry["Value"]["SourceString"] != "-"
}

weapon_class_to_value = {
    entry["Key"]: entry["Value"]["SourceString"]
    for entry in wep_class["DisplayNameMap"]
    if entry["Value"]["SourceString"] != "-"
}

weapon_category_to_value = {
    entry["Key"]: entry["Value"]["SourceString"]
    for entry in wep_cat["DisplayNameMap"]
    if entry["Value"]["SourceString"] != "-"
}

weapon_mode_to_value = {
    entry["Key"]: entry["Value"]["SourceString"]
    for entry in wep_mode["DisplayNameMap"]
    if entry["Value"]["SourceString"] != "-"
}
device_stats = device_data[0]["Rows"]
weapon_stats = weapon_data[0]["Rows"]
shell_stats = shell_data[0]["Rows"]
skill_rows = skilltree_data[0]["Rows"]
#---------------------------------------------------permks----------------------------------------------------
perk_output = []

for skill_name, skill_data in skill_rows.items():
    perk_enum = skill_data.get("PerkID_25_4BC92A00469A851AA5FE2792BE9F96C4")

    if perk_enum in perk_id_to_name:
        perk_name = perk_id_to_name[perk_enum]
        tooltips = skill_data.get("Tooltip_54_1E2214584583FA289C1781AA8CE4153E", [])
        if not tooltips:
            continue

        tooltip_text = tooltips[-1]["LocalizedString"]
        lines = [
            line.strip()
            for line in tooltip_text.strip().splitlines()
            if line.strip()
        ]

        req = skill_data.get("Requirements_8_A4C8470C4FCFFF82BFB0F097CA1EC92B", {})
        body = req.get("Body_10_68FBC6C34B6DDB19E010A9AB2419B88B", 0)
        tech = req.get("Tech_11_D9A98AA74B87F1DD6B0F43B4233753BC", 0)
        hardware = req.get("Hardware_12_9310D7DB447E651E58D0268CC41AC3B7", 0)

        perk_output.append({
            "name": perk_name,
            "tooltip": lines,
            "foundations": {
                "body": body,
                "tech": tech,
                "hardware": hardware
            }
        })



# save dis
with open("augments_db_test.json", "w", encoding="utf-8") as out_file:
    json.dump(perk_output, out_file, indent=2, ensure_ascii=False)
print("Augment database shit workin")