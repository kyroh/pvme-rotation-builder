#
# Author - Aaron Tarajos
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

        # Variables from GUI inputs
        self.ability_input = 'db'
        self.mh_input = 'Wand of the praesul'
        self.oh_input = 'Imperium core'
        self.th_input = 'Staff of Sliske'
        self.type = '2h'
        self.bonus = 12
        self.spell_input = 99
        self.base_magic_level = 99
        self.base_range_level = 99
        self.base_strength_level = 99
        self.aura_input = 'None'
        self.potion_input = 'None'
        self.prayer_input = 'None'
        self.precise_rank = 0
        self.equilibrium_rank = 0
        
        # Variables from methods
        self.boosted_levels = self.calculate_levels()
        self.boosted_magic_level = self.boosted_levels[0]
        self.boosted_range_level = self.boosted_levels[1]
        self.boosted_strength_level = self.boosted_levels[2]
        self.abil_params = self.get_abil_params()
        self.style = self.abil_params[0]
        self.class_n = self.abil_params[1]
        self.type_n = self.abil_params[2]
        self.min_dmg = self.abil_params[3]
        self.max_dmg = self.abil_params[4]
        self.ability_dmg = self.base_ability_dmg()
        self.prayer_boost = self.prayer_dmg()
        self.magic_prayer = self.prayer_boost[0]
        self.range_prayer = self.prayer_boost[1]
        self.melee_prayer = self.prayer_boost[2]
        self.aura_boost = self.aura_passive()
        self.magic_aura = self.aura_boost[0]
        self.range_aura = self.aura_boost[1]
        self.melee_aura = self.aura_boost[2]


    # Computes your boosted level from aura for ability dmg computation
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

    # Computes your boosted level from potions for ability dmg computation
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
    
    # Takes all boosts and appends it to your magic level for net boosted level
    def calculate_levels(self):
        aura_boosts = self.aura_level_boost()
        potion_boosts = self.potion_level_boost()
        base_levels = [self.base_magic_level, self.base_range_level, self.base_strength_level]
        total_levels = []
        for x, y, z in zip(aura_boosts, potion_boosts, base_levels):
            total_levels.append(math.floor(x + y + z))
        return total_levels
    
    # Computes base ability dmg for dual wield weapons
    def dw_ability_dmg(self):
        mh = None
        oh = None
        mh_ability_dmg = 0
        oh_ability_dmg = 0
        base_ability_dmg = 0
        
        for w in self.weapons:
            if w['name'] == self.mh_input:
                mh = w
                break
        if mh is None:
            pass
        if mh['style'] == 'magic':
            mh_ability_dmg = math.floor(2.5 * self.boosted_magic_level) + math.floor(9.6 * min(mh['dmg_tier'],self.spell_input) + self.bonus)
        elif mh['style'] == 'range':
            mh_ability_dmg = math.floor(2.5 * self.boosted_range_level) + math.floor(9.6 * min(mh['dmg_tier'],self.spell_input) + self.bonus)
        elif mh['style'] == 'melee':
            mh_ability_dmg = math.floor(2.5 * self.boosted_strength_level) + math.floor(9.6 * mh['dmg_tier'] + self.bonus)
        else:
            pass
        
        for w in self.weapons:
            if w['name'] == self.oh_input:
                oh = w
                break
        if oh is None:
            pass
        elif oh['style'] == 'magic':
            oh_ability_dmg = math.floor(0.5 * (math.floor(2.5 * self.boosted_magic_level) + math.floor(9.6 * min(oh['dmg_tier'],self.spell_input) + self.bonus)))
        elif oh['style'] == 'range':
            oh_ability_dmg = math.floor(0.5 * (math.floor(2.5 * self.boosted_range_level) + math.floor(9.6 * min(oh['dmg_tier'],self.spell_input) + self.bonus)))
        elif oh['style'] == 'melee':
            oh_ability_dmg = math.floor(0.5 * (math.floor(2.5 * self.boosted_strength_level) + math.floor(9.6 * oh['dmg_tier'] + self.bonus)))
        else:
            pass
        
        base_ability_dmg = mh_ability_dmg + oh_ability_dmg
        return base_ability_dmg
   
    # Computes base ability dmg for 2h weapon
    def th_ability_dmg(self):
        th = None
        base_ability_dmg = 0 
        
        for w in self.weapons:
            if w['name'] == self.th_input:
                th = w
                break
        if th is None:
            pass
        if th['style'] == 'magic':
            base_ability_dmg = math.floor(2.5 * self.boosted_magic_level) + math.floor(1.25 * self.boosted_magic_level) + math.floor(14.4 * min(th['dmg_tier'],self.spell_input) + 1.5 * self.bonus)
        elif th['style'] == 'range':
            base_ability_dmg = math.floor(2.5 * self.boosted_range_level) + math.floor(1.25 * self.boosted_range_level) + math.floor(14.4 * min(th['dmg_tier'],self.spell_input) + 1.5 * self.bonus)
        elif th['style'] == 'melee':
            base_ability_dmg = math.floor(2.5 * self.boosted_strength_level) + math.floor(1.25 * self.boosted_strength_level) + math.floor(14.4 * th['dmg_tier'] + 1.5 * self.bonus)
        else:
            pass
        return base_ability_dmg
    
    # Computes base ability dmg for Mainhand + no-offhand
    def ms_ability_dmg(self):
        mh = None
        mh_ability_dmg = 0
        
        for w in self.weapons:
            if w['name'] == self.mh_input:
                mh = w
                break
        if mh['style'] == 'magic':
            mh_ability_dmg = math.floor(2.5 * self.boosted_magic_level) + math.floor(9.6 * min(mh['dmg_tier'],self.spell_input) + self.bonus)
        elif mh['style'] == 'range':
            mh_ability_dmg = math.floor(2.5 * self.boosted_range_level) + math.floor(9.6 * min(mh['dmg_tier'],self.spell_input) + self.bonus)
        elif mh['style'] == 'melee':
            mh_ability_dmg = math.floor(2.5 * self.boosted_strength_level) + math.floor(9.6 * mh['dmg_tier'] + self.bonus)
        else:
            pass
        return mh_ability_dmg
    
    # Helper function to identify which weapons you're casting with and return the proper base ability dmg
    def base_ability_dmg(self):
        base_ability_dmg = 0
        
        if self.type == '2h':
            base_ability_dmg = self.th_ability_dmg()
        elif self.type == 'dw':
            base_ability_dmg = self.dw_ability_dmg()
        elif self.type == 'ms':
            base_ability_dmg = self.ms_ability_dmg()
        else:
            pass
        return base_ability_dmg
        ability = None
        min_dmg = 0
        max_dmg = 0
        
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
    
    # Helper function to identify the combat style and type of ability casted
    def get_abil_params(self):
        abil = None
        
        for a in self.abilities:
            if a['name'] == self.ability_input:
                abil = a
                break
        style = abil['style']
        class_n = abil['class_n']
        type_n = abil['type_n']
        min_dmg = abil['min']
        max_dmg = abil['max']
        return [style, class_n, type_n, min_dmg, max_dmg]
    
    # Computes dmg floor with prayer modifier
    def fixed(self):
        fixed = 0
        
        if self.style == 'magic':
            fixed = math.floor(self.ability_dmg * (self.min_dmg * (1 + self.magic_prayer)))
        elif self.style == 'range':
            fixed = math.floor(self.ability_dmg * (self.min_dmg * (1 + self.range_prayer)))
        elif self.style == 'melee':
            fixed = math.floor(self.ability_dmg * (self.min_dmg * (1 + self.melee_prayer)))
        else:
            pass
        return fixed
    
    # Computes variable dmg with prayer modifier
    def variable(self):
        if self.style == 'magic':
            variable = math.floor(self.ability_dmg * ((self.max_dmg - self.min_dmg) * (1 + self.magic_prayer)))
        elif self.style == 'range':
            variable = math.floor(self.ability_dmg * ((self.max_dmg - self.min_dmg) * (1 + self.range_prayer)))
        elif self.style == 'melee':
            variable = math.floor(self.ability_dmg * ((self.max_dmg - self.min_dmg) * (1 + self.melee_prayer)))
        else:
            pass
        return variable
    
    # Computes the dmg range of an abil after precise
    def precise(self):
        rank = self.precise_rank
        fixed = self.fixed()
        variable = self.variable()
        precise = 0.015 * (fixed + variable) * rank
        p_f = math.floor(fixed + precise)
        p_v = math.floor(variable - precise)
        return [p_f, p_v]
        
    # Computes the dmg range of an abil after equilibrium
    def equilibrium(self):
        precise = self.precise()
        fixed = precise[0]
        variable = precise[1]
        e_f = math.floor(fixed + (0.03 * variable * self.equilibrium_rank))
        e_v = math.floor(variable - (0.04 * variable * self.equilibrium_rank))
        return [e_f, e_v]
    
    def dpl(self):
        dmg_values = self.equilibrium()
        fixed = dmg_values[0]
        variable = dmg_values[1]
        
        if self.style == 'magic':
            dpl_f = math.floor(fixed + (self.boosted_magic_level - self.base_magic_level * 4))
            dpl_v = math.floor(fixed + (self.boosted_magic_level - self.base_magic_level * 4))
        elif self.style == 'range':
            dpl_f = math.floor(fixed + (self.boosted_range_level - self.base_range_level * 4))
            dpl_v = math.floor(fixed + (self.boosted_range_level - self.base_range_level * 4))
        elif self.style == 'melee':
            dpl_f = math.floor(fixed + (self.boosted_melee_level - self.base_melee_level * 4))
            dpl_v = math.floor(fixed + (self.boosted_melee_level - self.base_melee_level * 4))
        else:
            pass
        return [dpl_f, dpl_v]
        
    # Helper function to check hexhunter effect
    def hexhunter(self):
        hexhunter = 0
        
        if self.th_input == 'Inquisitor staff':
            hexhunter = 1
        elif self.th_input == 'Hexhunter bow':
            hexhunter = 2
        elif self.th_input == 'Terrasaur maul':
            hexhunter = 3
        return hexhunter
    
    # Computes the dmg boosts from prayer
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
    
    # Computes the dmg boost from aura passives
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
    
    # Computes the dmg boost from ultimates and specs
    def sunshine(self):
        pass
    
test = StandardAbility()




