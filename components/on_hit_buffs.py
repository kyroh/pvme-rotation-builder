from components.inputs import UserInputs
from components.standard import StandardAbility

class OnHitBuffs:
    #calcs all on-hit buffs currently known
    #see https://www.overleaf.com/read/vbptcfvfcfkf for explanation
    def __init__(self, ability, cast_tick, weapon):
        self.inputs = UserInputs(ability, weapon)
        self.standard = StandardAbility(ability, cast_tick, weapon)
        self.cast_tick = cast_tick
        self.hit = self.standard.hits()
        self.base_damage = self.hit["dmg"]
        self.style = self.inputs.style
        self.exsang = 0 #0-12 stacks
        self.vuln = self.vuln_check()
        self.sc = self.sc_check()
        self.Xslayer = 0 #0 or 1
        self.slayersigil = 0 #0 or 1
    
    def vuln_check(self):
        vuln = 0
        vuln_entries = [entry for entry in self.inputs.rotation if entry['name'] == 'vulnerability' and self.cast_tick - 100 < entry['tick']]
    
        for vuln_entry in vuln_entries:
            vuln_tick = vuln_entry['tick']
            if vuln_tick > self.cast_tick - 100 and vuln_tick <= self.cast_tick:
                vuln = 1
            else:
                vuln = 0
        return vuln
    
    def sc_check(self):
        sc = 0
        sc_entries = [entry for entry in self.inputs.rotation if entry['name'] == 'smoke cloud' and self.cast_tick - 200 < entry['tick']]
    
        for sc_entry in sc_entries:
            sc_tick = sc_entry['tick']
            if sc_tick > self.cast_tick - 200 and sc_tick <= self.cast_tick:
                sc = 1
            else:
                sc = 0
        return sc

    def hits(self):
        if self.style == "MELEE":
            dmg = int( int( int( int(self.base_damage
                    * (1+self.vuln*0.1)) * (1+self.sc *0.06))
                    * (1+(self.Xslayer*0.07))) * (1+(self.slayersigil*0.15)) )
        elif self.style == "MAGIC":
            dmg = int( int( int( int( int(self.base_damage * (1+self.exsang/100))
                    * (1+self.vuln*0.1)) * (1+self.sc *0.06))
                    * (1+(self.Xslayer*0.07))) * (1+(self.slayersigil*0.15)) )
        elif self.style == "RANGE":
            dmg = int( int( int( int(self.base_damage
                    * (1+self.vuln*0.1)) * (1+self.sc *0.06))
                    * (1+(self.Xslayer*0.07))) * (1+(self.slayersigil*0.15)) )
        elif self.style == "NECRO":
            return "lole"
        
        return {"tick" : self.standard.hit_tick, "dmg": dmg}
