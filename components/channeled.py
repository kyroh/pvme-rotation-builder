from components.inputs import UserInputs
from components.ability_dmg import AbilityDmg
from components.standard import StandardAbility

class ChanneledAbility:
    def __init__(self, ability, cast_tick):
        self.inputs = UserInputs(ability, cast_tick)
        self.ad = AbilityDmg(ability, cast_tick)
        self.standard = StandardAbility(ability, cast_tick)
        self.cast_tick = cast_tick
    
    def cancel(self):
        if self.inputs.type_n == 'CHANNELED':
            for i, entry in enumerate(self.inputs.rotation):
                if entry['tick'] == self.cast_tick:
                    if i + 1 < len(self.inputs.rotation):
                        return self.inputs.rotation[i + 1]['tick']
                    else:
                        None
        else:
            pass
    
    def hit_count(self):
        cancel_tick = self.cancel()
        abil = None
        for a in self.inputs.quad_channels:
            if a['name'] == self.inputs.ability_input:
                abil = a
                break
            
        hit_tick = abil['hit_tick']
        hit_delay = abil['hit_delay']
        max_hits = abil['max_hits']
        
        if cancel_tick is not None:
            hit_count = min(int((cancel_tick - self.cast_tick - hit_tick) / hit_delay), max_hits)
        else:
            hit_count = 4
        return hit_count

    def hits(self):
        dmg = self.standard.aura_passive()
        fixed = dmg[0]
        var = dmg[1]
        hits = {}
        hit_count = self.hit_count()
        
        if self.inputs.dmg_output == 'MIN':
            hits = fixed * hit_count
        elif self.inputs.dmg_output == 'AVG':
            hits = fixed + int(var / 2) * hit_count
        elif self.inputs.dmg_output == 'MAX':
            hits = fixed + var * hit_count
        
        for i in range(1, hit_count + 1):
            tick = 1 if i == 1 else hits[i - 1] + 2
            hits[i] = tick
        return hits