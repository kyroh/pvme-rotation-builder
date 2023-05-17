#
# Author - kyroh
# 
# This source code is licensed under the Attribution-NonCommercial-ShareAlike 4.0 International license found in the LICENSE file in the root directory of this source tree.
# 
#

import random
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
        self.th_input = 'Noxious staff'
        self.base_magic_level = 99
        self.base_range_level = 99
        self.base_strength_level = 99
        self.aura_input = 'None'
        self.potion_input = 'None'
        self.bonus = 12
        self.ability_input = input('Enter and ability to cast:\n')
        self.prayer_input = 'None'
        self.precise_rank = 6
        self.equilibrium_rank = 4

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
        if boost['range_level_percent'] != 0:
            range_boost_percent = self.base_range_level * boost['range_level_percent']
        if boost['strength_level_percent'] != 0:
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
        levels = self.calculate_levels()
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
    
    def standard_ability(self):
        ability = None
        
        for a in self.abilities:
            if a['name'] == self.ability_input:
                ability = a
                break
        if ability is None:
            pass
        if ability['type'] == 'standard':
            min_dmg = ability['min']
            max_dmg = ability['max']
        else:
            pass
        return [min_dmg, max_dmg]
    
    def df(self):
        base_ability_dmg = self.th_ability_dmg()
        style = 'magic'
        min_max = self.standard_ability()
        prayer_boost = self.prayer_dmg()
        magic_prayer = prayer_boost[0]
        range_prayer = prayer_boost[1]
        melee_prayer = prayer_boost[2]
        min_dmg = min_max[0]
        
        if style == 'magic':
            df = math.floor(base_ability_dmg * (min_dmg * (1 + magic_prayer)))
        elif style == 'range':
            df = math.floor(base_ability_dmg * (min_dmg * (1 + range_prayer)))
        elif style == 'melee':
            df = math.floor(base_ability_dmg * (min_dmg * (1 + melee_prayer)))
        else:
            pass
        return df
    
    def dv(self):
        base_ability_dmg = self.th_ability_dmg()
        style = 'magic'
        min_max = self.standard_ability()
        prayer_boost = self.prayer_dmg()
        magic_prayer = prayer_boost[0]
        range_prayer = prayer_boost[1]
        melee_prayer = prayer_boost[2]
        min_dmg = min_max[0]
        max_dmg = min_max[1]
        
        if style == 'magic':
            dv = math.floor(base_ability_dmg * ((max_dmg - min_dmg) * (1 + magic_prayer)))
        elif style == 'range':
            dv = math.floor(base_ability_dmg * ((max_dmg - min_dmg) * (1 + range_prayer)))
        elif style == 'melee':
            dv = math.floor(base_ability_dmg * ((max_dmg - min_dmg) * (1 + melee_prayer)))
        else:
            pass
        return dv
    
    def dpl_f(self):
        df = self.df()
        style = 'magic'
        levels = self.calculate_levels()
        boosted_magic = levels[0]
        boosted_range = levels[1]
        boosted_strength = levels[2]
        
        if style == 'magic':
            dpl_f = math.floor(df + (4 * max(0, boosted_magic - self.base_magic_level)))
        elif style == 'range':
            dpl_f = math.floor(df + (4 * max(0, boosted_range - self.base_range_level)))
        elif style == 'melee':
            dpl_f = math.floor(df + (4 * max(0, boosted_strength - self.base_strength_level)))
        else:
            pass
        return dpl_f
    
    def dpl_v(self):
        dv = self.dv()
        style = 'magic'
        levels = self.calculate_levels()
        boosted_magic = levels[0]
        boosted_range = levels[1]
        boosted_strength = levels[2]
        
        if style == 'magic':
            dpl_v = math.floor(dv + (4 * max(0, boosted_magic - self.base_magic_level)))
        elif style == 'range':
            dpl_v = math.floor(dv + (4 * max(0, boosted_range - self.base_range_level)))
        elif style == 'melee':
            dpl_v = math.floor(dv + (4 * max(0, boosted_strength - self.base_strength_level)))
        else:
            pass
        return dpl_v
    
    def hexhunter(self):
        hexhunter = 0
        
        if self.th_input == 'Inquisitor staff':
            hexhunter = 1
        elif self.th_input == 'Hexhunter bow':
            hexhunter = 2
        elif self.th_input == 'Terrasaur maul':
            hexhunter = 3
        return hexhunter
    
    def prayer_dmg(self):
        boost = None
        for b in self.boosts:
            if b['name'] == self.prayer_input:
                boost = b
                break
        if boost is None:
            pass
        
        prayer_dmg = [b["magic_dmg_percent"], b["range_dmg_percent"], b["strength_dmg_percent"]]
        
        return prayer_dmg
    
    def aura_passive(self):
        boost = None
        for b in self.boosts:
            if b['name'] == self.aura_input:
                boost = b
                break
        if boost is None:
            pass
        magic_dmg_percent = 1
        range_dmg_percent = 1
        strength_dmg_percent = 1
        if boost['magic_dmg_percent'] != 0:
            magic_dmg_percent = 1 + boost['magic_dmg_percent']
        if boost['range_dmg_percent'] != 0:
            range_dmg_percent = 1 + boost['range_dmg_percent']
        if boost['strength_dmg_percent'] != 0:
            strength_dmg_percent = 1 + boost['strength_dmg_percent']
        else:
            pass
        return [magic_dmg_percent, range_dmg_percent, strength_dmg_percent]
    
    def sunshine(self):
        pass
    
    def roll_dmg(self):
        dpl_v = self.dpl_v()
        dpl_f = self.dpl_f()
        min_dmg = dpl_f
        max_dmg = dpl_f + dpl_v
        
        roll = random.randint(min_dmg,max_dmg)
        
        return roll

    def precise(self):
        dpl_f = self.dpl_f()
        dpl_v = self.dpl_v()
        max_dmg = dpl_f + dpl_v
        rank = self.precise_rank
        precise = rank * 0.015
        
        if self.precise_rank == '0':
            pr_f = 0
        else:
            pr_f = math.floor(max_dmg * precise)
        return pr_f
    
    def equilibrium(self):
        dpl_f= self.dpl_f()
        dpl_v = self.dpl_v()
        rank = self.equilibrium_rank
        modifier_min = rank * 0.03
        modifier_max = rank * 0.04
        bonus = math.floor(modifier_min * dpl_v)
        reduct = math.floor(modifier_max * dpl_v)
        
        if self.equilibrium_rank == '0':
            equilibrium_f = dpl_f
            equilibrium_v = dpl_v
        else:
            equilibrium_f = math.floor(modifier_min * dpl_v)
            equilibrium_v = math.floor(modifier_max * dpl_v)
        return [equilibrium_f, equilibrium_v]
    
    def floor(self):
        dpl_f = self.dpl_f()
        pr_f = self.precise()
        equilibrium = self.equilibrium()
        eq_f = equilibrium[0]
   
        floor = dpl_f + pr_f + eq_f
        
        return floor
    
    def ceil(self):
        equilibrium = self.equilibrium()
        eq_f = equilibrium[0]
        eq_v = equilibrium[1]
        dpl_f = self.dpl_f()
        dpl_v = self.dpl_v()
        
        ceil = eq_f + dpl_f + dpl_v - eq_v
        
        return ceil
    
test = StandardAbility()

dmg = test.th_ability_dmg()

print(dmg)



