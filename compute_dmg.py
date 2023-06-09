#
# Author - kyroh
# 
# This source code is licensed under the Attribution-NonCommercial-ShareAlike 4.0 International license found in the LICENSE file in the root directory of this source tree.
# 
# May 2023
#

import json
from inputs import UserInputs
from standard import StandardAbility
from bleeds import BleedAbility
from channeled import ChanneledAbility


class OnHitEffects:
    pass      
            

class ability_info:
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

class Rotation:
    def rotation_data(self):
        rotation_dict = []
        
        for entry in self.inputs.rotation:
            ability_name = entry['name']
            inputs = UserInputs()
            params = inputs.get_abil_params()

            if params[4] == 'SINGLE_HIT_ABIL':
                stand = StandardAbility()
                hits = stand.hits()
                hit_dict = {"name": ability_name}
                for i, hit in enumerate(hits, start = 1):
                    hit_dict[f"hit {i}"] = hit
                rotation_dict.append(hit_dict)
            elif params[4] == 'BLEED':
                bleed = BleedAbility()
                hits = bleed.hits()
                hit_dict = {"name": ability_name}
                for i, hit in enumerate(hits, start = 1):
                    hit_dict[f"hit {i}"] = hit
                rotation_dict.append(hit_dict)
            elif params[4] == 'CHANNELED':
                chan = ChanneledAbility()
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


        
