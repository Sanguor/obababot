import json
import re
import sys


ROM = sys.argv[1]

with open(r"text\GStext.txt") as f:
    text = f.read().splitlines()
    item_descriptions = text[146:607]
    items = text[607:1068]
    items = [re.search(r"[^{}]*$", s).group() for s in items]
    enemynames = text[1068:1447]
    moves = text[1447:2181]
    move_descriptions = text[2181:2915]
    classes = text[2915:3159]
    djinn = text[1747:1827]
    summons = text[1827:1860]
    pcnames = ["Isaac", "Garet", "Ivan", "Mia", "Felix", "Jenna", "Sheba", "Piers"]
    elements = ["Venus", "Mercury", "Mars", "Jupiter", "Neutral"]
    itemtypes = [
        "Other", "Weapon", "Armor", "Armgear", "Headgear", "Boots", "Psy-item", 
        "Trident", "Rings", "Shirts", "Class-item", "Elemental Star",
    ]

with open(r"text\customtext.txt") as f:
    text = f.read().splitlines()
    ability_effects = text[0:92]
    equipped_effects = text[92:120]

with open(ROM, "rb") as f:
    def read(size):
        return int.from_bytes(f.read(size), "little")
    
    f.seek(0x0B2364)  # item data
    itemdata = []
    for i in range(461):
        itemdata.append({
            "ID": i,
            "name": items[i],
            "price": read(2),
            "item_type": itemtypes[read(1)],
            "flags": read(1),
            "equippable_by": read(1),
            "unused": read(1),
            "icon": read(2),
            "attack": read(2),
            "defense": read(1),
            "unleash_rate": read(1),
            "use_type": read(1),
            "unused": read(1),
            "unleash_ability": read(2),
            "unused": read(4),
            "element": elements[read(4)],
            "equipped_effects": [[read(1), read(1), read(2)] for i in range(4)],
            "effect_values": [],
            "use_ability": read(2),
            "unused": read(2),
            "dropped_by": [],
            "description": item_descriptions[i],
        })

    f.seek(0x0B7C14)  # ability data
    abilitydata = []
    for i in range(734):
        abilitydata.append({
            "ID": i,
            "name": moves[i],
            "target": read(1),
            "flags": read(1),
            "damage_type": None,
            "element": elements[read(1)],
            "ability_effect": ability_effects[read(1)],
            "icon": read(2),
            "utility": read(1),
            "unused": read(1),
            "range": read(1),
            "PP_cost": read(1),
            "power": read(2),
            "description": move_descriptions[i]
        })

    f.seek(0x0B9E7C)  # enemy data
    enemydata = []
    for i in range(379):
        enemydata.append({
            "ID": i,
            "name": enemynames[i],
            "unused": read(15),
            "level": read(1),
            "HP": read(2),
            "PP": read(2),
            "ATK": read(2),
            "DEF": read(2),
            "AGI": read(2),
            "LCK": read(1),
            "turns": read(1),
            "HP_regen": read(1),
            "PP_regen": read(1),
            "items": [read(2) for i in range(4)],
            "item_quantities": [read(1) for i in range(4)],
            "elemental_stats_id": read(1),
            "IQ": read(1),
            "attack_pattern": read(1),
            "item_priority_flags": read(1),
            "abilities": [moves[read(2)] for i in range(8)],
            "weaknesses": [read(1) for i in range(3)],
            "unused": read(1),
            "coins": read(2),
            "item_drop": read(2),
            "item_chance_class": read(2),
            "exp": read(2),
            "unused": read(2),
        })

    f.seek(0x0C0F4C)  # pc data
    pcdata = []
    for i in range(8):
        pcdata.append({
            "ID": i,
            "name": pcnames[i],
            "element": elements[[0,2,3,1,0,2,3,1][i]],
            "unused": read(80),
            "HP_growths": [read(2) for i in range(6)],
            "PP_growths": [read(2) for i in range(6)],
            "ATK_growths": [read(2) for i in range(6)],
            "DEF_growths": [read(2) for i in range(6)],
            "AGI_growths": [read(2) for i in range(6)],
            "LCK_growths": [read(1) for i in range(6)],
            "elevels": [read(1)/10 for i in range(4)],
            "starting_level": read(2),
            "starting_items": [read(2) for i in range(14)],
        })

    f.seek(0x0C150C)  # summon data
    summondata = []
    for i in range(30):
        moveID = read(4)
        if i == 25: moveID += 1
        move = abilitydata[moveID]
        summondata.append({
            "ID": i,
            "name": move["name"],
            "element": move["element"],
            "Venus": read(1),
            "Mercury": read(1),
            "Mars": read(1),
            "Jupiter": read(1),
            "ability_effect": move["ability_effect"],
            "icon": move["icon"],
            "range": move["range"],
            "power": move["power"],
            "hp_multiplier": None,
            "description": move["description"],
        })
        if i == 24: f.seek(-0x8, 1)

    f.seek(0x0C15F4)  # class data
    classdata = []
    for i in range(244):
        classdata.append({
            "ID": i,
            "name": classes[i],
            "class_group": read(4),
            "Venus": read(1),
            "Mercury": read(1),
            "Mars": read(1),
            "Jupiter": read(1),
            "HP": read(1),
            "PP": read(1),
            "ATK": read(1),
            "DEF": read(1),
            "AGI": read(1),
            "LCK": read(1),
            "unused": read(2),
            "abilities": [(read(2), read(2)) for i in range(16)],
            "weaknesses": [read(1) for i in range(3)],
            "unused": read(1),
        })

    f.seek(0x0C6684)  # elemental data
    elementdata = []
    for i in range(48):
        elementdata.append({
            "ID": i,
            "unused": read(4),
            "Venus_lvl": read(1),
            "Mercury_lvl": read(1),
            "Mars_lvl": read(1),
            "Jupiter_lvl": read(1),
            "Venus_Pow": read(2),
            "Venus_Res": read(2),
            "Mercury_Pow": read(2),
            "Mercury_Res": read(2),
            "Mars_Pow": read(2),
            "Mars_Res": read(2),
            "Jupiter_Pow": read(2),
            "Jupiter_Res": read(2),
        })
    
    f.seek(0x0C6BB0)  # djinn data
    djinndata = []
    for i in range(80):
        djinndata.append({
            "ID": i,
            "name": djinn[i],
            "element": elements[i//20],
            "ability": read(2),
            "damage_type": None,
            "effect": None,
            "target": None,
            "power": None,
            "unused": read(2),
            "HP": read(1),
            "PP": read(1),
            "ATK": read(1),
            "DEF": read(1),
            "AGI": read(1),
            "LCK": read(1),
            "description": None,
            "unused": read(2),
        })

    f.seek(0x0EDACC)  # encounter data
    encounterdata = []
    for i in range(110):
        encounterdata.append({
            "ID": i,
            "rate": read(2),
            "level": read(2),
            "enemy_groups": [read(2) for i in range(8)],
            "group_ratios": [read(1) for i in range(8)],
        })

    f.seek(0x12CE7C)  # enemy group data
    enemygroupdata = []
    for i in range(660):
        enemygroupdata.append({
            "ID": i,
            "enemies": [enemynames[read(2)] for i in range(5)],
            "min_amounts": [read(1) for i in range(5)],
            "max_amounts": [read(1) for i in range(5)],
            "positioning": read(1),
            "unused": read(3),
        })


for item in itemdata:
    item.pop("unused")
    item["effect_values"] = [i[1] for i in item["equipped_effects"] if i[0]]
    item["equipped_effects"] = [equipped_effects[i[0]]for i in item["equipped_effects"] if i[0]]
    item["equippable_by"] = [pcnames[i] for i in range(8) if item["equippable_by"] & 2**i]
    flagdesc = ["Curses when equipped", "Can't be removed", "Rare item", "Important item",
        "Stackable", "Not transferable"]
    item["flags"] = [flagdesc[i] for i in range(6) if item["flags"] & 2**i]
    usetypes = ["Multi-Use", "Consumable", "Can Break", "Bestows ability", "Item transforms when used"]
    item["use_type"] = usetypes[item["use_type"]]

for move in abilitydata:
    move.pop("unused")
    move["target"] = ["Utility", "Enemies", "Allies", "?", "Self"][move["target"]]
    damagetypes = [
        "?", "Healing","Effect Only","Added Damage","Multiplier","Base Damage",
        "Base Damage (Diminishing)","Djinn Effect","Summon","Utility",
        "Psynergy Drain","Psynergy Recovery"]
    move["damage_type"] = damagetypes[move["flags"] & 0xF]
    move["flags"] = move["flags"] >> 4
    flagdesc = ["", "", "usable out of battle", "usable in battle"]
    move["flags"] = [flagdesc[i] for i in range(2, 4) if move["flags"] & 2**i]

for enemy in enemydata:
    enemy.pop("unused")
    enemy["items"] = [items[i] for i in enemy["items"] if i]
    enemy["item_quantities"] = [i for i in enemy["item_quantities"] if i != 0]
    if enemy["name"] in ("Dullahan", "Serpent"): enemy["HP_regen"] *= 10
    enemy["weaknesses"] = [ability_effects[i] for i in enemy["weaknesses"] if i]
    itemID = enemy["item_drop"]
    if itemID: itemdata[itemID]["dropped_by"].append(enemy["name"])
    enemy["item_drop"] = items[itemID]

for pc in pcdata:
    pc.pop("unused")
    pc["starting_items"] = [items[i] for i in pc["starting_items"] if i]

for summon in summondata:
    summon["hp_multiplier"] = sum(summon[k] for k in elements[0:4])*0.03
    if summon["ID"] == 24: summon["hp_multiplier"] = 0.07
    if summon["ID"] == 25: summon["hp_multiplier"] = 0.15
    if summon["ID"] == 29: summon["hp_multiplier"] = 0.40

for class_ in classdata:
    class_.pop("unused")
    class_["abilities"] = {moves[k]: v for k,v in class_["abilities"] if k != 0}
    classgroups = [
        "", "Squire", "Guard", "Swordsman", "Brute",
        "Apprentice", "Water Seer", "Wind Seer", "Seer",
        "Pilgrim", "Hermit", "", "NPC", "Flame User",
        "Mariner", "Pierrot", "Tamer", "Dark Mage"
    ]
    class_["class_group"] = classgroups[class_["class_group"]]
    class_["weaknesses"] = [ability_effects[i] for i in class_["weaknesses"] if i]
    for k in ["HP", "PP", "ATK", "DEF", "AGI", "LCK"]:
        class_[k] /= 10

for entry in elementdata:
    entry.pop("unused")

for djinni in djinndata:
    djinni.pop("unused")
    move = abilitydata[djinni["ability"]]
    djinni["damage_type"] = move["damage_type"]
    djinni["effect"] = move["ability_effect"]
    djinni["target"] = move["target"]
    djinni["power"] = move["power"]
    djinni["description"] = move["description"]

for group in enemygroupdata:
    group.pop("unused")
    entries = [i for i in range(5) if group["enemies"][i] != "???"]
    group["enemies"] = [group["enemies"][i] for i in entries]
    group["min_amounts"] = [group["min_amounts"][i] for i in entries]
    group["max_amounts"] = [group["max_amounts"][i] for i in entries]


for name in [
        "djinndata", "enemydata", "itemdata", "abilitydata", "pcdata", "summondata",
        "classdata", "elementdata", "enemygroupdata", "encounterdata"
    ]:
    with open(f"data\\{name}.json", "w") as f: json.dump(globals()[name], f, indent=4)
