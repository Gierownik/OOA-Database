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
with open("DT_SkillTree.json", "r", encoding="utf-8") as f:
    skilltree_data = json.load(f)
with open("DT_DeviceData.json", "r", encoding="utf-8") as f:
    device_data = json.load(f)
with open("DT_WeaponData.json", "r", encoding="utf-8") as f:
    weapon_data = json.load(f)

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
skill_rows = skilltree_data[0]["Rows"]

#------------------------------------- Perk stuff ------------------------------------------
perk_output = {}

for skill_name, skill_data in skill_rows.items():
    perk_enum = skill_data.get("PerkID_25_4BC92A00469A851AA5FE2792BE9F96C4")

    if perk_enum in perk_id_to_name:
        perk_name = perk_id_to_name[perk_enum]
        tooltips = skill_data.get("Tooltip_54_1E2214584583FA289C1781AA8CE4153E", [])
        if not tooltips:
            continue

        tooltip_text = tooltips[-1]["LocalizedString"]

        lines = [
            line
            for line in tooltip_text.strip().splitlines()
            if line.strip()
        ]
        req = skill_data.get("Requirements_8_A4C8470C4FCFFF82BFB0F097CA1EC92B", {})
        body = req.get("Body_10_68FBC6C34B6DDB19E010A9AB2419B88B", 0)
        tech = req.get("Tech_11_D9A98AA74B87F1DD6B0F43B4233753BC", 0)
        hardware = req.get("Hardware_12_9310D7DB447E651E58D0268CC41AC3B7", 0)

        lines.extend([
            f"& {body} Body, {tech} Tech, {hardware} Hardware",
        ])
        perk_output[perk_name] = lines


# Save to JSON
with open("augments.json", "w", encoding="utf-8") as out_file:
    json.dump(perk_output, out_file, indent=2, ensure_ascii=False)
print("Augment shit workin")
#--------------------------------------Device part-----------------------------------------------

device_output = {}

for skill_name, data in skill_rows.items():
    device_enum = data.get("DeviceID_28_1CA191F04AB07E6156C5D1B6A59A1F9B")
    if not device_enum or device_enum not in device_id_to_name:
        continue

    device_name = device_id_to_name[device_enum]
    lines = []

    
    tooltips = data.get("Tooltip_54_1E2214584583FA289C1781AA8CE4153E", [])
    if tooltips:
        tooltip_text = tooltips[-1]["LocalizedString"]
        lines.extend([
            line for line in tooltip_text.strip().splitlines()
            if line.strip()
        ])

    
    req = data.get("Requirements_8_A4C8470C4FCFFF82BFB0F097CA1EC92B", {})
    body = req.get("Body_10_68FBC6C34B6DDB19E010A9AB2419B88B", 0)
    tech = req.get("Tech_11_D9A98AA74B87F1DD6B0F43B4233753BC", 0)
    hardware = req.get("Hardware_12_9310D7DB447E651E58D0268CC41AC3B7", 0)
    lines.append(f"& {body} Body, {tech} Tech, {hardware} Hardware")


    device_stat = device_stats.get(skill_name, {})
    cooldown = device_stat.get("cooldown_11_D555013643FE6003564BDCBE2F66D6AD", 0)
    duration = device_stat.get("duration_19_CADCF2D5460AE568CE1A9A8875DBE004", 0)
    speed_pen = device_stat.get("speedModifier_42_3066E3D040DBA54CFDD276B41E8CC316", 0)
    lines.append(f"$ {cooldown} Cooldown, {duration} Duration, {speed_pen} Speed Penalty, Experimental: WIP")


    device_output[device_name] = lines

with open("devices.json", "w", encoding="utf-8") as out_file:
    json.dump(device_output, out_file, indent=2, ensure_ascii=False)
print("Device shit workin")
#--------------------------------------Weapon part-----------------------------------------------

weapon_output = {}

for skill_name, data in skill_rows.items():
    weapon_enum = data.get("WeaponID_22_BB8DC4A4405B740F189E2AAEF93AA65E")
    if not weapon_enum or weapon_enum not in weapon_id_to_name:
        continue

    weapon_name = weapon_id_to_name[weapon_enum]
    lines = []


    req = data.get("Requirements_8_A4C8470C4FCFFF82BFB0F097CA1EC92B", {})
    body = req.get("Body_10_68FBC6C34B6DDB19E010A9AB2419B88B", 0)
    tech = req.get("Tech_11_D9A98AA74B87F1DD6B0F43B4233753BC", 0)
    hardware = req.get("Hardware_12_9310D7DB447E651E58D0268CC41AC3B7", 0)
    lines.append(f"& {body} Body, {tech} Tech, {hardware} Hardware")


    weapon_stat = weapon_stats.get(skill_name, {})
    slot_enum = weapon_stat.get("weaponClass_103_A033AA0D4A67345BE9F09089017236C0", "")
    cat_enum = weapon_stat.get("category_158_45CB73F443BFECF1A75A4ABAD13BEB27", "")
    fire_enum = weapon_stat.get("fireMode_27_09F1BA2744EAF4289A2295991B702E2A", "")


    slot_key = slot_enum.replace("ENUM_WeaponClass::", "")
    cat_key = cat_enum.replace("ENUM_Category::", "")
    fire_key = fire_enum.replace("ENUM_FireMode::", "")


    slot_name = weapon_class_to_value.get(slot_key, slot_key)
    cat_name = weapon_category_to_value.get(cat_key, cat_key)
    fire_name = weapon_mode_to_value.get(fire_key, fire_key)
    #-------------------Main part:-------------------
    #stat = weapon_stat.get("statid_ABCDEFGH", 0)
    #lines.append(f"@ Stat: {stat}")
    id = weapon_stat.get("ID_164_1DF0FD0E430EA7E965B389963917762B", 0)
    lines.append(f"^ ID: {id}")
    type = weapon_stat.get("Class_165_71C2F5264EA07AE77DDE398BD5729CD0", 0)
    lines.append(f"^ Weapon Type: {type}")
    lines.append(f"^ Slot: {slot_name}")
    lines.append(f"^ Category: {cat_name}")
    lines.append(f"@ Firemode: {fire_name}")






    weapon_output[weapon_name] = lines

with open("weapons.json", "w", encoding="utf-8") as out_file:
    json.dump(weapon_output, out_file, indent=2, ensure_ascii=False)
print("Weapon shit maybe workin")