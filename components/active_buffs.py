#
# Author - kyroh
# 
# June 2023
#

from components.inputs import UserInputs
from components.channeled import ChanneledAbility
from components.bleeds import BleedAbility

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
            
            if style == 'MAGIC':
                if auto_cast == 'incite_fear':
                    if type_n == 'SINGLE_HIT_ABIL' or type_n == 'BLEED':
                        stacks += 1
                    elif type_n == 'AUTO_CAST':
                        pass                    
                    elif stacks > 5:
                        stacks = 5
                    last_tick = cast_tick
                else:
                    if type_n == 'CHANNELED':
                        chaneled = ChanneledAbility(ability, cast_tick, weapon)
                        hits = chaneled.hits()
                        for hit in hits:
                            chan_inputs = UserInputs(ability, hit, weapon)
                            chan_auto_cast = chan_inputs.get_autocast()
                            if chan_auto_cast == 'incite_fear':
                                stacks += 1
                    consecutive_ticks = cast_tick - last_tick
                    if consecutive_ticks >= 34:
                        stacks = 0
            
            if ability == self.ability and cast_tick == self.cast_tick:
                break
                
        return stacks
    
    def conc(self):
        stacks = 0
        for entry in self.inputs.rotation:
            if entry['name'] == self.ability and entry['tick'] == self.cast_tick:
                index = self.inputs.rotation.index(entry) - 1
                channeled = self.inputs.rotation[index]
                
                if channeled['name'] == 'greater concentrated blast' or  channeled['name'] == 'concentrated blast':
                    chan = ChanneledAbility(channeled['name'], channeled['tick'], channeled['type'])
                    stacks = chan.hit_count()
                else:
                    pass
        return stacks
    
    def channelers(self):
        pass
    
    def ruby_aurora(self):
        stacks = 0
        expiration = []
        
        for entry in self.inputs.rotation:
            for tick in expiration:
                if entry['tick'] > tick:
                    stacks -= 1
                    
            if entry['name'] == 'ruby aurora':
                stacks += 1
                expiration += [entry['tick'] + 40]
            else:
                pass
            
            if stacks > 3:
                stacks = 3
            
            if entry['tick'] == self.cast_tick:
                break
                
        return stacks
    
    def scourge(self):
        stacks = 0
        last_tick = 0
        for entry in self.inputs.rotation:
            ability = entry['name']
            cast_tick = entry['tick']
            weapon = entry['type']
            inputs = UserInputs(ability, cast_tick, weapon)
            params = inputs.get_abil_params()
            style = params[3]
            type_n = params[4]
            ChanneledAbility
            
            if style == 'MELEE':
                if weapon == 'dw' or weapon == 'ms':
                    if self.inputs.mh_input == 'Abyssal scourge':
                        if type_n == 'SINGLE_HIT_ABIL':
                            stacks += 1
                        elif type_n == 'BLEED':                    
                            bleed = BleedAbility(ability, cast_tick, weapon)
                            hit_count = bleed.hit_count()
                            stacks += hit_count
                        elif stacks > 50:
                            stacks = 50
                        elif type_n == 'CHANNELED':
                            chaneled = ChanneledAbility(ability, cast_tick, weapon)
                            hits = chaneled.hits()
                            for hit in hits:
                                chan_inputs = UserInputs(ability, hit, weapon)
                                chan_weapon = chan_inputs.mh_input
                                if chan_weapon == 'Abyssal scourge':
                                    stacks += 1
                        last_tick = cast_tick
                        
                        consecutive_ticks = cast_tick - last_tick
                        if consecutive_ticks > 11:
                            stacks = 0
            if ability == self.ability and cast_tick == self.cast_tick:
                break
                
        return stacks
    
    