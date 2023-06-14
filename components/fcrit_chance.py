from components.inputs import UserInputs

class fcrit:
    def __init__(self, ability):
        self.inputs = UserInputs(ability)
        if self.inputs.pocket == 'Grimoire':
            self.grim = 1
        else:
            self.grim = 0
        self.inputs.biting_rank = 3 #biting level of the player
        self.biting_20 = 1 # 1 if level 20 armour
        self.kalg = 1 #1 if player uses a kalg familiar
        self.critikal = 1 #1 if kalg scroll is active
        self.corbicula = 1 #number of pens with elder corbiculas
        self.abil = ability
        self.warpriest = 0 #number of pieces
        self.fury = 2 # number of fury/conc hits, 2 for gfury
        self.gfury =  0 #1 if guaranteed crit
        self.reaver = 1 # 0 or 1
        self.channelers = 0 # 0 or 1
        self.channels = 0 #number hit it is in the channel
        self.champions = 0 # 0, 1 or 2
        self.bleeds = 0 #number of bleeds on the boss (for champ ring)
        self.stalkers = 0 # 0, 1 or 2
        self.bow = 1 #check if a bow is equipped for stalker's ring
        self.deathspore = 0 #1 if deathspore arrows are equipped


    def calc_fcrit(self):
        if self.gfury == 1:
            return 1.00

        fcrit_chance = 0
        if self.warpriest > 0:
            fcrit_chance += self.warpriest
        else:
            fcrit_chance += (self.inputs.biting_rank * 0.02) * (1+self.biting_20 * 0.1)

        fcrit_chance = (fcrit_chance + self.kalg * 0.05 + self.critikal * 0.01
                        + self.reaver * 0.05 + self.grim * 0.12)

        if self.inputs.style == 'Melee':
            fcrit_chance += self.fury * 0.05
            if self.champions == 1:
                fcrit_chance += 0.03
            elif self.champions == 2:
                fcrit_chance += 0.03 + 0.01 * self.bleeds
            if self.abil == 'Meteor Strike':
                fcrit_chance += self.corbicula * 0.2

        elif self.inputs.style == 'Magic':
            fcrit_chance += self.fury * 0.05 + self.channelers * self.channels * 0.04

        elif self.inputs.style == 'Ranged':
            fcrit_chance += self.deathspore * 0.03
            if self.stalkers == 1:
                fcrit_chance += 0.03
            elif self.stalkers == 2:
                fcrit_chance += 0.03 + 0.01 * self.bow

        elif self.style == 'Necromancy': #placeholder
            return "you're lying this skill isn't out yet"

        return round(fcrit_chance,3)
