import os
import json

class UserInputs:
    def __init__(self, ability):
        self.abilities = self.load_json("utils", "abilities.json")
        self.gear = self.load_json("utils", "gear.json")
        self.user_gear = self.load_json("user", "user_gear.json")
        self.bleeds = self.load_json("utils", "bleeds.json")
        self.channels = self.load_json("utils", "channels.json")
        self.weapons = self.load_json("utils", "weapons.json")
        self.timing = self.load_json("utils", "timing.json")
        self.boosts = self.load_json("utils", "boosts.json")
        self.rotation = self.load_json("user", "rotation.json")

        self.ability_input = ability
        
        self.type = '2h'
        self.reaper_crew = True
        self.gear_input = self.user_gear[2]
        self.mh_input = self.user_gear[1]["mh"]
        self.oh_input = self.user_gear[1]["oh"]
        self.th_input = self.user_gear[1]["2h"]
        self.shield_input = self.user_gear[1]["shield"]
        self.spell_input = self.user_gear[0]["spell"]
        self.base_magic_level = self.user_gear[0]["magic level"]
        self.base_range_level = self.user_gear[0]["range level"]
        self.base_strength_level = self.user_gear[0]["strength level"]
        self.aura_input = self.user_gear[0]["aura"]
        self.potion_input = self.user_gear[0]["potion"]
        self.prayer_input = self.user_gear[1]["prayer"]
        self.pocket = self.user_gear[2]["pocket"]
        self.precise_rank = 6
        self.equilibrium_rank = 2
        self.lunging_rank = 0
        self.biting_rank = 4
        self.dmg_output = 'MIN'
        
        self.abil_params = self.get_abil_params()
        self.name = self.abil_params[0]
        self.fixed_dmg = self.abil_params[1]
        self.var_dmg = self.abil_params[2]
        self.style = self.abil_params[3]
        self.type_n = self.abil_params[4]
        self.class_n = self.abil_params[5]

        self.bonus = self.compute_bonus()
        self.magic_bonus = self.bonus[0]
        self.range_bonus = self.bonus[1]
        self.melee_bonus = self.bonus[2]

    def get_abil_params(self):
        abil = next((a for a in self.abilities if a['name'] == self.ability_input), None)
        if abil is None:
            return []

        ability_name = abil['name']
        fixed_dmg = abil['fixed']
        var_dmg = abil['var']
        style = abil['style']
        type_n = abil['type_n']
        class_n = abil['class_n']

        return [ability_name, fixed_dmg, var_dmg, style, type_n, class_n]
    
    def compute_bonus(self):
        bonus = [0, 0, 0]
        gear_slots = {
            'helm': 'helm',
            'body': 'body',
            'legs': 'legs',
            'boots': 'boots',
            'gloves': 'gloves',
            'neck': 'neck',
            'cape': 'cape',
            'ring': 'ring',
            'pocket': 'pocket'        
        }

        for item in self.gear:
            slot = item['slot']
            if item['name'] == self.gear_input.get(gear_slots.get(slot)):
                bonus[0] += item['magic_bonus']
                bonus[1] += item['range_bonus']
                bonus[2] += item['melee_bonus']
           
        if self.reaper_crew == True:
            bonus[0] += 12
            bonus[1] += 12
            bonus[2] += 12
        return bonus
    
    def load_json(self, directory, filename):
        file_path = os.path.join(directory, filename)
        with open(file_path, "r") as file:
            return json.load(file)
