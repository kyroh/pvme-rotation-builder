from components.inputs import UserInputs

class AbilityDmg:
    def __init__(self, ability, cast_tick, weapon):
        self.inputs = UserInputs(ability, weapon)
        
        self.boosted_levels = self.calculate_levels()
        self.boosted_magic_level, self.boosted_range_level, self.boosted_strength_level = self.boosted_levels
        
        self.ability_dmg = self.base_ability_dmg()
    
    #computes the level boost from users active aura
    def aura_level_boost(self):
        boost = next((b for b in self.inputs.boosts if b['name'] == self.inputs.aura_input), None)
        if boost is None:
            return [0, 0, 0]

        magic_boost_percent = self.inputs.base_magic_level * boost.get('magic_level_percent', 0)
        range_boost_percent = self.inputs.base_range_level * boost.get('range_level_percent', 0)
        strength_boost_percent = self.inputs.base_strength_level * boost.get('strength_level_percent', 0)

        return [magic_boost_percent, range_boost_percent, strength_boost_percent]

    #computes level boost from users potion
    def potion_level_boost(self):
        boost = next((b for b in self.inputs.boosts if b['name'] == self.inputs.potion_input), None)
        if boost is None:
            return [0, 0, 0]

        boost_values = {
            'magic_level_percent': self.inputs.base_magic_level * boost.get('magic_level_percent', 0),
            'range_level_percent': self.inputs.base_range_level * boost.get('range_level_percent', 0),
            'strength_level_percent': self.inputs.base_strength_level * boost.get('strength_level_percent', 0),
            'magic_level_boost': boost.get('magic_level_boost', 0),
            'range_level_boost': boost.get('range_level_boost', 0),
            'strength_level_boost': boost.get('strength_level_boost', 0)
        }

        net_magic_boost = boost_values['magic_level_percent'] + boost_values['magic_level_boost']
        net_range_boost = boost_values['range_level_percent'] + boost_values['range_level_boost']
        net_strength_boost = boost_values['strength_level_percent'] + boost_values['strength_level_boost']

        return [net_magic_boost, net_range_boost, net_strength_boost]

    #computes total level boost for purpose of computes ability dmg
    def calculate_levels(self):
        aura_boosts = self.aura_level_boost()
        potion_boosts = self.potion_level_boost()
        base_levels = [self.inputs.base_magic_level, self.inputs.base_range_level, self.inputs.base_strength_level]

        total_levels = [int(x + y + z) for x, y, z in zip(aura_boosts, potion_boosts, base_levels)]
        return total_levels
    
    #dual wield ability dmg calc
    def dw_ability_dmg(self):
        base_ability_dmg = 0

        for w in self.inputs.weapons:
            if w['name'] == self.inputs.oh_input:
                oh = w
                break
        if oh is None:
            pass
        elif self.inputs.style == 'MAGIC':
            base_ability_dmg += int(0.5 * (int(2.5 * self.boosted_magic_level) + int(9.6 * min(oh['dmg_tier'],self.inputs.spell_input) + int(self.inputs.magic_bonus))))
        elif self.inputs.style == 'RANGE':
            base_ability_dmg += int(0.5 * (int(2.5 * self.boosted_range_level) + int(9.6 * min(oh['dmg_tier'],self.inputs.spell_input) + int(self.inputs.range_bonus))))
        elif self.inputs.style == 'MELEE':
            base_ability_dmg += int(0.5 * (int(2.5 * self.boosted_strength_level) + int(9.6 * oh['dmg_tier'] + int(self.inputs.melee_bonus))))
        else:
            pass
        
        for w in self.inputs.weapons:
            if w['name'] == self.inputs.mh_input:
                mh = w
                break
        if mh is None:
            pass

        if self.inputs.style == 'MAGIC':
            base_ability_dmg += int(2.5 * self.boosted_magic_level) + int(9.6 * min(mh['dmg_tier'], self.inputs.spell_input) + int(self.inputs.magic_bonus))
        elif self.inputs.style == 'RANGE':
            base_ability_dmg += int(2.5 * self.boosted_range_level) + int(9.6 * min(mh['dmg_tier'], self.inputs.spell_input) + int(self.inputs.range_bonus))
        elif self.inputs.style == 'MELEE':
            base_ability_dmg += int(2.5 * self.boosted_strength_level) + int(9.6 * min(mh['dmg_tier'], self.inputs.spell_input) + int(self.inputs.melee_bonus))
        else:
            pass

        return base_ability_dmg

    #two handed ability dmg calc
    def th_ability_dmg(self):
        base_ability_dmg = 0 

        for w in self.inputs.weapons:
            if w['name'] == self.inputs.th_input:
                th = w
                break    
            if th is None:
                pass
        if self.inputs.style == 'MAGIC':
            base_ability_dmg += int(2.5 * self.boosted_magic_level) + int(1.25 * self.boosted_magic_level) + int(14.4 * min(th['dmg_tier'],self.inputs.spell_input) + 1.5 * int(self.inputs.magic_bonus))
        elif self.inputs.style == 'RANGE':
            base_ability_dmg += int(2.5 * self.boosted_range_level) + int(1.25 * self.boosted_range_level) + int(14.4 * min(th['dmg_tier'],self.inputs.spell_input) + 1.5 * int(self.inputs.range_bonus))
        elif self.inputs.style == 'MELEE':
            base_ability_dmg += int(2.5 * self.boosted_strength_level) + int(1.25 * self.boosted_strength_level) + int(14.4 * th['dmg_tier'] + 1.5 * int(self.inputs.melee_bonus))
        else:
            pass
        return base_ability_dmg
    
    #mainhand shielf ability dmg calc
    def ms_ability_dmg(self):
        base_ability_dmg = 0

        for w in self.inputs.weapons:
            if w['name'] == self.inputs.mh_input:
                mh = w
                break
        if mh is None:
            pass

        if self.inputs.style == 'MAGIC':
            base_ability_dmg += int(2.5 * self.boosted_magic_level) + int(9.6 * min(mh['dmg_tier'], self.inputs.spell_input) + int(self.inputs.magic_bonus))
        elif self.inputs.style == 'RANGE':
            base_ability_dmg += int(2.5 * self.boosted_range_level) + int(9.6 * min(mh['dmg_tier'], self.inputs.spell_input) + int(self.inputs.range_bonus))
        elif self.inputs.style == 'MELEE':
            base_ability_dmg += int(2.5 * self.boosted_strength_level) + int(9.6 * min(mh['dmg_tier'], self.inputs.spell_input) + int(self.inputs.melee_bonus))
        else:
            pass
        
        return base_ability_dmg

    #helper function to use the correct ability dmg based on the casting weapon type from inputs.py
    def base_ability_dmg(self):
        if self.inputs.type == '2h':
            return self.th_ability_dmg()
        elif self.inputs.type == 'dw':
            return self.dw_ability_dmg()
        elif self.inputs.type == 'ms':
            return self.ms_ability_dmg()
        else:
            return 0
