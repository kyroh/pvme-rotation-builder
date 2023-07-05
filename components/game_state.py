from resources import Utils
from on_cast import OnCast

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
        self.channel = False
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
    
    def getAutoCast(self, ability):
            self.autocast = ability.split(' ')[1]
        
    def getExsang(self, ability, tick):
        if tick > self.exsang[1]:
            self.exsang[0] = 0
            self.exsang[1] = 0
        else:
            pass
        
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
        
    def getVuln(self, ability, tick):
        if ability == 'vuln':
            self.vuln[0] = 1
            self.vuln[1] = tick + 100
        else:
            self.vuln[0] = False
            self.vuln[1] = 0
            
    def getSC(self, ability, tick):
        if ability == 'smoke cloud':
            self.sc[0] = 1
            self.sc[1] = tick + 200
        else:
            self.sc[0] = False
            self.sc[1] = 0


    
    