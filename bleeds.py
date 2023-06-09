from inputs import UserInputs
import standard as StandardAbility
import random

inputs = UserInputs()

class BleedAbility:
    # Conmputes fixed dmg without prayer because bleeds are great
    def fixed(self):
        fixed = int(self.standard.ability_dmg * inputs.fixed_dmg)
        return fixed
    
    # Computes var dmg without prayer because bleeds make sense
    def var(self):
        var = int(self.standard.ability_dmg * inputs.var_dmg)
        return var
    
    # Simulates the abil n times and returns the average
    def avg_dmg(self):
        fixed = self.fixed()
        var = self.var()
        max_dmg = fixed + var
        avg_dmg = 0
        total = 0
        
        if inputs.name == 'combust' or inputs.name == 'fragmentation shot' or inputs.name == 'dismember' or inputs.name == 'slaughter':
            for _ in range(self.standard.sim):
                random_num = random.randint(1,100)
                dmg = int((self.standard.ability_dmg * max(((random_num * (1.88 + 0.2 * inputs.lunging_rank)) / 100), 1)) / 5)
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
        hits = []
        
        for bleed in inputs.bleeds:
            if bleed['name'] == inputs.name:
                abil = bleed
                break
        hit_count = abil['hits']
        dmg_decay = abil['dmg_decay']
        
        if dmg_decay == 0:
            if inputs.dmg_output == 'MIN':
                hits = [fixed] * hit_count
            elif inputs.dmg_output == 'AVG':
                hits = [avg_dmg] * hit_count
            elif inputs.dmg_output == 'MAX':
                hits = [max_dmg] * hit_count
            else:
                pass
        else:
            if inputs.name == 'corruption shot' or inputs.name == 'corruption blast':
                if inputs.dmg_output == 'MIN':
                    last_hit = int(self.standard.ability_dmg * 0.067)
                    for i in range(1, hit_count + 1):
                        hits.append(last_hit * i)
                elif inputs.dmg_output == 'AVG':
                    last_hit_min = int(self.standard.ability_dmg * 0.067)
                    last_hit_max = int(self.standard.ability_dmg * 0.067 * 3)
                    last_hit = int((last_hit_min + last_hit_max) / 2)
                    for i in range(1, hit_count + 1):
                        hits.append(last_hit * i)
                elif inputs.dmg_output == 'MAX':
                    last_hit = int(self.standard.ability_dmg * 0.067 * 3)
                    for i in range(1, hit_count + 1):
                        hits.append(last_hit * i)
                else:
                    pass
            elif inputs.name == 'blood tendrils':
                if inputs.dmg_output == 'MIN':
                    small_hit = int(36 / 20 * fixed)
                    large_hit = small_hit * 2
                    hits = [large_hit] + [small_hit] * (hit_count - 1)
                elif inputs.dmg_output == 'AVG':
                    small_hit = int((int((36 / 20 * fixed) + (36 / 20 * var)) + int(36 / 20 * fixed)) / 2)
                    large_hit = small_hit * 2
                    hits = [large_hit] + [small_hit] * (hit_count - 1)
                elif inputs.dmg_output == 'MAX':
                    small_hit = int((36 / 20 * fixed) + (36 / 20 * var))
                    large_hit = small_hit * 2
                    hits = [large_hit] + [small_hit] * (hit_count - 1)
            else:
                pass
        return hits

    
    def walk(self):
        walk = False
        hits = self.hits()

        for bleed in self.bleeds:
            if bleed['name'] == inputs.name:
                abil = bleed
                break
        multiplier = abil['walk']  

        if walk == True:
            hits = [entry * multiplier for entry in hits]
        else:
            pass
        return hits