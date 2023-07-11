from resources import Utils
from settings import SET_INS
from duration_effects import EFF_INS

class AbilityDmg:
    def __init__(self): 
        self.utils = Utils()
        
        self.armour = {
            'helm': SET_INS.helm,
            'body': SET_INS.body,
            'legs': SET_INS.legs,
            'boots': SET_INS.boots,
            'gloves': SET_INS.gloves,
            'neck': SET_INS.neck,
            'cape': SET_INS.cape,
            'ring': SET_INS.ring,
            'pocket': SET_INS.pocket        
        }
        
        self.magicLvl = 0
        self.rangeLvl = 0
        self.strLvl = 0
        self.necroLvl = 0
        
        self.magicBonus = 0
        self.rangeBonus = 0
        self.strBonus = 0
        self.necroBonus = 0
        
        self.ad = 0
    
    # computes the number of boosted levels derived from aura
    # boost is the aura name that is looked up in boost.json
    # boost_percent is the level boost from the json lookup
    ################
    def aura_level_boost(self):
        boost = next((b for b in self.utils.boosts if b['name'] == SET_INS.aura), None)
        if boost is None:
            return [0, 0, 0, 0]

        magic_boost_percent = SET_INS.magic_lvl * boost.get('magic_level_percent', 0)
        range_boost_percent = SET_INS.range_lvl * boost.get('range_level_percent', 0)
        strength_boost_percent = SET_INS.str_lvl * boost.get('strength_level_percent', 0)
        necro_boost_percent = SET_INS.necro_lvl * boost.get('necro_level_percent', 0)

        return [magic_boost_percent, range_boost_percent, strength_boost_percent, necro_boost_percent]

    # computes the number of boosted levels derived from potions
    # boost is the potion name that is looked up in boost.json
    # boost_values is a map of the results from the json lookup
    # net_boost is the sum of the int level boost + % level boost
    ################
    def potion_level_boost(self):
        boost = next((b for b in self.utils.boosts if b['name'] == SET_INS.potion), None)
        if boost is None:
            return [0, 0, 0, 0]

        boost_values = {
            'magic_level_percent': SET_INS.magic_lvl * boost.get('magic_level_percent', 0),
            'range_level_percent': SET_INS.range_lvl * boost.get('range_level_percent', 0),
            'strength_level_percent': SET_INS.str_lvl * boost.get('strength_level_percent', 0),
            'necro_level_percent': SET_INS.necro_lvl * boost.get('necro_level_percent', 0),
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

    # computes total boosted level for each skill
    # appends the individually computed aura and potion boost to the base levels
    ################
    def calculate_levels(self):
        aura_boosts = self.aura_level_boost()
        potion_boosts = self.potion_level_boost()
        base_levels = [SET_INS.magic_lvl, SET_INS.range_lvl, SET_INS.str_lvl, SET_INS.necro_lvl]

        levels = [int(x + y + z) for x, y, z in zip(aura_boosts, potion_boosts, base_levels)]
        if (EFF_INS.blood_ess[0] == True and EFF_INS.blood_ess[2] == 'MAGIC') and (SET_INS.potion == None or 'verload' not in SET_INS.potion):
            self.magicLvl = int((1.14 * levels[0]) + 2)
        else:
            self.magicLvl = levels[0]
            
        if (EFF_INS.blood_ess[0] == True and EFF_INS.blood_ess[2] == 'RANGE') and (SET_INS.potion == None or 'verload' not in SET_INS.potion):
            self.rangeLvl = int((1.14 * levels[1]) + 2)
        else:
            self.rangeLvl = levels[1]
            
        if (EFF_INS.blood_ess[0] == True and EFF_INS.blood_ess[2] == 'MELEE') and (SET_INS.potion == None or 'verload' not in SET_INS.potion):
            self.strLvl = int((1.14 * levels[2]) + 2)
        else:
            self.strLvl = levels[2]
            
        if (EFF_INS.blood_ess[0] == True and EFF_INS.blood_ess[2] == 'NECRO') and (SET_INS.potion == None or 'verload' not in SET_INS.potion):
            self.necroLvl = int((1.14 * levels[3]) + 2)
        else:
            self.necroLvl = levels[3]
    
    # computes the armour bonus portion of ability dmg
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
           
        if SET_INS.reaper_crew == True:
            bonus[0] += 12
            bonus[1] += 12
            bonus[2] += 12
            bonus[3] += 12
        
        self.magicBonus = bonus[0]
        self.rangeBonus = bonus[1]
        self.strBonus = bonus[2]
        self.necroBonus = bonus[3]
    
    # compute dual wield ability dmg
    ################
    def dw_ability_dmg(self):
        base_ability_dmg = 0

        oh = next((w for w in self.utils.weapons if w['name'] == SET_INS.oh['name']), None)   

        if oh['style'] == 'MAGIC':
            base_ability_dmg += int(0.5 * (int(2.5 * self.magicLvl) + int(9.6 * min(oh['dmg_tier'],SET_INS.auto_cast) + int(self.magicBonus))))
        elif oh['style'] == 'RANGE':
            base_ability_dmg += int(0.5 * (int(2.5 * self.rangeLvl) + int(9.6 * min(oh['dmg_tier'],SET_INS.ammo) + int(self.rangeBonus))))
        elif oh['style'] == 'MELEE':
            base_ability_dmg += int(0.5 * (int(2.5 * self.strLvl) + int(9.6 * oh['dmg_tier'] + int(self.strBonus))))
        else:
            pass
        
        mh = next((w for w in self.utils.weapons if w['name'] == SET_INS.mh['name']), None)

        if mh['style']== 'MAGIC':
            base_ability_dmg += int(2.5 * self.magicLvl) + int(9.6 * min(mh['dmg_tier'], SET_INS.auto_cast) + int(self.magicBonus))
        elif mh['style'] == 'RANGE':
            base_ability_dmg += int(2.5 * self.rangeLvl) + int(9.6 * min(mh['dmg_tier'], SET_INS.ammo) + int(self.rangeBonus))
        elif mh['style'] == 'MELEE':
            base_ability_dmg += int(2.5 * self.strLvl) + int(9.6 * mh['dmg_tier'] + int(self.strBonus))
        else:
            pass

        return base_ability_dmg

    # compute two hand ability dmg
    ################
    def th_ability_dmg(self):
        base_ability_dmg = 0 

        th = next((w for w in self.utils.weapons if w['name'] == SET_INS.th['name']), None)

        if th['style'] == 'MAGIC':
            base_ability_dmg += int(2.5 * self.magicLvl) + int(1.25 * self.magicLvl) + int(14.4 * min(th['dmg_tier'], SET_INS.auto_cast) + 1.5 * int(self.magicBonus))
        elif th['style'] == 'RANGE':
            base_ability_dmg += int(2.5 * self.rangeLvl) + int(1.25 * self.rangeLvl) + int(14.4 * min(th['dmg_tier'], SET_INS.ammo) + 1.5 * int(self.rangeBonus))
        elif th['style'] == 'MELEE':
            base_ability_dmg += int(2.5 * self.strLvl) + int(1.25 * self.strLvl) + int(14.4 * th['dmg_tier'] + 1.5 * int(self.strBonus))
        else:
            pass
        return base_ability_dmg
    
    # compute mainhand + shield ability dmg
    ################
    def ms_ability_dmg(self):
        base_ability_dmg = 0

        mh = next((w for w in self.utils.weapons if w['name'] == self.inputs.mh_input), None)

        if mh['style'] == 'MAGIC':
            base_ability_dmg += int(2.5 * self.magicLvl) + int(9.6 * min(mh['dmg_tier'], SET_INS.auto_cast) + int(self.magicBonus))
        elif mh['style'] == 'RANGE':
            base_ability_dmg += int(2.5 * self.rangeLvl) + int(9.6 * min(mh['dmg_tier'], SET_INS.ammo) + int(self.rangeBonus))
        elif mh['style'] == 'MELEE':
            base_ability_dmg += int(2.5 * self.strLvl) + int(9.6 * mh['dmg_tier'] + int(self.strBonus))
        else:
            pass

        return base_ability_dmg

    # identify what ability dmg should be calculated based on the user's casting weapon
    ################
    def base_ability_dmg(self):
        if SET_INS.preset == '2h':
            self.ad = self.th_ability_dmg()
        elif SET_INS.preset == 'dw':
            self.ad = self.dw_ability_dmg()
        elif SET_INS.preset == 'ms':
            self.ad = self.ms_ability_dmg()
        else:
            pass

AD_INS = AbilityDmg()