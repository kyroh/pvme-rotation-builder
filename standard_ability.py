#
# Author - kyroh
# 
# This source code is licensed under the Attribution-NonCommercial-ShareAlike 4.0 International license found in the LICENSE file in the root directory of this source tree.
# 
#test

import os
import json
import math

class StandardAbility:
    def __init__(self):
        with open(os.path.join('utils', 'weapons.json'), 'r') as w:
            self.weapons = json.load(w)
        
        with open(os.path.join('utils', 'boosts.json'), 'r') as b:
            self.boosts = json.load(b)

        with open(os.path.join('utils', 'abilities.json'), 'r') as a:
            self.abilities = json.load(a)

        self.mh_input = 'Wand of the praesul'
        self.oh_input = 'Imperium core'
        self.th_input = 'Staff of Sliske'
        self.base_magic_level = 99
        self.base_range_level = 99
        self.base_strength_level = 99
        self.aura_input = 'None'
        self.potion_input = 'None'
        self.bonus = 0

    def aura_level_boost(self):
        boost = None
        for b in self.boosts:
            if b['name'] == self.aura_input:
                boost = b
                break
        if boost is None:
            pass
        magic_boost_percent = 0
        range_boost_percent = 0
        strength_boost_percent = 0
        if boost['magic_level_percent'] != 0:
            magic_boost_percent = self.base_magic_level * boost['magic_level_percent']
        elif boost['range_level_percent'] != 0:
            range_boost_percent = self.base_range_level * boost['range_level_percent']
        elif boost['strength_level_percent'] != 0:
            strength_boost_percent = self.base_strength_level * boost['strength_level_percent']
        else:
            pass
        return [magic_boost_percent, range_boost_percent, strength_boost_percent]

    def potion_level_boost(self):
        boost = None
        for b in self.boosts:
            if b['name'] == self.potion_input:
                boost = b
                break
        if boost is None:
            pass
        magic_boost_percent = 0
        range_boost_percent = 0
        strength_boost_percent = 0
        magic_boost = 0
        range_boost = 0
        strength_boost = 0
        if boost['magic_level_percent'] != 0:
            magic_boost_percent = self.base_magic_level * boost['magic_level_percent']
        if boost['range_level_percent'] != 0:
            range_boost_percent = self.base_range_level * boost['range_level_percent']
        if boost['strength_level_percent'] != 0:
            strength_boost_percent = self.base_strength_level * boost['strength_level_percent']
        if boost['magic_level_boost'] != 0:
            magic_boost = boost['magic_level_boost']
        if boost['range_level_boost'] != 0:
            range_boost = boost['range_level_boost']
        if boost['strength_level_boost'] != 0:
            strength_boost = boost['strength_level_boost']
        net_magic_boost = magic_boost_percent + strength_boost
        net_range_boost = range_boost_percent + range_boost
        net_strength_boost = strength_boost_percent + magic_boost
        return [net_magic_boost, net_range_boost, net_strength_boost]
    
    def calculate_levels(self):
        aura_boosts = self.aura_level_boost()
        potion_boosts = self.potion_level_boost()
        base_levels = [self.base_magic_level, self.base_range_level, self.base_strength_level]
        total_levels = []
        for x, y, z in zip(aura_boosts, potion_boosts, base_levels):
            total_levels.append(math.floor(x + y + z))
        return total_levels
    
    def dw_ability_dmg(self):
        boost = StandardAbility()
        levels = boost.calculate_levels()
        magic_level = levels[0]
        range_level = levels[1]
        strength_level = levels[2]
        
        mh = None
        oh = None
        
        for w in self.weapons:
            if w['name'] == self.mh_input:
                mh = w
                break
        if mh is None:
            pass
        if mh['style'] == 'magic':
            mh_ability_dmg = math.floor(2.5 * magic_level) + mh['dmg'] + self.bonus
        elif mh['style'] == 'range':
            mh_ability_dmg = math.floor(2.5 * range_level) + mh['dmg'] + self.bonus
        elif mh['style'] == 'melee':
            mh_ability_dmg = math.floor(2.5 * strength_level) + mh['dmg'] + self.bonus
        else:
            pass
        
        for w in self.weapons:
            if w['name'] == self.oh_input:
                oh = w
                break
        if oh is None:
            pass
        elif oh['style'] == 'magic':
            oh_ability_dmg = math.floor(1.25 * magic_level) + oh['dmg'] + math.floor(0.5 * self.bonus)
        elif oh['style'] == 'range':
            oh_ability_dmg = math.floor(1.25 * range_level) + oh['dmg'] + math.floor(0.5 * self.bonus)
        elif oh['style'] == 'melee':
            oh_ability_dmg = math.floor(1.25 * strength_level) + oh['dmg'] + math.floor(0.5 * self.bonus)
        else:
            pass
        
        base_ability_dmg = mh_ability_dmg + oh_ability_dmg
        return base_ability_dmg
        
    def th_ability_dmg(self):
        levels = self.calculate_levels()
        magic_level = levels[0]
        range_level = levels[1]
        strength_level = levels[2]
        
        th = None 
        
        for w in self.weapons:
            if w['name'] == self.th_input:
                th = w
                break
        if th is None:
            pass
        if th['style'] == 'magic':
            base_ability_dmg = math.floor(3.75 * magic_level) + th['dmg'] + math.floor(1.5 * self.bonus)
        elif th['style'] == 'range':
            base_ability_dmg = math.floor(3.75 * range_level) + th['dmg'] + math.floor(1.5 * self.bonus)
        elif th['style'] == 'melee':
            base_ability_dmg = math.floor(3.75 * strength_level) + th['dmg'] + math.floor(1.5 * self.bonus)
        else:
            pass
        return base_ability_dmg
    
    def ms_ability_dmg(self):
        boosted_levels = self.calculate_levels()
        boosted_magic_level = boosted_levels[0]
        boosted_range_level = boosted_levels[1]
        boosted_strength_level = boosted_levels[2]
        
        mh = None 
        
        for w in self.weapons:
            if w['name'] == self.mh_input:
                mh = w
                break
        if mh is None:
            pass
        if mh['style'] == 'magic':
            base_ability_dmg = math.floor(2.5 * boosted_magic_level) + mh['dmg'] + self.bonus
        elif mh['style'] == 'range':
            base_ability_dmg = math.floor(2.5 * boosted_range_level) + mh['dmg'] + self.bonus
        elif mh['style'] == 'melee':
            base_ability_dmg = math.floor(2.5 * boosted_strength_level) + mh['dmg'] + self.bonus
        else:
            pass
        return base_ability_dmg
    
    def casting_weapon(self):
        weapon_type = (input(f'Select which weapons you will be casting with:\n1.Dual wield\n2.Two hand\n3.Mainhand shield\n'))
        if weapon_type == '1':
            base_ability_dmg = self.dw_ability_dmg()
        elif weapon_type == '2':
            base_ability_dmg = self.th_ability_dmg()
        elif weapon_type == '3':
            base_ability_dmg = self.ms_ability_dmg()
        else:
            pass 
        return base_ability_dmg
    
    def casting_style(self):
        weapon_type = (input(f'Select which weapons you will be casting with:\n1.magic\n2.range\n3.melee\n'))
        if weapon_type == '1':
            style = '1'
        elif weapon_type == '2':
            style = '2'
        elif weapon_type == '3':
            style = '3'
        else:
            pass 
        return style
    
    def dpl_fixed(self):
        base_ability_dmg = self.casting_weapon

    def dpl_var(self): 
        pass

    def net_ability_dmg(self):
        base_ability_dmg = self.casting_weapon()
        style = self.casting_style()
        boosted_levels = self.calculate_levels()
        boosted_magic_level = boosted_levels[0]
        boosted_range_level = boosted_levels[1]
        boosted_strength_level = boosted_levels[2]
        
        if style == '1':
            ability_dmg = math.floor(((base_ability_dmg * 1.88) + (boosted_magic_level - self.base_magic_level) * 8))
        elif style == '2':
            ability_dmg = math.floor(base_ability_dmg * 1.12) + math.floor(boosted_range_level - self.base_range_level) * 8
        elif style == '3':
            ability_dmg = math.floor(base_ability_dmg * 1.12) + math.floor(boosted_strength_level - self.base_strength_level) * 8
        else:
            pass
        return ability_dmg
    
    def hexhunter(self):
        hexhunter = 0
        
        if self.th_input == 'Inquisitor staff':
            hexhunter = 1
        elif self.th_input == 'Hexhunter bow':
            hexhunter = 2
        elif self.th_input == 'Terrasaur maul':
            hexhunter = 3
        return hexhunter
    
    def prayer(self):
        pass
    
    def aura_passive(self):
        pass
    
    def sunshine(self):
        pass
    

test = StandardAbility()
test_dmg = test.net_ability_dmg()
print(test_dmg)
