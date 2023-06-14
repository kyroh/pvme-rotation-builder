from components.inputs import UserInputs
from components.standard import StandardAbility
from components.ability_dmg import AbilityDmg
import random


class BleedAbility:
    def __init__(self, ability, cast_tick):
        self.inputs = UserInputs(ability)
        self.standard = StandardAbility(ability, cast_tick)
        self.ad = AbilityDmg(ability, cast_tick)
        self.cast_tick = cast_tick
        
    # Conmputes fixed dmg without prayer because bleeds are great
    def fixed(self):
        fixed = int(self.ad.ability_dmg * self.inputs.fixed_dmg)
        return fixed
    
    # Computes var dmg without prayer because bleeds make sense
    def var(self):
        var = int(self.ad.ability_dmg * self.inputs.var_dmg)
        return var
    
    # Simulates the abil n times and returns the average
    def avg_dmg(self):
        fixed = self.fixed()
        var = self.var()
        max_dmg = fixed + var
        avg_dmg = 0
        total = 0
        
        if self.inputs.name == 'combust' or self.inputs.name == 'fragmentation shot' or self.inputs.name == 'dismember' or self.inputs.name == 'slaughter':
            for _ in range(self.standard.sim):
                random_num = random.randint(1,100)
                dmg = int((self.ad.ability_dmg * max(((random_num * (1.88 + 0.2 * self.inputs.lunging_rank)) / 100), 1)) / 5)
                total += dmg
                avg_dmg = int(total / self.standard.sim)
        else:
            for _ in range(self.standard.sim):
                random_num = random.randint(fixed, max_dmg)
                total += random_num
            avg_dmg = int(total / self.standard.sim)
        return avg_dmg
    
    def hits(self):
        avg_dmg = self.avg_dmg()
        var = self.var()
        fixed = self.fixed()
        max_dmg = fixed + var
        hits = {}
        
        for bleed in self.inputs.bleeds:
            if bleed['name'] == self.inputs.name:
                abil = bleed
                break
        hit_count = abil['hits']
        dot = abil['dot']
        hit_delay = abil['frequency']
        tick = self.cast_tick + hit_delay
        
        if dot == 0:
            if self.inputs.dmg_output == 'MIN':
                for n in range(1, hit_count + 1):
                    hits[f'tick {tick}'] = fixed
                    tick += hit_delay
            elif self.inputs.dmg_output == 'AVG':
                for n in range(1, hit_count + 1):
                    hits[f'tick {tick}'] = avg_dmg
                    tick += hit_delay
            elif self.inputs.dmg_output == 'MAX':
                for n in range(1, hit_count + 1):
                    hits[f'tick {tick}'] = max_dmg
                    tick += hit_delay
            else:
                pass
        else:
            if self.inputs.name == 'corruption shot' or self.inputs.name == 'corruption blast':
                if self.inputs.dmg_output == 'MIN':
                    last_hit = int(self.ad.ability_dmg * 0.067)
                    for i in range(hit_count, 0, -1):
                        hits[f'tick {tick}'] = last_hit * i
                        tick += hit_delay
                elif self.inputs.dmg_output == 'AVG':
                    last_hit_min = int(self.ad.ability_dmg * 0.067)
                    last_hit_max = int(self.ad.ability_dmg * 0.067 * 3)
                    last_hit = int((last_hit_min + last_hit_max) / 2)
                    for i in range(hit_count, 0, -1):
                        hits[f'tick {tick}'] = last_hit * i
                        tick += hit_delay
                elif self.inputs.dmg_output == 'MAX':
                    last_hit = int(self.ad.ability_dmg * 0.067 * 3)
                    for i in range(hit_count, 0, -1):
                        hits[f'tick {tick}'] = last_hit * i
                        tick += hit_delay
                else:
                    pass
            elif self.inputs.name == 'blood tendrils':
                if self.inputs.dmg_output == 'MIN':
                    small_hit = int(36 / 20 * fixed)
                    large_hit = small_hit * 2
                    for i in range(hit_count, 0, -1):
                        hits[f'tick {tick}'] = large_hit if i == hit_count else small_hit
                        tick += hit_delay
                elif self.inputs.dmg_output == 'AVG':
                    small_hit = int((int((36 / 20 * fixed) + (36 / 20 * var)) + int(36 / 20 * fixed)) / 2)
                    large_hit = small_hit * 2
                    for i in range(hit_count, 0, -1):
                        hits[f'tick {tick}'] = large_hit if i == hit_count else small_hit
                        tick += hit_delay
                elif self.inputs.dmg_output == 'MAX':
                    small_hit = int((36 / 20 * fixed) + (36 / 20 * var))
                    large_hit = small_hit * 2
                    for i in range(hit_count, 0, -1):
                        hits[f'tick {tick}'] = large_hit if i == hit_count else small_hit
                        tick += hit_delay
            else:
                pass
        return hits

    
    def walk(self):
        walk = False
        hits = self.hits()

        for bleed in self.bleeds:
            if bleed['name'] == self.inputs.name:
                abil = bleed
                break
        multiplier = abil['walk']  

        if walk == True:
            hits = [entry * multiplier for entry in hits]
        else:
            pass
        return hits