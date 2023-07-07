from resources import Utils
from dmg_boost import DMG_BOOST_INS
from settings import SET_INS
from ability_dmg import AD_INS

class OnCast:
    def __init__(self):
        self.utils = Utils()
        self.sun = [False, 0]
        self.meta = [False, 0]
        self.swift = [False, 0]
        self.zerk = [False, 0]
        self.zgs = [False, 0]
        self.prayer_boost = [0,0,0,0]
        self.params = [None, 0, 0, None]
        
        self.ability = None
        self.style = None
        self.fixed = 0
        self.variable = 0
        self.type_n = None
        self.tick = 0
        self.damage = 0
    
    def get_abil(self, ability, tick):
        for abil in self.utils.abilities:
            if abil['name'] == ability:
                self.ability = abil['name']
                self.style = abil['style']
                self.fixed = abil['fixed']
                self.variable = abil['var']
                self.type_n = abil['type_n']
                self.tick = tick
            else:
                pass
            
    def prayer_dmg(self):
        boost = next((b for b in self.utils.boosts if b['name'] == SET_INS.prayer), None)
        if boost is None:
            pass
        else:
            self.prayer_boost = [
                boost["magic_dmg_percent"], 
                boost["range_dmg_percent"], 
                boost["strength_dmg_percent"], 
                boost["necro_dmg_percent"]
            ]
        
    
    def fixedDmg(self):
        prayer_map = {
            'MAGIC': self.prayer_boost[0],
            'RANGE': self.prayer_boost[1],
            'MELEE': self.prayer_boost[2],
            'NECRO': self.prayer_boost[3]
        }
        if self.type_n != 'BLEED':
            if self.style in prayer_map:
                self.fixed = int(int(AD_INS.ad * self.fixed) * (1 + prayer_map[self.style]))
            else:
                pass
        else:
            self.fixed = int(AD_INS.ad * self.fixed)

    def varDmg(self):
        prayer_map = {
            'MAGIC': self.prayer_boost[0],
            'RANGE': self.prayer_boost[1],
            'MELEE': self.prayer_boost[2],
            'NECRO': self.prayer_boost[3]
        }
        
        if self.type_n != 'BLEED':
            if self.style in prayer_map:
                self.variable = int(int(AD_INS.ad * self.variable) * (1 + prayer_map[self.style]))
            else:
                pass
        else:
            self.variable = int(AD_INS.ad * self.variable)
    
    def dpl(self):
        if self.style in ('MAGIC', 'RANGE', 'MELEE', 'NECRO'):
            if self.style == 'MAGIC':
                base_level = SET_INS.magic_lvl
                boosted_level = AD_INS.magicLvl
            elif self.style == 'RANGE':
                base_level = SET_INS.range_lvl
                boosted_level = AD_INS.rangeLvl
            elif self.style == 'MELEE':
                base_level = SET_INS.str_lvl
                boosted_level = AD_INS.strLvl
            elif self.style == 'NECRO':
                base_level = SET_INS.necro_lvl
                boosted_level = AD_INS.necroLvlLvl
            else:
                pass
        
            level_difference = boosted_level - base_level
            self.fixed += int(level_difference * 4)
            self.variable += int(level_difference * 4)
    
    def dmg_boost(self):
        if self.style == 'MAGIC':
            if DMG_BOOST_INS.sun[0] == True and self.type_n != 'BLEED':
                self.fixed = int(1.5 * self.fixed)
                self.variable = int(1.5 * self.variable)
            if DMG_BOOST_INS.meta[0] == True:
                self.fixed = int(1.625 * self.fixed)
                self.variable = int(1.625 * self.variable)
            else:
                pass
        elif self.style == 'RANGE':
            if DMG_BOOST_INS.swift[0] == True and self.type_n != 'BLEED':
                self.fixed = int(1.5 * self.fixed)
                self.variable = int(1.5 * self.variable)
            else:
                pass
        elif self.style == 'MELEE':
            if DMG_BOOST_INS.zerk[0] == True and self.type_n != 'BLEED':
                self.fixed = int(2 * self.fixed)
                self.variable = int(2 * self.variable)
            if DMG_BOOST_INS.zgs[0] == True:
                self.fixed = int(1.25 * self.fixed)
                self.variable = int(1.25 * self.variable)
            else:
                pass
        else:
            pass
            
    
    def precise(self):
        if self.type_n != 'BLEED':
            precise = int(0.015 * (self.fixed + self.variable) * SET_INS.perks['precise'])
            self.fixed += precise
            self.variable -= precise
        else:
            pass
    
    def equilibrium(self):
        if self.type_n != 'BLEED':
            if SET_INS.aura == 'Equilibrium':
                self.fixed += int(0.25 * self.variable)
                self.variable -= int(0.5 * self.variable)
            else:
                self.fixed += int(0.03 * self.variable * SET_INS.perks['equilibrium'])
                self.variable -= int(0.04 * self.variable * SET_INS.perks['equilibrium'])
        else:
            pass
    
    def aura_passive(self):
        boost = None
        for b in self.utils.boosts:
            if b['name'] == SET_INS.aura:
                boost = b
                break
        if boost == None:
            pass
        else:
            if self.style == 'MAGIC' and self.sun[0] == False:
                self.fixed += int(self.fixed * boost['magic_dmg_percent'])
                self.variable += int(self.variable * boost['magic_dmg_percent'])
            elif self.style == 'RANGE' and self.sun[0] == False:
                self.fixed += int(self.fixed * boost['range_dmg_percent'])
                self.variable += int(self.variable * boost['range_dmg_percent'])
            elif self.style == 'MELEE' and self.sun[0] == False:
                self.fixed += int(self.fixed * boost['strength_dmg_percent'])
                self.variable += int(self.variable * boost['strength_dmg_percent'])
            elif self.style == 'NECRO' and self.sun[0] == False:
                self.fixed += int(self.fixed * boost['necro_dmg_percent'])
                self.variable += int(self.variable * boost['necro_dmg_percent'])
            else:
                pass
        
    def base_damage(self, output):
        if output == 'MIN':
            self.damage = self.fixed
        elif output == 'AVG':
            self.damage = int(self.fixed + (self.variable * 0.5))
        elif output == 'MAX':
            self.damage = self.fixed + self.variable
        else:
            pass

CAST_INS = OnCast()