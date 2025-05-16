import json
import re
with open("augments.json", "r", encoding="utf-8") as f:
    enum_data = json.load(f)

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

def format_everything(obj):
    if isinstance(obj, str):
        return format_line(obj)
    elif isinstance(obj, list):
        return [format_everything(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: format_everything(value) for key, value in obj.items()}
    else:
        return obj


perk_output = format_everything(enum_data)

# Save to JSON
with open("augments_dc.json", "w", encoding="utf-8") as out_file:
    json.dump(perk_output, out_file, indent=2, ensure_ascii=False)

print("Shit's working")