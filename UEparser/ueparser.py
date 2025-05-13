import json
import re
# i use perk instead of aug cuz why not
# Load ENUM_PerkID
with open("ENUM_PerkID.json", "r", encoding="utf-8") as f:
    enum_data = json.load(f)

enum_props = enum_data[0]["Properties"]
perk_id_to_name = {
    f"ENUM_PerkID::{entry['Key']}": entry["Value"]["SourceString"]
    for entry in enum_props["DisplayNameMap"]
    if entry["Value"]["SourceString"] != "-"
}

# Load DT_SkillTree (ye its a data tree not an enum but close enough)
with open("DT_SkillTree.json", "r", encoding="utf-8") as f:
    skilltree_data = json.load(f)

skill_rows = skilltree_data[0]["Rows"]

perk_output = {}

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
    return line.strip()

for skill_name, skill_data in skill_rows.items():
    perk_enum = skill_data.get("PerkID_25_4BC92A00469A851AA5FE2792BE9F96C4") #you need this specific one

    if perk_enum in perk_id_to_name:
        perk_name = perk_id_to_name[perk_enum]
        tooltips = skill_data.get("Tooltip_54_1E2214584583FA289C1781AA8CE4153E", []) #same here
        if not tooltips:
            continue

        tooltip_text = tooltips[-1]["LocalizedString"]

        lines = [
            format_line(line)
            for line in tooltip_text.strip().splitlines()
            if line.strip()
        ]
        perk_output[perk_name] = lines

# Save to JSON
with open("augments.json", "w", encoding="utf-8") as out_file:
    json.dump(perk_output, out_file, indent=2, ensure_ascii=False)

print("Shit's working")

#BTH ID: "Body_10_68FBC6C34B6DDB19E010A9AB2419B88B"
#"Tech_11_D9A98AA74B87F1DD6B0F43B4233753BC"
#"Hardware_12_9310D7DB447E651E58D0268CC41AC3B7"