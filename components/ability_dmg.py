from resources import Utils

class AbilityDmg:
    def __init__(self): 
        self.utils = Utils()
        self.baseMagic = 0
        self.baseRange = 0
        self.baseStr = 0
        self.baseNecro = 0
        self.reaperCrew = False
        self.potion = None
        self.aura = None
        
        self.armour = {
            'helm': None,
            'body': None,
            'legs': None,
            'boots': None,
            'gloves': None,
            'neck': None,
            'cape': None,
            'ring': None,
            'pocket': None        
        }
        
        self.type = '2h'
        
        # a list of weapons that may be used order is mh, oh, 2h, shield
        self.mh = None
        self.oh = None
        self.th = None
        self.sh = None
        self.prayer = None
        self.autocast = 99
        self.ammo = 99
        
        self.levels = 0
        self.magicLvl = 0
        self.rangeLvl = 0
        self.strLvl = 0
        self.necroLvl = 0
        
        self.magicBonus = 0
        self.rangeBonus = 0
        self.strBonus = 0
        self.necroBonus = 0
    
    def getLevels(self, levels):
        index = levels
        self.baseMagic = index[0]
        self.baseRange = index[1]
        self.baseStr= index[2]
        self.baseNecro = index[3]
        
    def getConstants(self, constants):
        index = constants
        self.aura = index[0]
        self.potion= index[1]
        self.reaperCrew = index[2]
    
    def getPreset(self, armour, weapons, type):
        self.armour = armour
        index = weapons
        self.mh = index[0]
        self.oh = index[1]
        self.th = index[2]
        self.sh = index[3]
        self.prayer = index[4]
        self.type = type
    
    #computes the level boost from users active aura
    def aura_level_boost(self):
        boost = next((b for b in self.utils.boosts if b['name'] == self.aura), None)
        if boost is None:
            return [0, 0, 0, 0]

        magic_boost_percent = self.baseMagic * boost.get('magic_level_percent', 0)
        range_boost_percent = self.baseRange * boost.get('range_level_percent', 0)
        strength_boost_percent = self.baseStr * boost.get('strength_level_percent', 0)
        necro_boost_percent = self.baseNecro * boost.get('necro_level_percent', 0)

        return [magic_boost_percent, range_boost_percent, strength_boost_percent, necro_boost_percent]

    #computes level boost from users potion
    def potion_level_boost(self):
        boost = next((b for b in self.utils.boosts if b['name'] == self.potion), None)
        if boost is None:
            return [0, 0, 0, 0]

        boost_values = {
            'magic_level_percent': self.baseMagic * boost.get('magic_level_percent', 0),
            'range_level_percent': self.baseRange * boost.get('range_level_percent', 0),
            'strength_level_percent': self.baseStr * boost.get('strength_level_percent', 0),
            'necro_level_percent': self.baseNecro * boost.get('necro_level_percent', 0),
            'magic_level_boost': boost.get('magic_level_boost', 0),
            'range_level_boost': boost.get('range_level_boost', 0),
            'strength_level_boost': boost.get('strength_level_boost', 0),
            'necro_level_boost': boost.get('necro_level_boost', 0)
        }

        net_magic_boost = boost_values['magic_level_percent'] + boost_values['magic_level_boost']
        net_range_boost = boost_values['range_level_percent'] + boost_values['range_level_boost']
        net_strength_boost = boost_values['strength_level_percent'] + boost_values['strength_level_boost']
        net_necro_boost = boost_values['necro_level_percent'] + boost_values['necro_level_boost']

        return [net_magic_boost, net_range_boost, net_strength_boost, net_necro_boost]

    #computes total level boost for purpose of computes ability dmg
    def calculate_levels(self):
        aura_boosts = self.aura_level_boost()
        potion_boosts = self.potion_level_boost()
        base_levels = [self.baseMagic, self.baseRange, self.baseStr, self.baseNecro]

        total_levels = [int(x + y + z) for x, y, z in zip(aura_boosts, potion_boosts, base_levels)]
        
        self.magicLvl = total_levels[0]
        self.rangeLvl = total_levels[1]
        self.strLvl = total_levels[2]
        self.necroLvl = total_levels[3]
    
    def compute_bonus(self):
        bonus = [0, 0, 0, 0]
        gear_slots = {
            'helm': 'helm',
            'body': 'body',
            'legs': 'legs',
            'boots': 'boots',
            'gloves': 'gloves',
            'neck': 'neck',
            'cape': 'cape',
            'ring': 'ring',
            'pocket': 'pocket'        
        }

        for item in self.utils.gear:
            slot = item['slot']
            if item['name'] == self.armour.get(gear_slots.get(slot)):
                bonus[0] += item['magic_bonus']
                bonus[1] += item['range_bonus']
                bonus[2] += item['melee_bonus']
                bonus[3] += item['necro_bonus']
           
        if self.reaperCrew == True:
            bonus[0] += 12
            bonus[1] += 12
            bonus[2] += 12
            bonus[3] += 12
        
        self.magicBonus = bonus[0]
        self.rangeBonus = bonus[1]
        self.strBonus = bonus[2]
        self.necroBonus = bonus[3]
    
    #dual wield ability dmg calc
    def dw_ability_dmg(self):
        base_ability_dmg = 0

        oh = next((w for w in self.utils.weapons if w['name'] == self.oh), None)   

        if oh['style'] == 'MAGIC':
            base_ability_dmg += int(0.5 * (int(2.5 * self.magicLvl) + int(9.6 * min(oh['dmg_tier'],self.autocast) + int(self.magicBonus))))
        elif oh['style'] == 'RANGE':
            base_ability_dmg += int(0.5 * (int(2.5 * self.rangeLvl) + int(9.6 * min(oh['dmg_tier'],self.ammo) + int(self.rangeBonus))))
        elif oh['style'] == 'MELEE':
            base_ability_dmg += int(0.5 * (int(2.5 * self.strLvl) + int(9.6 * oh['dmg_tier'] + int(self.strBonus))))
        else:
            pass
        
        mh = next((w for w in self.utils.weapons if w['name'] == self.mh), None)

        if mh['style']== 'MAGIC':
            base_ability_dmg += int(2.5 * self.magicLvl) + int(9.6 * min(mh['dmg_tier'], self.autocast) + int(self.magicBonus))
        elif mh['style'] == 'RANGE':
            base_ability_dmg += int(2.5 * self.rangeLvl) + int(9.6 * min(mh['dmg_tier'], self.ammo) + int(self.rangeBonus))
        elif mh['style'] == 'MELEE':
            base_ability_dmg += int(2.5 * self.strLvl) + int(9.6 * mh['dmg_tier'] + int(self.strBonus))
        else:
            pass

        return base_ability_dmg

    #two handed ability dmg calc
    def th_ability_dmg(self):
        base_ability_dmg = 0 

        th = next((w for w in self.utils.weapons if w['name'] == self.th), None)

        if th['style'] == 'MAGIC':
            base_ability_dmg += int(2.5 * self.magicLvl) + int(1.25 * self.magicLvl) + int(14.4 * min(th['dmg_tier'], self.autocast) + 1.5 * int(self.magicBonus))
        elif th['style'] == 'RANGE':
            base_ability_dmg += int(2.5 * self.rangeLvl) + int(1.25 * self.rangeLvl) + int(14.4 * min(th['dmg_tier'], self.ammo) + 1.5 * int(self.rangeBonus))
        elif th['style'] == 'MELEE':
            base_ability_dmg += int(2.5 * self.strLvl) + int(1.25 * self.strLvl) + int(14.4 * th['dmg_tier'] + 1.5 * int(self.strBonus))
        else:
            pass
        return base_ability_dmg
    
    #mainhand shielf ability dmg calc
    def ms_ability_dmg(self):
        base_ability_dmg = 0

        mh = next((w for w in self.utils.weapons if w['name'] == self.inputs.mh_input), None)

        if mh['style'] == 'MAGIC':
            base_ability_dmg += int(2.5 * self.magicLvl) + int(9.6 * min(mh['dmg_tier'], self.autocast) + int(self.magicBonus))
        elif mh['style'] == 'RANGE':
            base_ability_dmg += int(2.5 * self.rangeLvl) + int(9.6 * min(mh['dmg_tier'], self.ammo) + int(self.rangeBonus))
        elif mh['style'] == 'MELEE':
            base_ability_dmg += int(2.5 * self.strLvl) + int(9.6 * mh['dmg_tier'] + int(self.strBonus))
        else:
            pass

        return base_ability_dmg

    #helper function to use the correct ability dmg based on the casting weapon type from inputs.py
    def base_ability_dmg(self):
        if self.type == '2h':
            return self.th_ability_dmg()
        elif self.type == 'dw':
            return self.dw_ability_dmg()
        elif self.type == 'ms':
            return self.ms_ability_dmg()
        else:
            return 0


