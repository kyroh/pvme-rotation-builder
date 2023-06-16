from inputs import UserInputs
from standard import StandardAbility

class OnHitBuffs:
    #calcs all on-hit buffs currently known
    #see https://www.overleaf.com/read/vbptcfvfcfkf for explanation
    def __init__(self,ability,cast_tick):
        self.inputs = UserInputs(ability, cast_tick)
        self.standard = StandardAbility(ability, cast_tick)
        self.cast_tick = cast_tick
        self.base_damage = self.standard.hits()
        self.style = self.inputs.style
        self.exsang = 2 #0-12 stacks
        for entry in self.inputs.rotation:
            if entry['name'] == 'vulnerability' and entry['tick'] >= cast_tick - 99:
                self.vuln = 1
            else:
                self.vuln = 0
        for entry in self.inputs.rotation:
            if entry['name'] == 'smoke cloud' and entry['tick'] >= cast_tick - 200:
                self.sc = 1
            else:
                self.sc = 0
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
