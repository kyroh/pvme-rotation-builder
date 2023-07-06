from resources import Utils
from on_cast import OnCast
from damage_store import DamageStore

class GameState:
    def __init__(self):
        self.utils = Utils()
        self.cast = OnCast()
        self.autocast = None
        self.exsang = [0,0]
        self.incite = [0,0]
        self.vuln = [0,0]
        self.sc = [0,0]
        self.barge = [False,0]
        self.bleed = False
        self.rubyAurora = [0,0,0,0]
        self.gconc = 0
        self.natty = False
        self.dba = False
        self.needle = False
        self.bolg = False
        self.channelers = False

        self.cooldowns = []
        self.adren = []
        self.damage = []
    
    def setAutoCast(self, ability):
            self.autocast = ability.split(' ')[1]
        
    def getExsang(self, ability, tick):
        if tick > self.exsang[1]:
            self.exsang[0] = 0
            self.exsang[1] = 0
        else:
            pass
        
        if ability == 'wrack' and self.exsang[0] == 12:
            self.exsang[0] = 0
        
        if self.autocast[0] == 'exsang':
            for abil in self.utils.abilities:
                if abil['name'] == ability:
                    break
                if abil['style'] == 'MAGIC':
                        self.exsang[0] += 1
                        self.exsang[1] = tick + 34
                if self.exsang[0] > 12:
                    self.exsang[0] = 12
        else:
            pass
            
    def getIncite(self, ability, tick):
        if tick > self.incite[1]:
            self.incite[0] = 0
            self.incite[1] = 0
        else:
            pass
        
        if self.autocast[0] == 'incite':
            for abil in self.utils.abilities:
                if abil['name'] == ability:
                    break
                if abil['style'] == 'MAGIC':
                        self.incite[0] += 1
                        self.incite[1] = tick + 34
                if self.incite[0] > 5:
                    self.incite[0] = 5
        else:
            pass
        
    def setVuln(self, ability, tick):
        if ability == 'vuln':
            self.vuln[0] = 1
            self.vuln[1] = tick + 100
        else:
            self.vuln[0] = False
            self.vuln[1] = 0
            
    def setSC(self, ability, tick):
        if ability == 'smoke cloud':
            self.sc[0] = 1
            self.sc[1] = tick + 200
        else:
            self.sc[0] = False
            self.sc[1] = 0
            
    def setBarge(self, ability, tick, buffer):
        if buffer > 8:
            if ability == 'greater barge':
                self.barge[0] = True
                self.barge[1] = tick + 10
            else:
                pass
        else:
            self.barge[0] = False
            self.barge[1] = 0
    
    def setBleed(self):
        if self.cast.type_n == 'BLEED':
            self.bleed = True
        elif self.cast.type_n == 'CHANNELED' and self.barge[0] == True:
            self.bleed = True
            self.barge[0] = False
        else:
            pass