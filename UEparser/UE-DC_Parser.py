import json
import re
with open("augments.json", "r", encoding="utf-8") as f:
    enum_data = json.load(f)
with open("devices.json", "r", encoding="utf-8") as f:
    device_enum_data = json.load(f)
with open("weapons.json", "r", encoding="utf-8") as f:
    weapon_enum_data = json.load(f)
with open("shells.json", "r", encoding="utf-8") as f:
    shell_enum_data = json.load(f)

def format_line(line):
    # Doku doesnt do other effects, so its just upside and downside (thats the reason i retype all tooltips)
    # Discord formating: bold numbers: replaces <C>...</> with **...**
    line = re.sub(r"<C>(.*?)</>", r"**\1**", line)
    # Discord formatting: lists and upside tag (^): replace lines that start with "> " with "- ^"  (yeh i chose random symbols as tags)
    line = re.sub(r"^> ", r"- ^ ", line)
    # Discord formatting: list and downside tag (@): replaces <B>>...</> with - @...
    line = re.sub(r"<B>>\s*(.*?)</>", r"- @ \1", line)
    # The line above me does some funky stuff this is the fix:
    line = re.sub(r"<B>\s*(.*?)</>", r"\1", line)
    #Speed pen cm/s to m/s
    line = re.sub(r",\s*(\d+)\.0 Speed Penalty",
    lambda m: f", {int(m.group(1))/100:.2f} m/s Speed Penalty",line)
    # Discord formating: Integrated augments titles
    line = re.sub(r":: <D>(.*?)</>", r"**:: \1**", line)
    return line.strip()
def format_weapon(line):
    line = re.sub(r":\s*(.+)", r": **\1**", line)
    line = re.sub(r"@", r"- @", line)
    line = re.sub(r"\b(\d+)\.0\b", r"\1", line)


    return line.strip()
def format_everything(obj):
    if isinstance(obj, str):
        return format_line(obj)
    elif isinstance(obj, list):
        return [format_everything(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: format_everything(value) for key, value in obj.items()}
    else:
        return obj
def format_weapons(obj):
    if isinstance(obj, str):
        return format_weapon(obj)
    elif isinstance(obj, list):
        return [format_weapons(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: format_weapons(value) for key, value in obj.items()}
    else:
        return obj


perk_output = format_everything(enum_data)
with open("augments_dc.json", "w", encoding="utf-8") as out_file:
    json.dump(perk_output, out_file, indent=2, ensure_ascii=False)
device_output = format_everything(device_enum_data)
with open("devices_dc.json", "w", encoding="utf-8") as out_file:
    json.dump(device_output, out_file, indent=2, ensure_ascii=False)
shell_output = format_everything(shell_enum_data)
with open("shells_dc.json", "w", encoding="utf-8") as out_file:
    json.dump(shell_output, out_file, indent=2, ensure_ascii=False)
weapon_output = format_weapons(weapon_enum_data)
with open("weapons_dc.json", "w", encoding="utf-8") as out_file:
    json.dump(weapon_output, out_file, indent=2, ensure_ascii=False)



print("Shit's working")