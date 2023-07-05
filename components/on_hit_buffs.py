
class OnHitBuffs:
    #calcs all on-hit buffs currently known
    #see https://www.overleaf.com/read/vbptcfvfcfkf for explanation
    def __init__(self, ability, tick, weapon):
        self.tick = tick
        self.base_damage = 1000
        self.style = 'MAGIC'
        self.exsang = 0
        self.vuln = 0
        self.sc = 0
        self.Xslayer = 0 #0 or 1
        self.slayersigil = 0 #0 or 1

    def hits(self):
        if self.style == "MELEE":
            dmg = int( int( int( int(self.base_damage
                    * (1+self.vuln*0.1)) * (1+self.sc *0.06))
                    * (1+(self.Xslayer*0.07))) * (1+(self.slayersigil*0.15)) )
        elif self.style == "MAGIC":
            dmg = int( int( int( int( int(self.base_damage * (1+self.exsang/100))
                    * (1+self.vuln*0.1)) * (1+self.sc *0.15))
                    * (1+(self.Xslayer*0.07))) * (1+(self.slayersigil*0.15)) )
        elif self.style == "RANGE":
            dmg = int( int( int( int(self.base_damage
                    * (1+self.vuln*0.1)) * (1+self.sc *0.06))
                    * (1+(self.Xslayer*0.07))) * (1+(self.slayersigil*0.15)) )
        elif self.style == "NECRO":
            return "lole"
        
        return {"tick" : self.standard.hit_tick, "dmg": dmg}
