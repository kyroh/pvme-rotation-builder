#
# Author - kyroh
# 
# This source code is licensed under the Attribution-NonCommercial-ShareAlike 4.0 International license found in the LICENSE file in the root directory of this source tree.
# 
# May 2023
#

import random
import os
import json

class StandardAbility:
    def __init__(self):
        with open(os.path.join('utils', 'WEAPONS.json'), 'r') as w:
            self.weapons = json.load(w)
        
        with open(os.path.join('utils', 'BOOSTS.json'), 'r') as b:
            self.boosts = json.load(b)

        with open(os.path.join('utils', 'ABILITIES.json'), 'r') as a:
            self.abilities = json.load(a)

        # Variables from GUI inputs
        self.ability_input = 'blood tendrils'
        self.mh_input = 'None'
        self.oh_input = 'None'
        self.th_input = 'Zaros godsword'
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
        self.sunshine = 'INACTIVE'
        self.death_swiftness = 'INACTIVE'
        self.berserk = 'INACTIVE'
        self.zgs_spec = 'INACTIVE'
        self.sim = 10000
        self.dmg_output = 'MAX'
        
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
        self.name = self.abil_params[5]
        
        self.ability_dmg = self.base_ability_dmg()
        
        self.prayer_boost = self.prayer_dmg()
        self.magic_prayer = self.prayer_boost[0]
        self.range_prayer = self.prayer_boost[1]
        self.melee_prayer = self.prayer_boost[2]

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
            total_levels.append(int(x + y + z))
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
        if mh['style'] == 'MAGIC':
            mh_ability_dmg = int(2.5 * self.boosted_magic_level) + int(9.6 * min(mh['dmg_tier'],self.spell_input) + self.bonus)
        elif mh['style'] == 'RANGE':
            mh_ability_dmg = int(2.5 * self.boosted_range_level) + int(9.6 * min(mh['dmg_tier'],self.spell_input) + self.bonus)
        elif mh['style'] == 'MELEE':
            mh_ability_dmg = int(2.5 * self.boosted_strength_level) + int(9.6 * mh['dmg_tier'] + self.bonus)
        else:
            pass
        
        for w in self.weapons:
            if w['name'] == self.oh_input:
                oh = w
                break
        if oh is None:
            pass
        elif oh['style'] == 'MAGIC':
            oh_ability_dmg = int(0.5 * (int(2.5 * self.boosted_magic_level) + int(9.6 * min(oh['dmg_tier'],self.spell_input) + self.bonus)))
        elif oh['style'] == 'RANGE':
            oh_ability_dmg = int(0.5 * (int(2.5 * self.boosted_range_level) + int(9.6 * min(oh['dmg_tier'],self.spell_input) + self.bonus)))
        elif oh['style'] == 'MELEE':
            oh_ability_dmg = int(0.5 * (int(2.5 * self.boosted_strength_level) + int(9.6 * oh['dmg_tier'] + self.bonus)))
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
        if th['style'] == 'MAGIC':
            base_ability_dmg = int(2.5 * self.boosted_magic_level) + int(1.25 * self.boosted_magic_level) + int(14.4 * min(th['dmg_tier'],self.spell_input) + 1.5 * self.bonus)
        elif th['style'] == 'RANGE':
            base_ability_dmg = int(2.5 * self.boosted_range_level) + int(1.25 * self.boosted_range_level) + int(14.4 * min(th['dmg_tier'],self.spell_input) + 1.5 * self.bonus)
        elif th['style'] == 'MELEE':
            base_ability_dmg = int(2.5 * self.boosted_strength_level) + int(1.25 * self.boosted_strength_level) + int(14.4 * th['dmg_tier'] + 1.5 * self.bonus)
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
        if mh['style'] == 'MAGIC':
            mh_ability_dmg = int(2.5 * self.boosted_magic_level) + int(9.6 * min(mh['dmg_tier'],self.spell_input) + self.bonus)
        elif mh['style'] == 'RANGE':
            mh_ability_dmg = int(2.5 * self.boosted_range_level) + int(9.6 * min(mh['dmg_tier'],self.spell_input) + self.bonus)
        elif mh['style'] == 'MELEE':
            mh_ability_dmg = int(2.5 * self.boosted_strength_level) + int(9.6 * mh['dmg_tier'] + self.bonus)
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
    
    # Helper function to identify the combat style and type of ability casted
    def get_abil_params(self):
        
        for a in self.abilities:
            if a['name'] == self.ability_input:
                abil = a
                break
        style = abil['style']
        class_n = abil['class_n']
        type_n = abil['type_n']
        min_dmg = abil['min']
        max_dmg = abil['max']
        name = abil['name']
        return [style, class_n, type_n, min_dmg, max_dmg, name]
    
    # Computes dmg floor with prayer modifier
    def fixed(self):
        fixed = 0
        
        if self.style == 'MAGIC':
            fixed = int(int(self.ability_dmg * self.min_dmg) * (1 + self.magic_prayer))
        elif self.style == 'RANGE':
            fixed = int(int(self.ability_dmg * self.min_dmg) * (1 + self.range_prayer))
        elif self.style == 'MELEE':
            fixed = int(int(self.ability_dmg * self.min_dmg) * (1 + self.melee_prayer))
        else:
            pass
        return fixed
    
    # Computes var dmg with prayer modifier
    def var(self):
        if self.style == 'MAGIC':
            var = int(int(self.ability_dmg * (self.max_dmg - self.min_dmg)) * (1 + self.magic_prayer))
        elif self.style == 'RANGE':
            var = int(int(self.ability_dmg * (self.max_dmg - self.min_dmg)) * (1 + self.range_prayer))
        elif self.style == 'MELEE':
            var = int(int(self.ability_dmg * (self.max_dmg - self.min_dmg)) * (1 + self.melee_prayer))
        else:
            pass
        return var
    
    # Computes the dmg range of an abil after precise
    def precise(self):
        dmg_values = self.dpl()
        fixed = dmg_values[0]
        var = dmg_values[1]
        precise = 0.015 * (fixed + var) * self.precise_rank
        fixed += precise
        var -= precise
        return [int(fixed), int(var)]
        
    # Computes the dmg range of an abil after equilibrium
    def equilibrium(self):
        precise = self.precise()
        fixed = precise[0]
        var = precise[1]
        
        if self.aura_input == 'Equilibrium':
            fixed += 0.25 * var
            var -= 0.5 * var
        else:
            fixed += 0.03 * var * self.equilibrium_rank
            var -= 0.04 * var * self.equilibrium_rank
        return [int(fixed), int(var)]
    
    # Computes dmg per level and outputs new fixed and var dmg
    def dpl(self):
        fixed = self.fixed()
        var = self.var()
        
        if self.style == 'MAGIC':
            fixed += int((self.boosted_magic_level - self.base_magic_level) * 4)
            var += int((self.boosted_magic_level - self.base_magic_level) * 4)
        elif self.style == 'RANGE':
            fixed += int((self.boosted_range_level - self.base_range_level) * 4)
            var += int((self.boosted_range_level - self.base_range_level) * 4)
        elif self.style == 'MELEE':
            fixed += int((self.boosted_melee_level - self.base_melee_level) * 4)
            var += int((self.boosted_melee_level - self.base_melee_level) * 4)
        else:
            pass
        return [fixed, var]
    
    # Computes the dmg boost from aura passives
    def aura_passive(self):
        # check if mani passive buff still applies if you're standing in a DS but using magic
        dmg = self.dmg_boost()
        fixed = dmg[0]
        var = dmg[1]
        
        if self.sunshine == 'ACTIVE' and self.style == 'MAGIC' or self.death_swiftness == 'ACTIVE' and self.style == 'RANGE' or self.berserk == 'ACTIVE' and self.style == 'MELEE' or self.zgs_spec == 'ACTIVE' and self.style == 'MELEE':
            pass
        else:
            for b in self.boosts:
                if b['name'] == self.aura_input:
                    boost = b
                    break
            if boost is None:
                pass
            if self.style == 'MAGIC':
                fixed += int(fixed * boost['magic_dmg_percent'])
                var += int(var * boost['magic_dmg_percent'])
            elif self.style == 'RANGE':
                fixed += int(fixed * boost['magic_dmg_percent'])
                var += int(var * boost['magic_dmg_percent'])
            elif self.style == 'MELEE':
                fixed += int(fixed * boost['magic_dmg_percent'])
                var += int(var * boost['magic_dmg_percent'])
            else:
                pass
        return [fixed, var]
    
    # Computes the dmg boost from ultimates and specs
    def dmg_boost(self):
        dmg_values = self.equilibrium()
        fixed = dmg_values[0]
        var = dmg_values[1]
        
        if self.ability_input != 'BLEED':
            if self.sunshine == 'ACTIVE' and self.style == 'MAGIC' or self.death_swiftness == 'ACTIVE' and self.style == 'RANGE':
                fixed += int(fixed * 0.5)
                var += int(var * 0.5)
            elif self.berserk == 'ACTIVE' and self.style == 'MELEE':
                fixed += int(fixed * 2.0)
                var += int(var * 2.0)
            elif self.zgs_spec == 'ACTIVE' and self.style == 'MELEE':
                fixed += int(fixed * 1.25)
                var += int(var * 1.25)
            else:
                pass
            
        else:
            pass
        return [fixed, var]

