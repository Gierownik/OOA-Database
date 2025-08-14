import json
import re
with open(r"Raw Data\ENUM_PerkID.json", "r", encoding="utf-8") as f:
    enum_data = json.load(f)
with open(r"Raw Data\ENUM_DeviceID.json", "r", encoding="utf-8") as f:
    device_enum_data = json.load(f)
with open(r"Raw Data\ENUM_WeaponID.json", "r", encoding="utf-8") as f:
    weapon_enum_data = json.load(f)
with open(r"Raw Data\ENUM_AttachmentID.json", "r", encoding="utf-8") as f:
    attachment_enum_data = json.load(f)
with open(r"Raw Data\ENUM_ShellID.json", "r", encoding="utf-8") as f:
    shell_enum_data = json.load(f)
with open(r"Raw Data\DT_SkillTree.json", "r", encoding="utf-8") as f:
    skilltree_data = json.load(f)
with open(r"Raw Data\DT_DeviceData.json", "r", encoding="utf-8") as f:
    device_data = json.load(f)
with open(r"Raw Data\DT_WeaponData.json", "r", encoding="utf-8") as f:
    weapon_data = json.load(f)
with open(r"Raw Data\DT_ShellData.json", "r", encoding="utf-8") as f:
    shell_data = json.load(f)
with open(r"Raw Data\DT_AttachmentData.json", "r", encoding="utf-8") as f:
    attachment_data = json.load(f)
with open(r"Raw Data\ENUM_WeaponClass.json", "r", encoding="utf-8") as f:
    weapon_class = json.load(f)
with open(r"Raw Data\ENUM_Category.json", "r", encoding="utf-8") as f:
    weapon_category = json.load(f)
with open(r"Raw Data\ENUM_FireMode.json", "r", encoding="utf-8") as f:
    weapon_mode = json.load(f)
#-----------------------------------------------------------------------------Tactical ForeGripper fix-----------------------------------------------

for item in attachment_data:
    if "Rows" in item and "TacticalForeGrip" in item["Rows"]:
        item["Rows"]["TacticalForegrip"] = item["Rows"].pop("TacticalForeGrip") 


