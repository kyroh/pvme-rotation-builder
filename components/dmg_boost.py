from components.inputs import UserInputs

class CheckDmgBoosts:
    def __init__(self, ability, cast_tick, weapon):
        self.inputs = UserInputs(ability, weapon)
        self.ability = ability
        self.cast_tick = cast_tick
        self.pf = False
        self.vestments = False
        self.sunshine = self.check_sunshine()
        self.death_swift = self.check_swift()
        self.zerk = self.check_zerk()
        self.zgs = self.check_zgs()
    
    def check_sunshine(self):
        sun = False
        sun_entries = [entry for entry in self.inputs.rotation if entry['name'] == 'sunshine' and self.cast_tick - 64 < entry['tick']]
        for sun_entry in sun_entries:
            sun_tick = sun_entry['tick']
            if self.pf:
                if sun_tick > self.cast_tick - 64 and sun_tick <= self.cast_tick:
                    sun = True
                    break
            else:
                if sun_tick > self.cast_tick - 50 and sun_tick <= self.cast_tick:
                    sun = True
                    break
            
        if not self.pf:
            gsun_entries = [entry for entry in self.inputs.rotation if entry['name'] == 'greater sunshine' and self.cast_tick - 64 < entry['tick']]
            for gsun_entry in gsun_entries:
                gsun_tick = gsun_entry['tick']
                if gsun_tick > self.cast_tick - 50 and gsun_tick <= self.cast_tick:
                    sun = True
                    break
        
        return sun
    
    def check_swift(self):
        swift = False
        swift_entries = [entry for entry in self.inputs.rotation if entry['name'] == 'death swiftness' and self.cast_tick - 64 < entry['tick']]
        for swift_entry in swift_entries:
            swift_tick = swift_entry['tick']
            if self.pf:
                if swift_tick > self.cast_tick - 64 and swift_tick <= self.cast_tick:
                    swift = True
                    break
            else:
                if swift_tick > self.cast_tick - 50 and swift_tick <= self.cast_tick:
                    swift = True
                    break
            
        if not self.pf:
            gswift_entries = [entry for entry in self.inputs.rotation if entry['name'] == 'greater death swiftness' and self.cast_tick - 64 < entry['tick']]
            for gswift_entry in gswift_entries:
                gswift_tick = gswift_entry['tick']
                if gswift_tick > self.cast_tick - 50 and gswift_tick <= self.cast_tick:
                    swift = True
                    break
        
        return swift
    
    def check_zerk(self):
        zerk = False
        zerk_entries = [entry for entry in self.inputs.rotation if entry['name'] == 'berserk' and self.cast_tick - 44 < entry['tick']]
        for zerk_entry in zerk_entries:
            zerk_tick = zerk_entry['tick']
            if self.vestments:
                if zerk_tick > self.cast_tick - 44 and zerk_tick <= self.cast_tick:
                    zerk = True
                    break
            else:
                if zerk_tick > self.cast_tick - 34 and zerk_tick <= self.cast_tick:
                    zerk = True
                    break
        
        return zerk

    def check_zgs(self):
        zgs = False
        zgs_entries = [entry for entry in self.inputs.rotation if entry['name'] == 'zgs spec' and self.cast_tick - 34 < entry['tick']]
        for zgs_entry in zgs_entries:
            zgs_tick = zgs_entry['tick']
            if zgs_tick > self.cast_tick - 34 and zgs_tick <= self.cast_tick:
                    zgs = True
                    break
        return zgs
        