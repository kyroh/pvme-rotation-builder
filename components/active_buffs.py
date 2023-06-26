#
# Author - kyroh
# 
# June 2023
#

from components.inputs import UserInputs
from components.channeled import ChanneledAbility

class ActiveBuffs:
    def __init__(self, ability, cast_tick, weapon):
        self.inputs = UserInputs(ability, cast_tick, weapon)
        self.ability = ability
        self.cast_tick = cast_tick
        
    def exsang(self):
        stacks = 0
        last_tick = 0
        for entry in self.inputs.rotation:
            ability = entry['name']
            cast_tick = entry['tick']
            weapon = entry['type']
            inputs = UserInputs(ability, cast_tick, weapon)
            auto_cast = inputs.get_autocast()
            params = inputs.get_abil_params()
            style = params[3]
            type_n = params[4]
                
            if stacks == 12 and ability == 'wrack':
                stacks = 0
                continue
            
            if style == 'MAGIC':
                if auto_cast == 'exsanguinate':
                    if type_n == 'SINGLE_HIT_ABIL' or type_n == 'BLEED':
                        stacks += 1
                    elif type_n == 'AUTO_CAST':
                        pass                    
                    elif stacks > 12:
                        stacks = 12
                    last_tick = cast_tick
                else:
                    if type_n == 'CHANNELED':
                        chaneled = ChanneledAbility(ability, cast_tick, weapon)
                        hits = chaneled.hits()
                        for hit in hits:
                            chan_inputs = UserInputs(ability, hit, weapon)
                            chan_auto_cast = chan_inputs.get_autocast()
                            print(chan_auto_cast)
                            if chan_auto_cast == 'exsanguinate':
                                stacks += 1
                    consecutive_ticks = cast_tick - last_tick
                    if consecutive_ticks >= 34:
                        stacks = 0
            
            if ability == self.ability and cast_tick == self.cast_tick:
                break
                
        return stacks
            
    
    def incite(self):
        stacks = 0
        for entry in self.inputs.rotation:
            ability = entry['name']
            cast_tick = entry['tick']
            weapon = entry['type']
            inputs = UserInputs(ability, cast_tick, weapon)
            auto_cast = inputs.get_autocast()
            params = inputs.get_abil_params()
            style = params[3]
            type_n = params[4]
            
            if 'cast' not in entry['name']:
                if style == 'MAGIC' and auto_cast == 'incite_fear':
                    last_tick = cast_tick
                    stacks += 1
                    if stacks > 5:
                        stacks = 5
                else:
                    consecutive_ticks = cast_tick - last_tick
                    if consecutive_ticks >= 34:
                        stacks = 0
            
            if ability == self.ability and cast_tick == self.cast_tick:
                break
                
        return stacks
    
    def gconc(self):
        pass
    
    def channelers(self):
        pass
    
    def ruby_aurora(self):
        pass
    
    