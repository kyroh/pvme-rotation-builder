from inputs import UserInputs
from ability_dmg import AbilityDmg

class StandardAbility:
    def __init__(self, ability):
        self.sunshine = False
        self.death_swiftness = False
        self.berserk = False
        self.zgs_spec = False
        self.sim = 10000
        self.ad = AbilityDmg(ability)
        self.inputs = UserInputs(ability)
    
    # Computes dmg floor with prayer modifier
    def fixed(self):
        prayer_map = {
            'MAGIC': self.ad.magic_prayer,
            'RANGE': self.ad.range_prayer,
            'MELEE': self.ad.melee_prayer
        }
        
        if self.inputs.style in prayer_map:
            fixed = int(int(self.ad.ability_dmg * self.inputs.fixed_dmg) * (1 + prayer_map[self.inputs.style]))
        else:
            fixed = 0
        return fixed
    
    # Computes var dmg with prayer modifier
    def var(self):
        prayer_map = {
            'MAGIC': self.ad.magic_prayer,
            'RANGE': self.ad.range_prayer,
            'MELEE': self.ad.melee_prayer
        }
        
        if self.inputs.style in prayer_map:
            var = int(int(self.ad.ability_dmg * self.inputs.var_dmg) * (1 + prayer_map[self.inputs.style]))
        else:
            var = 0
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
        dmg_values = self.dpl()
        fixed = dmg_values[0]
        var = dmg_values[1]
        precise = int(0.015 * (fixed + var) * self.inputs.precise_rank)
        fixed += precise
        var -= precise
        return [(fixed), (var)]
        
    # Computes the dmg range of an abil after equilibrium
    def equilibrium(self):
        precise = self.precise()
        fixed = precise[0]
        var = precise[1]
        
        if self.inputs.aura_input == 'Equilibrium':
            fixed += 0.25 * var
            var -= 0.5 * var
        else:
            fixed += 0.03 * var * self.inputs.equilibrium_rank
            var -= 0.04 * var * self.inputs.equilibrium_rank
        return [int(fixed), int(var)]

    # Computes the dmg boost from ultimates and specs
    def dmg_boost(self):
        precise = self.precise()
        prec_fixed = precise[0]
        prec_var = precise[1]
        equilibrium = self.equilibrium()
        eq_var = equilibrium[1]
    
        if (self.sunshine == True and self.inputs.style == 'MAGIC') or (self.death_swiftness == True and self.inputs.style == 'RANGE'):
            fixed = int(1.5 * (prec_fixed + (0.03 * self.inputs.equilibrium_rank * prec_var)))
            var = int(1.5 * (prec_var - 0.04 * self.inputs.equilibrium_rank * prec_var))
        elif self.berserk == True and self.inputs.style == 'MELEE':
            fixed = int(2 * (prec_fixed + (0.03 * self.inputs.equilibrium_rank * prec_var)))
            var = int(2 * (prec_var - 0.04 * self.inputs.equilibrium_rank * prec_var))
        elif self.zgs_spec == True and self.inputs.style == 'MELEE':
            fixed = int(1.25 * (prec_fixed + (0.03 * self.inputs.equilibrium_rank * prec_var)))
            var = int(1.25 * (prec_var - 0.04 * self.inputs.equilibrium_rank * prec_var))
        else:
            fixed = equilibrium[0]
            var = equilibrium[1]
        return [fixed, var]
    
    # Computes the dmg boost from aura passives
    def aura_passive(self):
        dmg = self.dmg_boost()
        fixed = dmg[0]
        var = dmg[1]
        
        boost = None
        for b in self.inputs.boosts:
            if b['name'] == self.inputs.aura_input:
                boost = b
                break
        if self.inputs.style == 'MAGIC' and self.sunshine == False:
            fixed += int(fixed * boost['magic_dmg_percent'])
            var += int(var * boost['magic_dmg_percent'])
        elif self.inputs.style == 'RANGE' and self.death_swiftness == False:
            fixed += int(fixed * boost['range_dmg_percent'])
            var += int(var * boost['range_dmg_percent'])
        elif self.inputs.style == 'MELEE' and (self.berserk == False or self.zgs_spec == False):
            fixed += int(fixed * boost['strength_dmg_percent'])
            var += int(var * boost['strength_dmg_percent'])
        else:
            pass
        return [fixed, var]
    
    def hits(self):
        dmg = self.aura_passive()
        fixed = dmg[0]
        var = dmg[1]
        hits = []

        if self.inputs.dmg_output == 'MIN':
            hits = [fixed]
        elif self.inputs.dmg_output == 'AVG':
            hits = [fixed + int(var / 2)]
        elif self.inputs.dmg_output == 'MAX':
            hits = [fixed + var]
        return hits
