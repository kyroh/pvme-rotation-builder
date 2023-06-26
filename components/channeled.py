#
# Author - kyroh
# 
# June 2023
#

from components.inputs import UserInputs
from components.ability_dmg import AbilityDmg
from components.standard import StandardAbility

class ChanneledAbility:
    def __init__(self, ability, cast_tick, weapon):
        self.inputs = UserInputs(ability, cast_tick, weapon)
        self.ad = AbilityDmg(ability, cast_tick, weapon)
        self.standard = StandardAbility(ability, cast_tick, weapon)
        self.cast_tick = cast_tick
        self.ability = ability
        
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
        cancel_tick = None
        if self.inputs.type_n == 'CHANNELED':
            last_tick = self.max_hits * self.frequency - self.coefficient
            for entry in self.inputs.rotation:
                if self.cast_tick <= entry['tick'] <= last_tick and entry['name'] != self.ability:
                    entry_name = entry['name']
                    for abil in self.inputs.abilities:
                        if entry_name == abil['name']:
                            type_n = abil['type_n']
                            if type_n != 'AUTO_CAST' or type_n != 'POTION':
                                cancel_tick = entry['tick']
                            else:
                                pass
        return cancel_tick

    
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
        hit_count = self.hit_count()
        init_tick = self.cast_tick + self.hit_tick
        hits = [init_tick + i * self.frequency for i in range(hit_count)]
        return hits






        
        