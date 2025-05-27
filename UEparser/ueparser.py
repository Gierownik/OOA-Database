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
    damage_section = weapon_stat.get("damage_51_4503C2744F2DD64F4FC8FFADCC5F09EE", {})
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
    burst = weapon_stat.get("burstCount_125_4B49DFE84C24E8AA5A63B7B6983618D1", 0)
    if burst not in [0, 0.0, False, ""]:
        lines.append(f"@ Burst Count: {burst}")
    burst_del = weapon_stat.get("burstDelay_152_D2A7BF0742680DCB3E9BE381C99B9BFC", 0)
    if burst_del not in [0, 0.0, False, ""]:
        lines.append(f"@ Burst Delay: {burst_del}s")
    rpm = weapon_stat.get("roundsPerMinute_88_9A62D92546A54AF5B9BD9CA681C99779", 0)
    lines.append(f"@ Firerate: {rpm} rpm")
    spinup = weapon_stat.get("spinUpDuration_114_42F529AD41ADDCCCDB0ED0915E8BCCEC", 0)
    if spinup not in [0, 0.0, False, ""]:
        lines.append(f"@ Spinup: {spinup}s")
    infammo = weapon_stat.get("usesAmmo_109_C8A226E545A12A663A1AF398568E1897", 0)
    if infammo not in [0, 0.0, True, ""]:
        lines.append(f"@ Infinite ammo: True")
    cap = weapon_stat.get("ammoCapacity_37_C66372EB4769BC9D909A6CA771FD33A0", 0)
    if cap not in [0, 0.0, False, ""]:
        lines.append(f"@ Ammo Capacity: {cap}")
    rlspe = weapon_stat.get("reloadSpeed_42_4B9E289B467B258218AE298E52A1B0E3", 0)
    if rlspe not in [0, 0.0, False, ""]:
        lines.append(f"@ Reload Duration: {rlspe}s")
    rchm = weapon_stat.get("rechamberDuration_121_DA9C2951452609B501BB76B185DE3800", 0)
    if rchm not in [0, 0.0, False, ""]:
        lines.append(f"@ Rechamber Duration: {rchm}s")
    singleload = weapon_stat.get("singleReload_128_E69294BE4B79448A0BAC2AB62561973D", 0)
    if singleload not in [0, 0.0, False, ""]:
        lines.append(f"@ One by one reload: True")
    dmgn = damage_section.get("DamageNear_28_C0ECF144455E9C9F13D929A6E1A9FA6C", 0)
    lines.append(f"@- Near Damage: {dmgn}")
    dmgf = damage_section.get("DamageFar_31_9A92287545630DA083AAA18D6F6D52B2", 0)
    lines.append(f"@- Far Damage: {dmgf}")
    rngn = damage_section.get("RangeNear_32_7051C33A45ED3E81881748AF79D60E71", 0)
    rngf = damage_section.get("RangeFar_33_9FC06C8A49BBBCDC074BDEBAF8F978BB", 0)
    lines.append(f"@- Range: {rngn} - {rngf} m")
    hsm = damage_section.get("HeadMultiplier_18_6AC23285474D12C7B9B9C9B43C915FE8", 0)
    lines.append(f"@- Headshot Multiplier: {hsm}x")
    lmb = damage_section.get("LimbMultiplier_36_F099D86241C4A7BDF8FC47849F76F552", 0)
    lines.append(f"@- Limb Multiplier: {lmb}x")
    bld = damage_section.get("BleedMultiplier_27_0D5F760E45CA9912594F6787BD30615F", 0)
    if bld not in [1, 1.0, False, ""]:
        lines.append(f"@- Bleed Multiplier: {bld}x")
    pen = weapon_stat.get("penetrationPower_18_B8E8BDFC45F3DFA9B84410AEEF7CF3DE", 0)
    lines.append(f"@ Penetration: {pen} cm")
    vel = weapon_stat.get("muzzleVelocity_20_0A3F52FD4DB2E8D23F8E05A26A11E7BA", 0)
    lines.append(f"@ Velocity: {vel} m/s")
    recv = weapon_stat.get("recoilVertical_14_8D17013D41FC3D7BB68C2E816F8B69C7", 0)
    lines.append(f"@- Vertical Recoil: {recv}")
    rech = weapon_stat.get("recoilHorizonal_16_562990B74D7D4F4DDCF429942D1839C5", 0)
    lines.append(f"@- Horizontal Recoil: {rech}")
    ads = weapon_stat.get("aimTime_34_F110FBC149382F201D7A3C9AA8BE8D17", 0)
    lines.append(f"@ Time to ADS: {ads}s")
    sprdh = weapon_stat.get("hipSpread_92_F512DB8F4AA38F47776755B509674FDB", 0)
    lines.append(f"@- Hipfire Spread: {sprdh}°")
    sprda = weapon_stat.get("aimSpread_93_4DB54D3B45DEEA9F6DBF20B24D661F94", 0)
    lines.append(f"@- ADS Spread: {sprda}°")
    sprdg = weapon_stat.get("spreadGain_135_D194D65F441D7033F8F0E89B097BD9ED", 0)
    lines.append(f"@- Spread Gain: {sprdg}°")
    spdpen = weapon_stat.get("speedModifier_75_CA08E44842050D047DB75CA31280BE88", 0)
    lines.append(f"@ Speed Penalty: 0.{spdpen} m/s")

    







    weapon_output[weapon_name] = lines