#----------------------------------------------------------------------------------------------------------------------------------------------------
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
attachment_id_to_name = {
    f"ENUM_AttachmentID::{entry['Key']}": entry["Value"]["SourceString"]
    for entry in attachment_enum_data[0]["Properties"]["DisplayNameMap"]
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
attachment_stats = attachment_data[0]["Rows"]
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

        found = skill_data.get("Foundation_56_A4C8470C4FCFFF82BFB0F097CA1EC92B", "")
        if (found == "ENUM_Foundation::NewEnumerator0"):
            found_type = "body"
        elif (found == "ENUM_Foundation::NewEnumerator1"):
            found_type = "tech"
        elif (found == "ENUM_Foundation::NewEnumerator2"):
            found_type = "hardware"
        else:
            found_type = "other"
        req = skill_data.get("Requirement_59_D88055FA43F71EEE4E6C4A8D07FC1C9D", 0)

        perk_output.append({
            "name": perk_name,
            "tooltip": lines,
            "foundations": {
                "type": found_type,
                "value": req
            }
        })



# save dis
with open("augments.json", "w", encoding="utf-8") as out_file:
    json.dump(perk_output, out_file, indent=2, ensure_ascii=False)
print("Augment database shit workin")
#------------------------------------------------------demvimces---------------------------
device_output = []

for skill_name, data in skill_rows.items():
    device_enum = data.get("DeviceID_28_1CA191F04AB07E6156C5D1B6A59A1F9B")
    if not device_enum or device_enum not in device_id_to_name:
        continue

    device_name = device_id_to_name[device_enum]
    tooltips = data.get("Tooltip_54_1E2214584583FA289C1781AA8CE4153E", [])
    if not tooltips:
        continue

    tooltip_text = tooltips[-1]["LocalizedString"]
    lines = [
        line.strip()
        for line in tooltip_text.strip().splitlines()
        if line.strip()
    ]

    device_stat = device_stats.get(skill_name, {})
    cooldown = device_stat.get("cooldown_11_D555013643FE6003564BDCBE2F66D6AD", 0)
    duration = device_stat.get("duration_19_CADCF2D5460AE568CE1A9A8875DBE004", 0)
    speed_pen = device_stat.get("speedModifier_42_3066E3D040DBA54CFDD276B41E8CC316", 0)

    found = data.get("Foundation_56_A4C8470C4FCFFF82BFB0F097CA1EC92B", "")
    if (found == "ENUM_Foundation::NewEnumerator0"):
        found_type = "body"
    elif (found == "ENUM_Foundation::NewEnumerator1"):
        found_type = "tech"
    elif (found == "ENUM_Foundation::NewEnumerator2"):
        found_type = "hardware"
    else:
        found_type = "other"
    act = device_stat.get("action_57_9ACD9FD14A212852B1FFB8BB602B1D47")
    if (act == "ENUM_DeviceAction::NewEnumerator0"):
        action = "Throw"
    elif (act == "ENUM_DeviceAction::NewEnumerator1"):
        action = "Launch"
    elif (act == "ENUM_DeviceAction::NewEnumerator2"):
        action = "Activate"
    else:
        action = "Deploy"
    
    exp = data.get("Prerequisite_46_1618947F4F88562C70609FAE0671C5E9", 0)
    if (exp == "ENUM_PerkID::NewEnumerator17"):
        experimental = "true"
    else:
        experimental = "false"
    
    req = data.get("Requirement_59_D88055FA43F71EEE4E6C4A8D07FC1C9D", 0)

    device_output.append({
        "name": device_name,
        "tooltip": lines,
        "experimental": experimental,
        "stats": {
            "cooldown": cooldown,
            "duration": duration,
            "action": action,
            "speed_penalty": speed_pen / 100
        },
        "foundations": {
            "type": found_type,
            "value": req
        }
    })

with open("devices.json", "w", encoding="utf-8") as out_file:
    json.dump(device_output, out_file, indent=2, ensure_ascii=False)
print("Device database shit workin")
#-------------------------------------------Goons---------------------------------------
weapon_output = []

for skill_name, data in skill_rows.items():
    weapon_enum = data.get("WeaponID_22_BB8DC4A4405B740F189E2AAEF93AA65E")
    if not weapon_enum or weapon_enum not in weapon_id_to_name:
        continue

    weapon_name = weapon_id_to_name[weapon_enum]

    found = data.get("Foundation_56_A4C8470C4FCFFF82BFB0F097CA1EC92B", "")
    if (found == "ENUM_Foundation::NewEnumerator0"):
        found_type = "body"
    elif (found == "ENUM_Foundation::NewEnumerator1"):
        found_type = "tech"
    elif (found == "ENUM_Foundation::NewEnumerator2"):
        found_type = "hardware"
    else:
        found_type = "other"
    req = data.get("Requirement_59_D88055FA43F71EEE4E6C4A8D07FC1C9D", 0)

    weapon_stat = weapon_stats.get(skill_name, {})
    damage_section = weapon_stat.get("damage_51_4503C2744F2DD64F4FC8FFADCC5F09EE", {})

    slot_enum = weapon_stat.get("weaponClass_103_A033AA0D4A67345BE9F09089017236C0", "")
    cat_enum = weapon_stat.get("category_158_45CB73F443BFECF1A75A4ABAD13BEB27", "")
    fire_enum = weapon_stat.get("fireMode_27_09F1BA2744EAF4289A2295991B702E2A", "")

    slot_key = slot_enum.replace("ENUM_WeaponClass::", "")
    cat_key = cat_enum.replace("ENUM_Category::", "")
    fire_key = fire_enum.replace("ENUM_FireMode::", "")

    slot_name = weapon_class_to_value.get(slot_key, slot_key)
    cat_name = weapon_category_to_value.get(cat_key, cat_key)
    fire_name = weapon_mode_to_value.get(fire_key, fire_key)

    stats = {
        "id": weapon_stat.get("ID_164_1DF0FD0E430EA7E965B389963917762B", 0),
        "type": weapon_stat.get("Class_165_71C2F5264EA07AE77DDE398BD5729CD0", 0),
        "slot": slot_name,
        "category": cat_name,
        "firemode": fire_name,
        "firerate": f"{weapon_stat.get('roundsPerMinute_88_9A62D92546A54AF5B9BD9CA681C99779', 0)}",
        "damage_near": damage_section.get("DamageNear_28_C0ECF144455E9C9F13D929A6E1A9FA6C", 0),
        "damage_far": damage_section.get("DamageFar_31_9A92287545630DA083AAA18D6F6D52B2", 0),
        "range": f"{damage_section.get('RangeNear_32_7051C33A45ED3E81881748AF79D60E71', 0)} - {damage_section.get('RangeFar_33_9FC06C8A49BBBCDC074BDEBAF8F978BB', 0)}",
        "head_mult": f"{damage_section.get('HeadMultiplier_18_6AC23285474D12C7B9B9C9B43C915FE8', 0)}",
        "limb_mult": f"{damage_section.get('LimbMultiplier_36_F099D86241C4A7BDF8FC47849F76F552', 0)}",
        "penetration": f"{weapon_stat.get('penetrationPower_18_B8E8BDFC45F3DFA9B84410AEEF7CF3DE', 0)}",
        "velocity": f"{weapon_stat.get('muzzleVelocity_20_0A3F52FD4DB2E8D23F8E05A26A11E7BA', 0) / 100}",
        "recoil_vert": weapon_stat.get("recoilVertical_14_8D17013D41FC3D7BB68C2E816F8B69C7", 0),
        "recoil_hor": weapon_stat.get("recoilHorizonal_16_562990B74D7D4F4DDCF429942D1839C5", 0),
        "aim_time": f"{weapon_stat.get('aimTime_34_F110FBC149382F201D7A3C9AA8BE8D17', 0)}",
        "spread_hip": f"{weapon_stat.get('hipSpread_92_F512DB8F4AA38F47776755B509674FDB', 0)}",
        "spread_ads": f"{weapon_stat.get('aimSpread_93_4DB54D3B45DEEA9F6DBF20B24D661F94', 0)}",
        "spread_gain": f"{weapon_stat.get('spreadGain_135_D194D65F441D7033F8F0E89B097BD9ED', 0)}",
        "speed_penalty": f"{weapon_stat.get('speedModifier_75_CA08E44842050D047DB75CA31280BE88', 0) / 100}"
    }

    if (val := weapon_stat.get("burstCount_125_4B49DFE84C24E8AA5A63B7B6983618D1")) not in [0, 0.0, False, ""]:
        stats["burst_count"] = val
    if (val := weapon_stat.get("burstDelay_152_D2A7BF0742680DCB3E9BE381C99B9BFC")) not in [0, 0.0, False, ""]:
        stats["burst_delay"] = f"{val}"
    if (val := weapon_stat.get("spinUpDuration_114_42F529AD41ADDCCCDB0ED0915E8BCCEC")) not in [0, 0.0, False, ""]:
        stats["spinup"] = f"{val}s"
    if (val := weapon_stat.get("usesAmmo_109_C8A226E545A12A663A1AF398568E1897")) not in [0, 0.0, True, ""]:
        stats["ammo_infinite"] = "true"
    if (val := weapon_stat.get("ammoCapacity_37_C66372EB4769BC9D909A6CA771FD33A0")) not in [0, 0.0, False, ""]:
        stats["ammo_capacity"] = val
    if (val := weapon_stat.get("reloadSpeed_42_4B9E289B467B258218AE298E52A1B0E3")) not in [0, 0.0, False, ""]:
        stats["reload_duration"] = f"{val}"
    if (val := weapon_stat.get("rechamberDuration_121_DA9C2951452609B501BB76B185DE3800")) not in [0, 0.0, False, ""]:
        stats["rechamber_duration"] = f"{val}"
    if (val := weapon_stat.get("singleReload_128_E69294BE4B79448A0BAC2AB62561973D")) not in [0, 0.0, False, ""]:
        stats["one_by_one_reload"] = "true"

    weapon_output.append({
        "name": weapon_name,
        "stats": stats,
        "foundations": {
            "type": found_type,
            "value": req
        }
    })

with open("weapons.json", "w", encoding="utf-8") as out_file:
    json.dump(weapon_output, out_file, indent=2, ensure_ascii=False)

print("Weapon database shit workin")
#----------------------------------------------------------------------Mods n shit-----------------------------------------------------------
attachment_output = []

for skill_name, data in skill_rows.items():
    attachment_enum = data.get("AttachmentID_37_E6AEC497440716B81674448A0826E94C")
    if not attachment_enum or attachment_enum not in attachment_id_to_name:
        continue

    attachment_name = attachment_id_to_name[attachment_enum]
    tooltips = data.get("Tooltip_54_1E2214584583FA289C1781AA8CE4153E", [])
    if not tooltips:
        continue

    tooltip_text = tooltips[-1]["LocalizedString"]
    lines = [
        line.strip()
        for line in tooltip_text.strip().splitlines()
        if line.strip()
    ]

    attachment_stat = attachment_stats.get(skill_name, {})
    comp = attachment_stat.get("compatibility_36_7FE0C99C438BD2496CBB7FBF13856D3B", 0)
    if comp == 0:
        compatibility = []
    else:
        compatibility = [weapon_id_to_name.get(wep_id, wep_id) for wep_id in comp]
    mod_type = attachment_stat.get("type_23_AEC1445A44E4B924DED2AABCBB869556", 0)
    exclu = attachment_stat.get("excludeList_43_3E6DA3624973B648616BB8AC7146A5D8", 0)
    if exclu == 0:
        exclude = []
    else:
        exclude = [attachment_id_to_name.get(at_id, at_id) for at_id in exclu]
    if mod_type == "ENUM_AttachmentType::NewEnumerator2":
        attachment_type = "Mod"
    elif mod_type == "ENUM_AttachmentType::NewEnumerator0":
        attachment_type = "Optic"
    elif mod_type == "ENUM_AttachmentType::NewEnumerator3":
        attachment_type = "Ammo"
    else:
        attachment_type = "Unknown"

    found = data.get("Foundation_56_A4C8470C4FCFFF82BFB0F097CA1EC92B", "")
    if (found == "ENUM_Foundation::NewEnumerator0"):
        found_type = "body"
    elif (found == "ENUM_Foundation::NewEnumerator1"):
        found_type = "tech"
    elif (found == "ENUM_Foundation::NewEnumerator2"):
        found_type = "hardware"
    else:
        found_type = "other"

    tech = data.get("Prerequisite_46_1618947F4F88562C70609FAE0671C5E9", 0)
    if (tech == "ENUM_PerkID::NewEnumerator23"):
        technician = "true"
    else:
        technician = "false"
    
    req = data.get("Requirement_59_D88055FA43F71EEE4E6C4A8D07FC1C9D", 0)

    attachment_output.append({
        "name": attachment_name,
        "type": attachment_type,
        "tooltip": lines,
        "technician": technician,
        "compatibility": compatibility,
        "excludes": exclude,
        "foundations": {
            "type": found_type,
            "value": req
        }
    })

with open("attachments.json", "w", encoding="utf-8") as out_file:
    json.dump(attachment_output, out_file, indent=2, ensure_ascii=False)
print("Mod database shit workin")
#-------------------------------------------------------------------Shellfish----------------------
shell_output = []

for skill_name, shell_data in skill_rows.items():
    shell_enum = shell_data.get("ShellID_20_E0F2764D41C112BEE1BFEA864FA45992")
    if not shell_enum or shell_enum not in shell_id_to_name:
        continue

    shell_name = shell_id_to_name[shell_enum]
    tooltips = shell_data.get("Tooltip_54_1E2214584583FA289C1781AA8CE4153E", [])
    if not tooltips:
        continue

    tooltip_text = tooltips[-1]["LocalizedString"]
    lines = [
        line.strip()
        for line in tooltip_text.strip().splitlines()
        if line.strip()
    ]

    shell_stat = shell_stats.get(shell_name, {})
    vit = shell_stat.get("health_46_8D62C6074CE3721B91A1A1A352B1DAAA", 0)
    defe = shell_stat.get("armour_40_6774162D445FCEB1CEEC26A0CC5BE55F", 0)
    sped = shell_stat.get("speedModifier_32_2C4926ED42431993DD4F01B0F07F8908", 0)
    core = shell_stat.get("coreSpeed_49_16E1B3544598A2B32ABC7EB0BF430FCF", 0)
    rdr = shell_stat.get("radarRange_43_14DB15624ACE3BC2575EE191D41E0BDE", 0)

    if (shell_name == "Bison"):
        defer = 15
        deferd = 1
        aux = 40
        climb = 0.2
        air = 1
        spetz = "> Activates after killing an enemy: <C>50%</> increased weapon accuracy, <C>25%</> increased speed + dexterity, for <C>5 s</> on receiving direct vitals damage, <C>10 s</> cooldown"
    elif (shell_name == "Hydra"):
        defer = 15
        deferd = 0
        aux = 35
        climb = 0.25
        air = 1
        spetz = "> Activates after killing an enemy: Gain an Adrenal Feedback stack every <C>20 s</>, stacking up to <C>5</> times"
    elif (shell_name == "Dragon"):
        defer = 10
        deferd = 1
        aux = 30
        climb = 0.25
        air = 2
        spetz = "> Activates after killing an enemy: Backdraft + Ground Slam deal <C>25%</> increased fire damage + apply combust"
    elif (shell_name == "Ghost"):
        defer = 10
        deferd = 1
        aux = 40
        climb = 0.15
        air = 2
        spetz = "> Activates after killing an enemy: Hip firing supressed firearms, throwing devices + interactions no longer deactivate camouflage"
    elif (shell_name == "Rhino"):
        defer = 10
        deferd = 1.5
        aux = 30
        climb = 0.25
        air = 0
        spetz = "> Activates after killing an enemy: Shockwave gains <C>50%</> increased debuff duration, incresed knockback force, applies stun + cripple"
    else:
        defer = 0
        deferd = 0
        aux = 0
        climb = 0
        air = 0
        spetz = "> Activates after scratching your balls"

    found = shell_data.get("Foundation_56_A4C8470C4FCFFF82BFB0F097CA1EC92B", "")
    if (found == "ENUM_Foundation::NewEnumerator0"):
        found_type = "body"
    elif (found == "ENUM_Foundation::NewEnumerator1"):
        found_type = "tech"
    elif (found == "ENUM_Foundation::NewEnumerator2"):
        found_type = "hardware"
    else:
        found_type = "other"
    req = shell_data.get("Requirement_59_D88055FA43F71EEE4E6C4A8D07FC1C9D", 0)

    shell_output.append({
        "name": shell_name,
        "tooltip": lines,
        "specialisation": spetz,
        "stats": {
            "vitals": vit,
            "defense": defe,
            "defense_regen": defer,
            "defense_regen_delay": deferd,
            "aux_regen": aux,
            "speed": 8 - (sped / 100),
            "climb_penalty": climb,
            "aerial_charges": air,
            "core_speed": core,
            "radar_profile": rdr / 100     
        },
        "foundations": {
            "type": found_type,
            "value": req
        }
    })

with open("shells.json", "w", encoding="utf-8") as out_file:
    json.dump(shell_output, out_file, indent=2, ensure_ascii=False)
print("Shell database shit workin n faked")
#----------------------------------------------------------faking toolips baybeeeeee-------------------------------
spec_output = []

for entry in wep_cat["DisplayNameMap"]:
    key = entry["Key"]
    spec = entry["Value"]["SourceString"]
    if spec == "-":
        continue
    if spec == "Heavy Weapons":
        spec_output.append({
            "name": spec,
            "tooltip": [
                f"> <C>15%</> increased dexterity with {spec}",
                f"> <C>25%</> reduced loadout speed penalty from {spec}",
                f"> <C>25%</> reduced direct damage received from {spec}"
            ]
    })
    elif spec == "Melee Weapons":
        spec_output.append({
            "name": spec,
            "tooltip": [
                f"> <C>15%</> increased dexterity with {spec}",
                f"> <C>10%</> increased ground speed while using {spec}",
                f"> <C>25%</> increased aux power regeneration while using {spec}"
            ]
    })
    elif spec == "Devices":
        spec_output.append({
            "name": spec,
            "tooltip": [
                "> <C>100%</> reduced device speed penalties",
                "> <C>25%</> increased device duration + throw velocity",
                "> <C>25%</> reduced device cooldowns"
            ]
    })
    elif spec == "Shells":
        spec_output.append({
            "name": spec,
            "tooltip": [
                "Check shell tooltips"
            ]
    })
    else:
        spec_output.append({
            "name": spec,
            "tooltip": [
                f"> <C>15%</> increased dexterity with {spec}",
                f"> <C>100%</> additional reserve ammo for {spec}",
                f"> <C>100%</> additional reserve ammo for non loadout {spec}"
            ]
    })
        
with open("specialisations.json", "w", encoding="utf-8") as out_file:
    json.dump(spec_output, out_file, indent=2, ensure_ascii=False)
print("Spectz database shit faked")