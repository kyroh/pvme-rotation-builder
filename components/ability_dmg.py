from components.inputs import UserInputs

class AbilityDmg:
    def __init__(self, ability, cast_tick, weapon):
        self.input = UserInputs(ability, weapon)
        
        self.boosted_levels = self.calculate_levels()
        self.boosted_magic_level, self.boosted_range_level, self.boosted_strength_level = self.boosted_levels
        
        self.ability_dmg = self.base_ability_dmg()
    
    #computes the level boost from users active aura
    def aura_level_boost(self):
        boost = next((b for b in self.input.boosts if b['name'] == self.input.aura_input), None)
        if boost is None:
            return [0, 0, 0]

        magic_boost_percent = self.input.base_magic_level * boost.get('magic_level_percent', 0)
        range_boost_percent = self.input.base_range_level * boost.get('range_level_percent', 0)
        strength_boost_percent = self.input.base_strength_level * boost.get('strength_level_percent', 0)

        return [magic_boost_percent, range_boost_percent, strength_boost_percent]

    #computes level boost from users potion
    def potion_level_boost(self):
        boost = next((b for b in self.input.boosts if b['name'] == self.input.potion_input), None)
        if boost is None:
            return [0, 0, 0]

        boost_values = {
            'magic_level_percent': self.input.base_magic_level * boost.get('magic_level_percent', 0),
            'range_level_percent': self.input.base_range_level * boost.get('range_level_percent', 0),
            'strength_level_percent': self.input.base_strength_level * boost.get('strength_level_percent', 0),
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
        base_levels = [self.input.base_magic_level, self.input.base_range_level, self.input.base_strength_level]

        total_levels = [int(x + y + z) for x, y, z in zip(aura_boosts, potion_boosts, base_levels)]
        return total_levels
    
    #dual wield ability dmg calc
    def dw_ability_dmg(self):
        mh = next((w for w in self.input.weapons if w['name'] == self.input.mh_input), None)
        if mh is None:
            return 0

        style = mh['style']
        dmg_tier = min(mh['dmg_tier'], self.input.spell_input)
        bonus = 0
        if style == 'MAGIC':
            base_ability_dmg = int(2.5 * self.boosted_magic_level) + int(9.6 * dmg_tier + self.input.magic_bonus)
        elif style == 'RANGE':
            base_ability_dmg = int(2.5 * self.boosted_range_level) + int(9.6 * dmg_tier + self.input.range_bonus)
        elif style == 'MELEE':
            base_ability_dmg = int(2.5 * self.boosted_strength_level) + int(9.6 * dmg_tier + self.input.melee_bonus)
        else:
            base_ability_dmg = 0
        
        return base_ability_dmg

    #two handed ability dmg calc
    def th_ability_dmg(self):
        th = next((w for w in self.input.weapons if w['name'] == self.input.th_input), None)
        if th is None:
            return 0

        style = th['style']
        dmg_tier = min(th['dmg_tier'], self.input.spell_input)
        bonus = 0
        if style == 'MAGIC':
            base_ability_dmg = int(3.75 * self.boosted_magic_level) + int(14.4 * dmg_tier + 1.5 * self.input.magic_bonus)
        elif style == 'RANGE':
            base_ability_dmg = int(3.75 * self.boosted_range_level) + int(14.4 * dmg_tier + 1.5 * self.input.range_bonus)
        elif style == 'MELEE':
            base_ability_dmg = int(3.75 * self.boosted_strength_level) + int(14.4 * dmg_tier + 1.5 * self.input.melee_bonus)
        else:
            base_ability_dmg = 0

        return base_ability_dmg
    
    #mainhand shielf ability dmg calc
    def ms_ability_dmg(self):
        mh = next((w for w in self.input.weapons if w['name'] == self.input.mh_input), None)
        if mh is None:
            return 0

        style = mh['style']
        dmg_tier = min(mh['dmg_tier'], self.input.spell_input)
        bonus = 0
        if style == 'MAGIC':
            base_ability_dmg = int(2.5 * self.boosted_magic_level) + int(9.6 * dmg_tier + self.input.magic_bonus)
        elif style == 'RANGE':
            base_ability_dmg = int(2.5 * self.boosted_range_level) + int(9.6 * dmg_tier + self.input.range_bonus)
        elif style == 'MELEE':
            base_ability_dmg = int(2.5 * self.boosted_strength_level) + int(9.6 * dmg_tier + self.input.melee_bonus)
        else:
            base_ability_dmg = 0

        return base_ability_dmg

    #helper function to use the correct ability dmg based on the casting weapon type from inputs.py
    def base_ability_dmg(self):
        if self.input.type == '2h':
            return self.th_ability_dmg()
        elif self.input.type == 'dw':
            return self.dw_ability_dmg()
        elif self.input.type == 'ms':
            return self.ms_ability_dmg()
        else:
            return 0
