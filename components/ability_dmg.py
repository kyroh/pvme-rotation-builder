from resources import Utils
from settings import Settings

class AbilityDmg:
    def __init__(self): 
        self.utils = Utils()
        self.settings = Settings()
        
        self.armour = {
            'helm': self.settings.helm,
            'body': self.settings.body,
            'legs': self.settings.legs,
            'boots': self.settings.boots,
            'gloves': self.settings.gloves,
            'neck': self.settings.neck,
            'cape': self.settings.cape,
            'ring': self.settings.ring,
            'pocket': self.settings.pocket        
        }
        
        self.magicLvl = 0
        self.rangeLvl = 0
        self.strLvl = 0
        self.necroLvl = 0
        
        self.magicBonus = 0
        self.rangeBonus = 0
        self.strBonus = 0
        self.necroBonus = 0
    
    # PURPOSE - computes the number of boosted levels derived from aura
    # boost is the aura name that is looked up in boost.json
    # boost_percent is the level boost from the json lookup
    ################
    def aura_level_boost(self):
        boost = next((b for b in self.utils.boosts if b['name'] == self.settings.aura), None)
        if boost is None:
            return [0, 0, 0, 0]

        magic_boost_percent = self.settings.magic_lvl * boost.get('magic_level_percent', 0)
        range_boost_percent = self.settings.range_lvl * boost.get('range_level_percent', 0)
        strength_boost_percent = self.settings.str_lvl * boost.get('strength_level_percent', 0)
        necro_boost_percent = self.settings.necro_lvl * boost.get('necro_level_percent', 0)

        return [magic_boost_percent, range_boost_percent, strength_boost_percent, necro_boost_percent]

    # PURPOSE - computes the number of boosted levels derived from potions
    # boost is the potion name that is looked up in boost.json
    # boost_values is a map of the results from the json lookup
    # net_boost is the sum of the int level boost + % level boost
    ################
    def potion_level_boost(self):
        boost = next((b for b in self.utils.boosts if b['name'] == self.settings.potion), None)
        if boost is None:
            return [0, 0, 0, 0]

        boost_values = {
            'magic_level_percent': self.settings.magic_lvl * boost.get('magic_level_percent', 0),
            'range_level_percent': self.settings.range_lvl * boost.get('range_level_percent', 0),
            'strength_level_percent': self.settings.str_lvl * boost.get('strength_level_percent', 0),
            'necro_level_percent': self.settings.necro_lvl * boost.get('necro_level_percent', 0),
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

    # PURPOSE - computes total boosted level for each skill
    # appends the individually computed aura and potion boost to the base levels
    ################
    def calculate_levels(self):
        aura_boosts = self.aura_level_boost()
        potion_boosts = self.potion_level_boost()
        base_levels = [self.settings.magic_lvl, self.settings.range_lvl, self.settings.str_lvl, self.settings.necro_lvl]

        total_levels = [int(x + y + z) for x, y, z in zip(aura_boosts, potion_boosts, base_levels)]
        
        self.magicLvl = total_levels[0]
        self.rangeLvl = total_levels[1]
        self.strLvl = total_levels[2]
        self.necroLvl = total_levels[3]
    
    # PURPOSE - computes the armour bonus portion of ability dmg
    # gear slots is a map that identifies what piece of gear it is looking up the bonusf or in gear.json
    # it iterates through all armour slots and adds the net armour bonus
    # if reaper crew is added
    ################
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
           
        if self.settings.reaper_crew == True:
            bonus[0] += 12
            bonus[1] += 12
            bonus[2] += 12
            bonus[3] += 12
        
        self.magicBonus = bonus[0]
        self.rangeBonus = bonus[1]
        self.strBonus = bonus[2]
        self.necroBonus = bonus[3]
    
    # PURPOSE - compute dual wield ability dmg
    ################
    def dw_ability_dmg(self):
        base_ability_dmg = 0

        oh = next((w for w in self.utils.weapons if w['name'] == self.settings.oh['name']), None)   

        if oh['style'] == 'MAGIC':
            base_ability_dmg += int(0.5 * (int(2.5 * self.magicLvl) + int(9.6 * min(oh['dmg_tier'],self.settings.auto_cast) + int(self.magicBonus))))
        elif oh['style'] == 'RANGE':
            base_ability_dmg += int(0.5 * (int(2.5 * self.rangeLvl) + int(9.6 * min(oh['dmg_tier'],self.settings.ammo) + int(self.rangeBonus))))
        elif oh['style'] == 'MELEE':
            base_ability_dmg += int(0.5 * (int(2.5 * self.strLvl) + int(9.6 * oh['dmg_tier'] + int(self.strBonus))))
        else:
            pass
        
        mh = next((w for w in self.utils.weapons if w['name'] == self.settings.mh['name']), None)

        if mh['style']== 'MAGIC':
            base_ability_dmg += int(2.5 * self.magicLvl) + int(9.6 * min(mh['dmg_tier'], self.settings.auto_cast) + int(self.magicBonus))
        elif mh['style'] == 'RANGE':
            base_ability_dmg += int(2.5 * self.rangeLvl) + int(9.6 * min(mh['dmg_tier'], self.settings.ammo) + int(self.rangeBonus))
        elif mh['style'] == 'MELEE':
            base_ability_dmg += int(2.5 * self.strLvl) + int(9.6 * mh['dmg_tier'] + int(self.strBonus))
        else:
            pass

        return base_ability_dmg

    # PURPOSE - compute two hand ability dmg
    ################
    def th_ability_dmg(self):
        base_ability_dmg = 0 

        th = next((w for w in self.utils.weapons if w['name'] == self.settings.th['name']), None)

        if th['style'] == 'MAGIC':
            base_ability_dmg += int(2.5 * self.magicLvl) + int(1.25 * self.magicLvl) + int(14.4 * min(th['dmg_tier'], self.settings.auto_cast) + 1.5 * int(self.magicBonus))
        elif th['style'] == 'RANGE':
            base_ability_dmg += int(2.5 * self.rangeLvl) + int(1.25 * self.rangeLvl) + int(14.4 * min(th['dmg_tier'], self.settings.ammo) + 1.5 * int(self.rangeBonus))
        elif th['style'] == 'MELEE':
            base_ability_dmg += int(2.5 * self.strLvl) + int(1.25 * self.strLvl) + int(14.4 * th['dmg_tier'] + 1.5 * int(self.strBonus))
        else:
            pass
        return base_ability_dmg
    
    # PURPOSE - compute mainhand + shield ability dmg
    ################
    def ms_ability_dmg(self):
        base_ability_dmg = 0

        mh = next((w for w in self.utils.weapons if w['name'] == self.inputs.mh_input), None)

        if mh['style'] == 'MAGIC':
            base_ability_dmg += int(2.5 * self.magicLvl) + int(9.6 * min(mh['dmg_tier'], self.settings.auto_cast) + int(self.magicBonus))
        elif mh['style'] == 'RANGE':
            base_ability_dmg += int(2.5 * self.rangeLvl) + int(9.6 * min(mh['dmg_tier'], self.settings.ammo) + int(self.rangeBonus))
        elif mh['style'] == 'MELEE':
            base_ability_dmg += int(2.5 * self.strLvl) + int(9.6 * mh['dmg_tier'] + int(self.strBonus))
        else:
            pass

        return base_ability_dmg

    # PURPOSE - identify what ability dmg should be calculated based on the user's casting weapon
    ################
    def base_ability_dmg(self):
        if self.settings.preset == '2h':
            return self.th_ability_dmg()
        elif self.settings.preset == 'dw':
            return self.dw_ability_dmg()
        elif self.settings.preset == 'ms':
            return self.ms_ability_dmg()
        else:
            return 0

ad = AbilityDmg()
ad.calculate_levels()
ad.compute_bonus()

dmg = ad.base_ability_dmg()

print(dmg)
