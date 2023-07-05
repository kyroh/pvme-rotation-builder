from resources import Utils
from dmg_boost import CheckDmgBoosts

class OnCast:
    def __init__(self):
        self.utils = Utils()
        self.boost = CheckDmgBoosts()
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
            
    def prayer_dmg(self, prayer):
        boost = next((b for b in self.utils.boosts if b['name'] == prayer), None)
        if boost is None:
            pass
        else:
            self.prayer_boost = [boost["magic_dmg_percent"], boost["range_dmg_percent"], boost["strength_dmg_percent"], boost["necro_dmg_percent"]]
        
    
    def fixedDmg(self, ability_dmg):
        prayer_map = {
            'MAGIC': self.prayer_boost[0],
            'RANGE': self.prayer_boost[1],
            'MELEE': self.prayer_boost[2],
            'NECRO': self.prayer_boost[3]
        }
        if self.type_n != 'BLEED':
            if self.style in prayer_map:
                self.fixed = int(int(ability_dmg * self.fixed) * (1 + prayer_map[self.style]))
            else:
                pass
        else:
            self.fixed = int(ability_dmg * self.fixed)

    def varDmg(self, ability_dmg):
        prayer_map = {
            'MAGIC': self.prayer_boost[0],
            'RANGE': self.prayer_boost[1],
            'MELEE': self.prayer_boost[2],
            'NECRO': self.prayer_boost[3]
        }
        
        if self.type_n != 'BLEED':
            if self.style in prayer_map:
                self.variable = int(int(ability_dmg * self.variable) * (1 + prayer_map[self.style]))
            else:
                pass
        else:
            self.variable = int(ability_dmg * self.variable)
    
    def dpl(self, base_levels, boosted_levels):
        levels = base_levels
        b_levels = boosted_levels
        
        if self.style in ('MAGIC', 'RANGE', 'MELEE'):
            if self.style == 'MAGIC':
                base_level = levels[0]
                boosted_level = b_levels[0]
            elif self.style == 'RANGE':
                base_level = levels[1]
                boosted_level = b_levels[1]
            elif self.style == 'MELEE':
                base_level = levels[2]
                boosted_level = b_levels[2]
            elif self.style == 'NECRO':
                base_level = levels[3]
                boosted_level = b_levels[3]
            else:
                pass
        
            level_difference = boosted_level - base_level
            self.fixed += int(level_difference * 4)
            self.variable += int(level_difference * 4)
    
    def dmg_boost(self):
        if self.style == 'MAGIC':
            if self.ability == 'sunshine' or self.ability == 'greater sunshine' or self.tick > self.sun[1]:
                    self.sun = self.boost.check_boost(self.ability, self.tick)
            if self.ability == 'metamorphosis' or self.tick > self.meta[1]:
                    self.meta = self.boost.check_boost(self.ability, self.tick)
            else:
                pass
            
            if self.sun[0] == True and self.type_n != 'BLEED':
                self.fixed = int(1.5 * self.fixed)
                self.variable = int(1.5 * self.variable)
            if self.meta[0] == True:
                self.fixed = int(1.625 * self.fixed)
                self.variable = int(1.625 * self.variable)
            else:
                pass
        
        elif self.style == 'RANGE':
            if self.ability == 'death swiftness' or self.ability == 'greater death swiftness' or self.tick > self.swift[1]:
                    self.swift = self.boost.check_boost(self.ability, self.tick)
            else:
                pass
            
            if self.swift[0] == True and self.type_n != 'BLEED':
                self.fixed = int(1.5 * self.fixed)
                self.variable = int(1.5 * self.variable)
            else:
                pass
            
        elif self.style == 'MELEE':
            if self.ability == 'berserk' or self.tick > self.sun[1]:
                    self.zerk = self.boost.check_boost(self.ability, self.tick)
            if self.ability == 'zgs' or self.tick > self.meta[1]:
                    self.zgs = self.boost.check_boost(self.ability, self.tick)
            else:
                pass
            
            if self.zerk[0] == True and self.type_n != 'BLEED':
                self.fixed = int(2 * self.fixed)
                self.variable = int(2 * self.variable)
            if self.zgs[0] == True:
                self.fixed = int(1.25 * self.fixed)
                self.variable = int(1.25 * self.variable)
            else:
                pass
        
        else:
            pass
            
    
    def precise(self, rank):
        if self.type_n != 'BLEED':
            precise = int(0.015 * (self.fixed + self.variable) * rank)
            self.fixed += precise
            self.variable -= precise
        else:
            pass
    
    def equilibrium(self, aura, rank):
        if self.type_n != 'BLEED':
            if aura == 'Equilibrium':
                self.fixed += 0.25 * self.variable
                self.variable -= 0.5 * self.variable
            else:
                self.fixed += 0.03 * self.variable * rank
                self.variable -= 0.04 * self.variable * rank
        else:
            pass
    
    def aura_passive(self, aura):
        boost = None
        for b in self.utils.boosts:
            if b['name'] == aura:
                boost = b
                break
        if self.style == 'MAGIC' and self.sun[0] == False:
            self.fixed += int(self.fixed * boost['magic_dmg_percent'])
            self.variable += int(self.variable * boost['magic_dmg_percent'])
        else:
            pass
    
levels = [99, 99, 99, 99]
constants = [None, None, True]
weapons = ['Wand of the praesul', 'Imperium core', 'Staff of Sliske', None, None]

armour = {
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



    
    