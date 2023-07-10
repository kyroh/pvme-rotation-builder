from resources import Utils

class Entry:
    def __init__(self):
        self.utils = Utils()
        self.ability = None
        self.style = None
        self.fixed = None
        self.variable = None
        self.type_n = None
        self.tick = None       

    def get_entry(self, ability, tick):
        for abil in self.utils.abilities:
            if abil['name'] == ability:
                self.ability = abil['name']
                self.style = abil['style']
                self.fixed = abil['fixed']
                self.variable = abil['var']
                self.type_n = abil['type_n']
                self.class_n = abil['class_n']
                self.tick = tick
            else:
                pass

ENTRY_INS = Entry()