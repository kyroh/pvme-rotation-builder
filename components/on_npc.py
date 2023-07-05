from game_state import GameState
from on_cast import OnCast

class OnNPC:
    #calcs all on-hit buffs currently known
    #see https://www.overleaf.com/read/vbptcfvfcfkf for explanation
    def __init__(self):
        self.state = GameState()
        self.cast = OnCast()
        self.exsang = self.state.exsang[0]
        self.vuln = self.state.vuln[0]
        self.sc = self.state.sc[0]
        self.Xslayer = 0 #0 or 1
        self.slayersigil = 0 #0 or 1
        self.damage = 0

    def hits(self):
        if self.cast.style == "MELEE":
            self.damage = int( int( int( int(self.cast.damage
                    * (1+self.vuln*0.1)) * (1+self.sc *0.06))
                    * (1+(self.Xslayer*0.07))) * (1+(self.slayersigil*0.15)) )
        elif self.cast.style == "MAGIC":
            self.damage = int( int( int( int( int(self.cast.damage * (1+self.exsang/100))
                    * (1+self.vuln*0.1)) * (1+self.sc *0.15))
                    * (1+(self.Xslayer*0.07))) * (1+(self.slayersigil*0.15)) )
        elif self.cast.style == "RANGE":
            self.damage = int( int( int( int(self.cast.damage
                    * (1+self.vuln*0.1)) * (1+self.sc *0.06))
                    * (1+(self.Xslayer*0.07))) * (1+(self.slayersigil*0.15)) )
        elif self.cast.style == "NECRO":
            return "lole"
    