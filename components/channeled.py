from components.inputs import UserInputs
from components.ability_dmg import AbilityDmg
from components.standard import StandardAbility

class ChanneledAbility:
    def __init__(self, ability, cast_tick, weapon):
        self.inputs = UserInputs(ability, cast_tick, weapon)
        self.ad = AbilityDmg(ability, cast_tick, weapon)
        self.standard = StandardAbility(ability, cast_tick, weapon)
        self.cast_tick = cast_tick
        
        if self.inputs.type == 'dw':
            for i in self.inputs.timing:
                if i['name'] == self.inputs.ability_input:
                    self.hit_tick = i['dw tick']
        elif self.inputs.type == '2h':
            for i in self.inputs.timing:
                if i['name'] == self.inputs.ability_input:
                    self.hit_tick = i['2h tick']
        elif self.inputs.type == 'ms':
            for i in self.inputs.timing:
                if i['name'] == self.inputs.ability_input:
                    self.hit_tick = i['dw tick']
        else:
            pass
        
        for a in self.inputs.channels:
            if a['name'] == self.inputs.ability_input:
                abil = a
                break
        self.coefficient = abil['timing_coe']
        self.frequency = abil['frequency']
        self.max_hits = abil['max_hits']
        if abil['bleed'] == 1:
            self.bleedable = True
        else:
            self.bleedable = False
    
    # figures out if an abil was canceled and returns the tick it was canceled
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
    
    # figures out bled channels
    def barge_check(self):
        bleed = True
        check = None
        barge_entries = [entry for entry in self.inputs.rotation if entry['name'] == 'greater barge' and self.cast_tick - 10 < entry['tick']]
        if barge_entries != []:
            for barge_entry in barge_entries:
                barge_tick = barge_entry['tick']
                if barge_tick > self.cast_tick - 10 and barge_tick <= self.cast_tick:
                    for abil in self.inputs.rotation:
                        if abil['tick'] > barge_tick and abil['tick'] < self.cast_tick:
                            check = abil['name']
                        else:
                            pass
                    if check != None:
                        for channel in self.inputs.channels:
                            if check == channel['name'] and channel['bleed'] == 1:
                                bleed = False
                                break
                    else:
                        bleed = True
                else:
                    bleed = False
        else:
            bleed = False
        return bleed
                        

    # figures out how many times a channeled abil hits factoring in cancelations and bleeding
    def hit_count(self):
        cancel_tick = self.cancel()
        bleed = self.barge_check()
        if cancel_tick is not None:
            if bleed == True:
                hit_count = self.max_hits
            else:
                hit_count = min(int((cancel_tick - self.cast_tick + self.coefficient) / self.frequency), self.max_hits)
        else:
            hit_count = self.max_hits
        return hit_count
    
    # returns a dict of the hits for the channeled ability and the tick they land on
    def hits(self):
        dmg = self.standard.aura_passive()
        fixed = dmg[0]
        var = dmg[1]
        hits = {}
        hit_count = self.hit_count()
        tick = self.cast_tick + self.hit_tick

        if self.inputs.dmg_output == 'MIN':
            for n in range(1, hit_count + 1):
                hits[f'tick {tick}'] = fixed
                tick += self.frequency
        elif self.inputs.dmg_output == 'AVG':
            for n in range(1, hit_count + 1):
                hits[f'tick {tick}'] = fixed + int(var / 2)
                tick += self.frequency
        elif self.inputs.dmg_output == 'MAX':
            for n in range(1, hit_count + 1):
                hits[f'tick {tick}'] = fixed + var
                tick += self.frequency

        return hits