#
# Author - kyroh
# 
# This source code is licensed under the Attribution-NonCommercial-ShareAlike 4.0 International license found in the LICENSE file in the root directory of this source tree.
# 
# May 2023
#

import os
import json
from components.inputs import UserInputs
from components.standard import StandardAbility
from components.bleeds import BleedAbility
from components.channeled import ChanneledAbility
from components.on_hit_buffs import OnHitBuffs
from components.crit_chance import CriticalHitChance
from components.ability_dmg import AbilityDmg

class Rotation:
    def __init__(self):
        with open(os.path.join('user', 'rotation.json'), 'r') as r:
            self.rotation = json.load(r)
        
        with open(os.path.join('utils', 'timing.json'), 'r') as t:
            self.timing = json.load(t)

        self.timing_dict = {abil['name']: abil for abil in self.timing}

    def rotation_data(self):
        rotation_dict = []
        
        for entry in self.rotation:
            ability_name = entry['name']
            cast_tick = entry['tick']
            weapon = entry['type']
            inputs = UserInputs(ability_name, weapon)
            params = inputs.get_abil_params()
            if params[4] == 'SINGLE_HIT_ABIL':
                ref = OnHitBuffs(ability_name, cast_tick, weapon)
                ability = ref.hits()
            elif params[4] == 'BLEED':
                ref = BleedAbility(ability_name, cast_tick, weapon)
                ability = ref.hits()
            elif params[4] == 'CHANNELED':
                ref = ChanneledAbility(ability_name, cast_tick, weapon)
                ability = ref.hits()
            else:
                ability = {"tick": cast_tick, "dmg": 0}
                    
            hit_dict = {"name": ability_name}
            hit_dict.update(ability)
            rotation_dict.append(hit_dict)

        return rotation_dict


    
    def dmg_json(self):
        dmg_dict = self.rotation_data()
        
        json_data = json.dumps(dmg_dict, indent=4)
        
        with open('dmg.json', 'w') as file:
            file.write(json_data)
        
        print('Json Saved')
        
test = ChanneledAbility('assault', 3, '2h')
dmg = test.barge_check()

print(dmg)