#
# Author - kyroh
# 
# June 2023
#

from components.inputs import UserInputs
from components.standard import StandardAbility
from components.ability_dmg import AbilityDmg
import random


class BleedAbility:
    def __init__(self, ability, cast_tick, weapon):
        self.inputs = UserInputs(ability, cast_tick, weapon)
        self.standard = StandardAbility(ability, cast_tick)
        self.ad = AbilityDmg(ability, weapon)
        self.cast_tick = cast_tick
        self.weapon = weapon
        self.ability = ability
    
    # Simulates the abil n times and returns the average with adjustment for the weirdo bleeds
    def avg_dmg(self):
        dmg = self.standard.aura_passive()
        fixed = dmg[0]
        var = dmg[1]
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
    
    def hit_count(self):
        for bleed in self.inputs.bleeds:
            if bleed['name'] == self.inputs.name:
                abil = bleed
                break
            
            if self.inputs.style == 'MELEE' and self.inputs.th_input == 'masterwork spear' and self.weapon == '2h':
                hit_count = int(abil['hit_count'] * 1.5)
            elif self.inputs.style == 'MAGIC' and self.ability == 'wrack and ruin':
                hit_count = abil['hit_count']
            else:
                hit_count = abil['hit_count']
        return hit_count
    
    # Outputs a dict of hits and tick they land for bleed abilities
    def hits(self):
        dmg = self.standard.aura_passive()
        fixed = dmg[0]
        var = dmg[1]
        avg_dmg = self.avg_dmg()
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
    
    # Walk multiplier for certain bleeds needs to be finished still
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