class BleedAbility:
    
    def __init__(self):
        with open(os.path.join('utils', 'BLEEDS.json'), 'r') as bleed:
            self.bleeds = json.load(bleed)
            
        standard = StandardAbility()

        self.dmg_output = standard.dmg_output
        self.sim = standard.sim
        
        self.lunging_rank = 0
            
        self.base_magic_level = standard.base_magic_level
        self.base_range_level = standard.base_range_level
        self.base_strength_level = standard.base_strength_level

        self.ability_dmg = standard.base_ability_dmg()

        self.name = standard.name
        self.style = standard.style
        self.class_n = standard.class_n
        self.type_n = standard.type_n
        self.min_dmg = standard.min_dmg
        self.max_dmg = standard.max_dmg
        
        self.boosted_magic_level = standard.boosted_magic_level
        self.boosted_range_level = standard.boosted_range_level
        self.boosted_strength_level = standard.boosted_strength_level

    # Conmputes fixed dmg without prayer because bleeds are great
    def fixed(self):
        if self.style == 'MAGIC':
            fixed = int(int(self.ability_dmg * self.min_dmg))
        elif self.style == 'RANGE':
            fixed = int(int(self.ability_dmg * self.min_dmg))
        elif self.style == 'MELEE':
            fixed = int(int(self.ability_dmg * self.min_dmg))
        else:
            pass
        return fixed
    
    # Computes var dmg without prayer because bleeds make sense
    def var(self):
        if self.style == 'MAGIC':
            var = int(int(self.ability_dmg * (self.max_dmg - self.min_dmg)))
        elif self.style == 'RANGE':
            var = int(int(self.ability_dmg * (self.max_dmg - self.min_dmg)))
        elif self.style == 'MELEE':
            var = int(int(self.ability_dmg * (self.max_dmg - self.min_dmg)))
        else:
            pass
        return var
    
    # Simulates the abil n times and returns the average
    def avg_dmg(self):
        fixed = self.fixed()
        var = self.var()
        max_dmg = fixed + var
        min_dmg = fixed
        avg_dmg = 0
        total = 0
        
        if self.name == 'combust' or self.name == 'fragmentation shot' or self.name == 'dismember' or self.name == 'slaughter':
            pass
        else:
            for _ in range(self.sim):
                random_num = random.randint(min_dmg, max_dmg)
                total += random_num
            avg_dmg = int(total / self.sim)
        return avg_dmg
    
    def hits(self):
        avg_dmg = self.avg_dmg()
        var = self.var()
        min_dmg = self.fixed()
        max_dmg = min_dmg + var
        hits = []
        
        for bleed in self.bleeds:
            if bleed['name'] == self.name:
                abil = bleed
                break
        hit_count = abil['hits']
        dmg_decay = abil['dmg_decay']
        
        if dmg_decay == 0:
            if self.dmg_output == 'MIN':
                hits = [min_dmg] * hit_count
            elif self.dmg_output == 'AVG':
                hits = [avg_dmg] * hit_count
            elif self.dmg_output == 'MAX':
                hits = [max_dmg] * hit_count
            else:
                pass
        else:
            if self.name == 'corruption shot' or self.name == 'corruption blast':
                if self.dmg_output == 'MIN':
                    reduce = int(dmg_decay * min_dmg)
                    hits = [min_dmg - i * reduce for i in range(hit_count)]
                elif self.dmg_output == 'AVG':
                    reduce = int(dmg_decay * avg_dmg)
                    hits = [avg_dmg - i * reduce for i in range(hit_count)]
                elif self.dmg_output == 'MAX':
                    reduce = int(dmg_decay * max_dmg)
                    hits = [max_dmg - i * reduce for i in range(hit_count)]
                else:
                    pass
            elif self.name == 'blood tendrils':
                if self.dmg_output == 'MIN':
                    reduce = int(dmg_decay * min_dmg)
                    hits = [min_dmg] + [min_dmg - reduce] * (hit_count - 1)
                elif self.dmg_output == 'AVG':
                    reduce = int(dmg_decay * avg_dmg)
                    hits = [avg_dmg] + [avg_dmg - reduce] * (hit_count - 1)
                elif self.dmg_output == 'MAX':
                    reduce = int(dmg_decay * max_dmg)
                    hits = [max_dmg] + [max_dmg - reduce] * (hit_count - 1)
            else:
                pass
        return hits
    
    def walk(self):
         pass

class ChanneledABility:
    pass 

class OnHitEffects:
    pass


test = BleedAbility() 

avg = test.hits()

print(avg)





