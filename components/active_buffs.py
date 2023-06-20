from components.inputs import UserInputs
from components.channeled import ChanneledAbility

class ActiveBuffs:
    def __init__(self, ability, cast_tick, weapon):
        self.inputs = UserInputs(ability, weapon)
        self.cast_tick = cast_tick
        
    def exsang(self):
        auto_cast = False
        stacks = 0
        for entry in self.inputs.rotation:
            ability = entry['name']
            cast_tick = entry['tick']
            weapon = entry['type']
            if cast_tick >= self.cast_tick:
                continue

            if ability == 'exsang':
                auto_cast = True
                continue  

            if not auto_cast:
                continue
            
            if stacks == 12 and ability == 'wrack':
                stacks = 0
                continue
            
            for entry in self.inputs.abilities:
                if entry['name'] == ability and entry['style'] == 'MAGIC':
                    type_n = entry['type_n']
                    break
            else:
                continue
            
            if type_n != 'CHANNELED':
                stacks += 1
            elif type_n == 'CHANNELED':
                channeled = ChanneledAbility(ability, cast_tick, weapon)
                hit_count = channeled.hit_count()
                stacks += hit_count
            else:
                pass
        return stacks

    
    def incite(self):
        pass
    
    def gconc(self):
        pass
    
    def channelers(self):
        pass
    
    def ruby_aurora(self):
        pass
    
    