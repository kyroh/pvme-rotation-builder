import inputs as Inputs
import standard as StandardAbility

class ChanneledAbility:
    def __init__(self):
        self.inputs = Inputs()
        self.standard = StandardAbility()
        self.count = self.hit_count()

    def hit_count(self):
        hit_count = 4
        hit_dict = []

        for entry in self.rotation:
            if entry['name'] == self.inputs.name:
                cast_tick = entry['tick']
                abil = next((channel for channel in self.channels if channel['name'] == self.inputs.name), None)
                if abil is not None:
                    for i in range(1, 5):
                        hit_dict.append(abil[f'hit {i}'] + cast_tick)
                break
        
        remaining_hits = []
        for hit in hit_dict:
            cancel = False
            for entry in self.rotation:
                if entry['tick'] < hit and entry['tick'] > cast_tick and entry['name'] != '-':
                    cancel = True
                    break
            if not cancel:
                remaining_hits.append(hit)

        hit_count = len(remaining_hits)
        return hit_count


    def hits(self):
        dmg = self.standard.aura_passive()
        fixed = dmg[0]
        var = dmg[1]
        hits = []

        if self.inputs.dmg_output == 'MIN':
            hits = [fixed] * self.count
        elif self.inputs.dmg_output == 'AVG':
            hits = [fixed + int(var / 2)] * self.count
        elif self.inputs.dmg_output == 'MAX':
            hits = [fixed + var] * self.count
        return hits