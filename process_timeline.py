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
    
    def rotation_data(self):
        rotation_dict = []
        
        for entry in self.rotation:
            ability_name = entry['name']
            cast_tick = entry['tick']
            inputs = UserInputs(ability_name, cast_tick)
            params = inputs.get_abil_params()

            if params[4] == 'SINGLE_HIT_ABIL':
                stand = StandardAbility(ability_name, cast_tick)
                hits = stand.hits()
                hit_dict = {"name": ability_name}
                for i, hit in enumerate(hits, start = 1):
                    hit_dict[f"hit {i}"] = hit
                rotation_dict.append(hit_dict)
            elif params[4] == 'BLEED':
                bleed = BleedAbility(ability_name, cast_tick)
                hits = bleed.hits()
                hit_dict = {"name": ability_name}
                for i, hit in enumerate(hits, start = 1):
                    hit_dict[f"hit {i}"] = hit
                rotation_dict.append(hit_dict)
            elif params[4] == 'CHANNELED':
                chan = ChanneledAbility(ability_name, cast_tick)
                hits = chan.hits()
                hit_dict = {"name": ability_name}
                for i, hit in enumerate(hits, start = 1):
                    hit_dict[f"hit {i}"] = hit
                rotation_dict.append(hit_dict)
            else:
                pass
        return rotation_dict
    
    def dmg_json(self):
        dmg_dict = self.rotation_data()
        
        json_data = json.dumps(dmg_dict, indent=4)
        
        with open('dmg.json', 'w') as file:
            file.write(json_data)
        
        print('Json Saved')
        
test = Rotation()
dmg = test.dmg_json()

        