with open("weapons.json", "w", encoding="utf-8") as out_file:
    json.dump(weapon_output, out_file, indent=2, ensure_ascii=False)
print("Weapon shit maybe workin")
#------------------------------------------------Shell stuff-----------------------------------------------------------------------
shell_output = {}

for shell_name, shell_data in skill_rows.items():
    shell_enum = shell_data.get("ShellID_20_E0F2764D41C112BEE1BFEA864FA45992")

    if shell_enum in shell_id_to_name:
        shell_name = shell_id_to_name[shell_enum]
        tooltips = shell_data.get("Tooltip_54_1E2214584583FA289C1781AA8CE4153E", [])
        if not tooltips:
            continue

        tooltip_text = tooltips[-1]["LocalizedString"]

        lines = [
            line
            for line in tooltip_text.strip().splitlines()
            if line.strip()
        ]
        shell_stat = shell_stats.get(shell_name, {})
        vit = shell_stat.get("health_46_8D62C6074CE3721B91A1A1A352B1DAAA", 0)
        lines.append(f"Vitals: {vit}")
        defe = shell_stat.get("armour_40_6774162D445FCEB1CEEC26A0CC5BE55F", 0)
        lines.append(f"Defense: {defe}")
        sped = shell_stat.get("speedModifier_32_2C4926ED42431993DD4F01B0F07F8908", 0)
        lines.append(f"Base Speed: {(800 - sped) / 100} m/s")
        core = shell_stat.get("coreSpeed_49_16E1B3544598A2B32ABC7EB0BF430FCF", 0)
        lines.append(f"Core Speed: {core * 100}%")
        rdr = shell_stat.get("radarRange_43_14DB15624ACE3BC2575EE191D41E0BDE", 0)
        lines.append(f"Radar detection range: {rdr / 100} m")
        req = skill_data.get("Requirements_8_A4C8470C4FCFFF82BFB0F097CA1EC92B", {})
        body = req.get("Body_10_68FBC6C34B6DDB19E010A9AB2419B88B", 0)
        tech = req.get("Tech_11_D9A98AA74B87F1DD6B0F43B4233753BC", 0)
        hardware = req.get("Hardware_12_9310D7DB447E651E58D0268CC41AC3B7", 0)

        lines.extend([
            f"& {body} Body, {tech} Tech, {hardware} Hardware",
        ])
        shell_output[shell_name] = lines


# Save to JSON
with open("shells.json", "w", encoding="utf-8") as out_file:
    json.dump(shell_output, out_file, indent=2, ensure_ascii=False)
print("Shell shit workin")