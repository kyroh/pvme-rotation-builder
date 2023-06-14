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
from components.fcrit_chance import fcrit
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
            inputs = UserInputs(ability_name)
            params = inputs.get_abil_params()
            abil = self.timing_dict.get(ability_name)
            if abil and abil['name'] == ability_name:
                if inputs.type == '2h':
                    hit_tick = cast_tick + abil['2h tick']
                elif inputs.type in ['dw', 'ms']:
                    hit_tick = cast_tick + abil['dw tick']
                else:
                    continue

                if params[4] == 'SINGLE_HIT_ABIL':
                    ability = StandardAbility(ability_name, cast_tick)
                elif params[4] == 'BLEED':
                    ability = BleedAbility(ability_name, cast_tick)
                elif params[4] == 'CHANNELED':
                    ability = ChanneledAbility(ability_name, cast_tick)
                else:
                    continue

                hits = ability.hits()
                hit_dict = {"name": ability_name}
                hit_dict.update(hits)
                rotation_dict.append(hit_dict)

        return rotation_dict


    
    def dmg_json(self):
        dmg_dict = self.rotation_data()
        
        json_data = json.dumps(dmg_dict, indent=4)
        
        with open('dmg.json', 'w') as file:
            file.write(json_data)
        
        print('Json Saved')
        
test = Rotation()
dmg = test.dmg_json()
        
