from resources import Utils
from on_cast import CAST_INS
from settings import SET_INS
from duration_effects import EFF_INS
from damage_store import DamageStore

class GameState:
    def __init__(self):
        self.utils = Utils()
        self.autocast = None
        self.exsang = [0,0]
        self.incite = [0,0]
        self.barge = [False,0]
        self.bleed = False
        self.bolg = 0
        self.rubyAurora = [0,0,0,0]
        self.gconc = 0
        self.needle = False
        self.channelers = False

        self.cooldowns = []
        self.adren = []
        self.damage = []
    
    def set_autocast(self):
            self.autocast = CAST_INS.ability.split(' ')[1]
        
    def get_exsang(self):
        if CAST_INS.tick > self.exsang[1]:
            self.exsang[0] = 0
            self.exsang[1] = 0
        else:
            pass
        
        if self.autocast[0] == 'exsang':
            for abil in self.utils.abilities:
                if abil['name'] == CAST_INS.ability:
                    break
                if abil['style'] == 'MAGIC':
                        self.exsang[0] += 1
                        self.exsang[1] = CAST_INS.tick + 34
                
                if CAST_INS.ability == 'wrack' and self.exsang[0] == 13:
                    self.exsang[0] = 0
                    
                if self.exsang[0] > 12:
                    self.exsang[0] = 12
        else:
            pass
            
    def get_incite(self):
        if CAST_INS.tick > self.incite[1]:
            self.incite[0] = 0
            self.incite[1] = 0
        else:
            pass
        
        if self.autocast[0] == 'incite':
            for abil in self.utils.abilities:
                if abil['name'] == CAST_INS.ability:
                    break
                if abil['style'] == 'MAGIC':
                        self.incite[0] += 1
                        self.incite[1] = CAST_INS.tick + 34
                if self.incite[0] > 5:
                    self.incite[0] = 5
        else:
            pass
            
    def set_barge(self, buffer):
        if buffer > 8:
            if CAST_INS.ability == 'greater barge':
                self.barge[0] = True
                self.barge[1] = CAST_INS.tick + 10
            else:
                pass
        else:
            self.barge[0] = False
            self.barge[1] = 0
    
    def set_bleed(self):
        if CAST_INS.type_n == 'BLEED':
            self.bleed = True
        elif CAST_INS.type_n == 'CHANNELED' and self.barge[0] == True:
            self.bleed = True
            self.barge[0] = False
        else:
            pass
        
    def get_bolg(self):
        if SET_INS.th == 'Bow of the last guardian' and SET_INS.preset == '2h':
            self.bolg += 1
        else:
            pass
        
        if EFF_INS.bolg == True and self.bolg == 4:
            self.bolg = 0
        elif self.bolg == 8:
            self.bolg = 0
        else:
            pass
    
    def set_gconc(self):
        pass
    
    def get_ruby_aurora(self):
        pass
    
    def set_needle(self):
        pass
    
    def set_channelers(self):
        pass
        
STATE_INS = GameState()
    
    