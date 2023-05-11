import json
import math

with open("weapons.json", "r") as f:
    weapons = json.load(f)

weapon_name = input("Enter the weapon name:\n")
level = float(input("Enter your magic level:\n"))
bonus = 0

def compute_base_ability_dmg():
    weapon = None
    for w in weapons:
        if w["name"] == weapon_name:
            weapon = w
            break
    if weapon is None:
        pass
    if weapon["type"] == "mh":
        base_ability_dmg = math.floor(2.5 * level) + weapon["dmg"] + bonus
        print('your ability damage is: ', base_ability_dmg)
    elif weapon["type"] == "oh":
        base_ability_dmg = math.floor(1.25 * level) + weapon["dmg"] + math.floor(.5 * bonus)
        print('your ability damage is: ', base_ability_dmg)
    elif weapon["type"] == "2h":
        base_ability_dmg = math.floor(3.75 * level) + weapon["dmg"] + math.floor(1.5 * bonus)
        print('your ability damage is: ', base_ability_dmg)
    else:
        pass

compute_base_ability_dmg()