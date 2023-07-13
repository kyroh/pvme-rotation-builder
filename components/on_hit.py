

from resources import Utils
from dmg_boost import DMG_BOOST_INS
from settings import SET_INS
from ability_dmg import AD_INS
from get_entry import ENTRY_INS
from game_state import STATE_INS
from duration_effects import EFF_INS

# TODO: Change OnCast to OnHit for the class name, file name, and all reference to the instance

class OnHit:
    def __init__(self):
        self.utils = Utils()
        self.sun = [False, 0]
        self.meta = [False, 0]
        self.swift = [False, 0]
        self.zerk = [False, 0]
        self.zgs = [False, 0]
        self.prayer_boost = [0,0,0,0]
        self.params = [None, 0, 0, None]
        
        self.fixed = 0
        ENTRY_INS.variable = 0
        self.damage = 0
    
    # gets the prayer modifier for the current active
    ################
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
        
    # computes fixed damage from ability damage and the AD % from the abilities dict
    ################
    def get_fixed(self):
        prayer_map = {
            'MAGIC': self.prayer_boost[0],
            'RANGE': self.prayer_boost[1],
            'MELEE': self.prayer_boost[2],
            'NECRO': self.prayer_boost[3]
        }
        if ENTRY_INS.type_n != 'BLEED':
            if ENTRY_INS.style in prayer_map:
                self.fixed = int(int(AD_INS.ad * ENTRY_INS.fixed) * (1 + prayer_map[ENTRY_INS.style]))
            else:
                pass
        else:
            self.fixed = int(AD_INS.ad * ENTRY_INS.fixed)

    # computes variable damage from ability damage and the AD % from the abilities dict
    ################
    def get_var(self):
        prayer_map = {
            'MAGIC': self.prayer_boost[0],
            'RANGE': self.prayer_boost[1],
            'MELEE': self.prayer_boost[2],
            'NECRO': self.prayer_boost[3]
        }
        
        if ENTRY_INS.type_n != 'BLEED':
            if ENTRY_INS.style in prayer_map:
                ENTRY_INS.variable = int(int(AD_INS.ad * ENTRY_INS.variable) * (1 + prayer_map[ENTRY_INS.style]))
            else:
                pass
        else:
            ENTRY_INS.variable = int(AD_INS.ad * ENTRY_INS.variable)
    
    
    # computes DPL might need to remove if Mod Sponge removes DPL
    ################
    def dpl(self):
        if ENTRY_INS.style in ('MAGIC', 'RANGE', 'MELEE', 'NECRO'):
            if ENTRY_INS.style == 'MAGIC':
                base_level = SET_INS.magic_lvl
                boosted_level = AD_INS.magicLvl
            elif ENTRY_INS.style == 'RANGE':
                base_level = SET_INS.range_lvl
                boosted_level = AD_INS.rangeLvl
            elif ENTRY_INS.style == 'MELEE':
                base_level = SET_INS.str_lvl
                boosted_level = AD_INS.strLvl
            elif ENTRY_INS.style == 'NECRO':
                base_level = SET_INS.necro_lvl
                boosted_level = AD_INS.necroLvlLvl
            else:
                pass
        
            level_difference = boosted_level - base_level
            ENTRY_INS.fixed += int(level_difference * 4)
            ENTRY_INS.variable += int(level_difference * 4)
    
    # checks if dmg boosting effect like sun zerk etc are active and computes fixed and variable dmg
    ################
    def dmg_boost(self):
        if ENTRY_INS.style == 'MAGIC':
            if DMG_BOOST_INS.sun[0] == True and ENTRY_INS.type_n != 'BLEED':
                ENTRY_INS.fixed = int(1.5 * ENTRY_INS.fixed)
                ENTRY_INS.variable = int(1.5 * ENTRY_INS.variable)
            if DMG_BOOST_INS.meta[0] == True:
                ENTRY_INS.fixed = int(1.625 * ENTRY_INS.fixed)
                ENTRY_INS.variable = int(1.625 * ENTRY_INS.variable)
            else:
                pass
        elif ENTRY_INS.style == 'RANGE':
            if DMG_BOOST_INS.swift[0] == True and ENTRY_INS.type_n != 'BLEED':
                ENTRY_INS.fixed = int(1.5 * ENTRY_INS.fixed)
                ENTRY_INS.variable = int(1.5 * ENTRY_INS.variable)
            else:
                pass
        elif ENTRY_INS.style == 'MELEE':
            if DMG_BOOST_INS.zerk[0] == True and ENTRY_INS.type_n != 'BLEED':
                ENTRY_INS.fixed = int(2 * ENTRY_INS.fixed)
                ENTRY_INS.variable = int(2 * ENTRY_INS.variable)
            if DMG_BOOST_INS.zgs[0] == True:
                ENTRY_INS.fixed = int(1.25 * ENTRY_INS.fixed)
                ENTRY_INS.variable = int(1.25 * ENTRY_INS.variable)
            else:
                pass
        else:
            pass   
    
    def precise(self):
        precise = int(0.015 * (ENTRY_INS.fixed + ENTRY_INS.variable) * SET_INS.perks['precise'])
        ENTRY_INS.fixed += precise
        ENTRY_INS.variable -= precise
    
    def equilibrium(self):
        if SET_INS.aura == 'Equilibrium':
            ENTRY_INS.fixed += int(0.25 * ENTRY_INS.variable)
            ENTRY_INS.variable -= int(0.5 * ENTRY_INS.variable)
        else:
            ENTRY_INS.fixed += int(0.03 * ENTRY_INS.variable * SET_INS.perks['equilibrium'])
            ENTRY_INS.variable -= int(0.04 * ENTRY_INS.variable * SET_INS.perks['equilibrium'])
    
    def aura_passive(self):
        boost = None
        for b in self.utils.boosts:
            if b['name'] == SET_INS.aura:
                boost = b
                break
        if boost == None:
            pass
        else:
            if ENTRY_INS.style == 'MAGIC' and self.sun[0] == False:
                ENTRY_INS.fixed += int(ENTRY_INS.fixed * boost['magic_dmg_percent'])
                ENTRY_INS.variable += int(ENTRY_INS.variable * boost['magic_dmg_percent'])
            elif ENTRY_INS.style == 'RANGE' and self.sun[0] == False:
                ENTRY_INS.fixed += int(ENTRY_INS.fixed * boost['range_dmg_percent'])
                ENTRY_INS.variable += int(ENTRY_INS.variable * boost['range_dmg_percent'])
            elif ENTRY_INS.style == 'MELEE' and self.sun[0] == False:
                ENTRY_INS.fixed += int(ENTRY_INS.fixed * boost['strength_dmg_percent'])
                ENTRY_INS.variable += int(ENTRY_INS.variable * boost['strength_dmg_percent'])
            elif ENTRY_INS.style == 'NECRO' and self.sun[0] == False:
                ENTRY_INS.fixed += int(ENTRY_INS.fixed * boost['necro_dmg_percent'])
                ENTRY_INS.variable += int(ENTRY_INS.variable * boost['necro_dmg_percent'])
            else:
                pass
        
    def exsang_damage(self):
        if ENTRY_INS.class_n == 'BASIC':
            exsang = int(0.01 * STATE_INS.exsang[0])
            ENTRY_INS.fixed = int(ENTRY_INS.fixed * exsang)
            ENTRY_INS.variable = int(ENTRY_INS.variable * exsang)
        else:
            pass
    
    def scriptue_of_ful(self):
        if STATE_INS.needle == True:
            pass
        else:
            ENTRY_INS.fixed = int(ENTRY_INS.fixed * 1.2)
            ENTRY_INS.variable = int(ENTRY_INS.variable * 1.2)

    
    def ruby_aurora_damage(self):
        ruby_aurora = int(0.01 * STATE_INS.rubyAurora[0])
        ENTRY_INS.fixed = int(ENTRY_INS.fixed * ruby_aurora)
        ENTRY_INS.variable = int(ENTRY_INS.variable * ruby_aurora)
        
    def needle_damage(self):
        if EFF_INS.scripture_ful[0] == True:
            ENTRY_INS.fixed = int(ENTRY_INS.fixed * 1.27)
            ENTRY_INS.variable = int(ENTRY_INS.variable * 1.27)
            STATE_INS.needle = False
        else:
            ENTRY_INS.fixed = int(ENTRY_INS.fixed * 1.07)
            ENTRY_INS.variable = int(ENTRY_INS.variable * 1.07)
            STATE_INS.needle = False
        
    def ful_arrow_damage(self):
            ENTRY_INS.fixed = int(ENTRY_INS.fixed * 1.15)
            ENTRY_INS.variable = int(ENTRY_INS.variable * 1.15)
        
    def base_damage(self, output):
        if output == 'MIN':
            self.damage = ENTRY_INS.fixed
        elif output == 'AVG':
            self.damage = int(ENTRY_INS.fixed + (ENTRY_INS.variable * 0.5))
        elif output == 'MAX':
            self.damage = ENTRY_INS.fixed + ENTRY_INS.variable
        else:
            pass

HIT_INS = OnHit()