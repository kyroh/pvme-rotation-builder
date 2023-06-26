#
# Author - kyroh
# 
# June 2023
#

from components.inputs import UserInputs
from components.ability_dmg import AbilityDmg
from components.dmg_boost import CheckDmgBoosts

class StandardAbility:
    def __init__(self, ability, cast_tick, weapon):
        self.boost = CheckDmgBoosts(ability, cast_tick, weapon)
        self.sim = 10000
        self.ad = AbilityDmg(ability, cast_tick, weapon)
        self.inputs = UserInputs(ability, cast_tick, weapon)
        self.cast_tick = cast_tick
        for abil in self.inputs.timing:
            if abil['name'] == self.inputs.ability_input:
                ability = abil
                break
        self.hit_tick = ability[f'{self.inputs.type} tick'] + self.cast_tick
        
        self.prayer_boost = self.prayer_dmg()
        self.magic_prayer, self.range_prayer, self.melee_prayer = self.prayer_boost
    
    def prayer_dmg(self):
        boost = next((b for b in self.inputs.boosts if b['name'] == self.inputs.prayer_input), None)
        if boost is None:
            return [0, 0, 0]
        
        prayer_dmg = [boost["magic_dmg_percent"], boost["range_dmg_percent"], boost["strength_dmg_percent"]]
        return prayer_dmg
    
    # Computes dmg floor with prayer modifier
    def fixed(self):
        prayer_map = {
            'MAGIC': self.magic_prayer,
            'RANGE': self.range_prayer,
            'MELEE': self.melee_prayer
        }
        if self.inputs.type_n != 'BLEED':
            if self.inputs.style in prayer_map:
                fixed = int(int(self.ad.ability_dmg * self.inputs.fixed_dmg) * (1 + prayer_map[self.inputs.style]))
            else:
                pass
        else:
            fixed = int(self.ad.ability_dmg * self.inputs.fixed_dmg)
        return fixed
    
    # Computes var dmg with prayer modifier
    def var(self):
        prayer_map = {
            'MAGIC': self.magic_prayer,
            'RANGE': self.range_prayer,
            'MELEE': self.melee_prayer
        }
        
        if self.inputs.type_n != 'BLEED':
            if self.inputs.style in prayer_map:
                var = int(int(self.ad.ability_dmg * self.inputs.var_dmg) * (1 + prayer_map[self.inputs.style]))
            else:
                pass
        else:
            var = int(self.ad.ability_dmg * self.inputs.var_dmg)
        return var
    
     # Computes dmg per level and outputs new fixed and var dmg
    def dpl(self):
        fixed = self.fixed()
        var = self.var()
    
        if self.inputs.style in ('MAGIC', 'RANGE', 'MELEE'):
            if self.inputs.style == 'MAGIC':
                base_level = self.inputs.base_magic_level
                boosted_level = self.ad.boosted_magic_level
            elif self.inputs.style == 'RANGE':
                base_level = self.inputs.base_range_level
                boosted_level = self.ad.boosted_range_level
            elif self.inputs.style == 'MELEE':
                base_level = self.inputs.base_strength_level
                boosted_level = self.ad.boosted_strength_level
            else:
                pass
        
            level_difference = boosted_level - base_level
            fixed += int(level_difference * 4)
            var += int(level_difference * 4)
        
        return [fixed, var]
    
    # Computes the dmg range of an abil after precise
    def precise(self):
        dmg_values = self.dmg_boost()
        fixed = dmg_values[0]
        var = dmg_values[1]
        if self.inputs.type_n != 'BLEED':
            precise = int(0.015 * (fixed + var) * self.inputs.precise_rank)
            fixed += precise
            var -= precise
        else:
            pass
        return [fixed, var]
        
    # Computes the dmg range of an abil after equilibrium
    def equilibrium(self):
        precise = self.precise()
        fixed = precise[0]
        var = precise[1]
        if self.inputs.type_n != 'BLEED':
            if self.inputs.aura_input == 'Equilibrium':
                fixed += 0.25 * var
                var -= 0.5 * var
            else:
                fixed += 0.03 * var * self.inputs.equilibrium_rank
                var -= 0.04 * var * self.inputs.equilibrium_rank
        else:
            pass
        return [int(fixed), int(var)]

    # Computes the dmg boost from ultimates and specs
    def dmg_boost(self):
        dmg = self.dpl()
        fixed = dmg[0]
        var = dmg[1]
        if (self.boost.meta == True and self.inputs.style == 'MAGIC'):
            fixed = int(1.625 * fixed)
            var = int(1.625 * var)
        elif self.inputs.type_n != 'BLEED':
            if (self.boost.sunshine == True and self.inputs.style == 'MAGIC') or (self.boost.death_swift == True and self.inputs.style == 'RANGE'):
                fixed = int(1.5 * fixed)
                var = int(1.5 * var)
            elif self.boost.zerk == True and self.inputs.style == 'MELEE':
                fixed = int(2 * fixed)
                var = int(2 * var)
            elif self.boost.zgs == True and self.inputs.style == 'MELEE':
                fixed = int(1.25 * fixed)
                var = int(1.25 * var)
            else:
                pass
        else:
            pass
        return [fixed, var]
    
    # Computes the dmg boost from aura passives
    def aura_passive(self):
        dmg = self.equilibrium()
        fixed = dmg[0]
        var = dmg[1]
        
        boost = None
        for b in self.inputs.boosts:
            if b['name'] == self.inputs.aura_input:
                boost = b
                break
        if self.inputs.style == 'MAGIC' and self.boost.sunshine == False:
            fixed += int(fixed * boost['magic_dmg_percent'])
            var += int(var * boost['magic_dmg_percent'])
        elif self.inputs.style == 'RANGE' and self.boost.death_swift == False:
            fixed += int(fixed * boost['range_dmg_percent'])
            var += int(var * boost['range_dmg_percent'])
        elif self.inputs.style == 'MELEE' and (self.boost.zerk == False or self.boost.zgs == False):
            fixed += int(fixed * boost['strength_dmg_percent'])
            var += int(var * boost['strength_dmg_percent'])
        else:
            pass
        return [fixed, var]
    
    def hits(self):
        dmg = self.aura_passive()
        fixed = dmg[0]
        var = dmg[1]
        hits = {}
        if self.inputs.type_n == 'SINGLE_HIT_ABIL':
            if self.inputs.dmg_output == 'MIN':
                hits = fixed
            elif self.inputs.dmg_output == 'AVG':
                hits = fixed + int(var * 0.5)
            elif self.inputs.dmg_output == 'MAX':
                hits = fixed + var
        elif self.inputs.type_n == 'BLEED':
            pass
        elif self.inputs.type_n == 'CHANNELED':
            pass
        return {"tick": self.hit_tick, "dmg": hits}