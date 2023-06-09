class OnHitBuffs:
    #calcs all on-hit buffs currently known
    #see https://www.overleaf.com/read/vbptcfvfcfkf for explanation
    def __init__(self,damage):
        self.base_damage = damage
        self.style = "Melee" #combat style used
        self.exsang = 2 #0-12 stacks
        self.vuln = 1 #0 or 1
        self.sc = 1 #smoke cloud; 0 if no smoke or no crit, 1 if sc and crit
        self.Xslayer = 1 #0 or 1
        self.slayersigil = 1 #0 or 1

    def damage_calc(self):
        if self.style == "Melee":
            return int( int( int( int(self.base_damage
                    * (1+self.vuln*0.1)) * (1+self.sc *0.06))
                    * (1+(self.Xslayer*0.07))) * (1+(self.slayersigil*0.15)) )
        elif self.style == "Magic":
            return int( int( int( int( int(self.base_damage * (1+self.exsang/100))
                    * (1+self.vuln*0.1)) * (1+self.sc *0.06))
                    * (1+(self.Xslayer*0.07))) * (1+(self.slayersigil*0.15)) )
        elif self.style == "Ranged":
            return int( int( int( int(self.base_damage
                    * (1+self.vuln*0.1)) * (1+self.sc *0.06))
                    * (1+(self.Xslayer*0.07))) * (1+(self.slayersigil*0.15)) )
        elif self.style == "Necromancy":
            return "lole"

damage = 1000
test = OnHitBuffs(damage)
buff = test.damage_calc()
print(buff)
