class CheckDmgBoosts:
    def __init__(self):
        self.pf = False
        self.vestments = False
        self.sun = [False, 0]
        self.meta = [False, 0]
        self.swift = [False, 0]
        self.zerk = [False, 0]
        self.zgs = [False, 0]
    
    def check_boost(self, ability, tick):
        check = False
        end = 0
        if ability == 'greater sunshine' or ability == 'greater death swiftness':
            self.sun[0] = True
            self.sun[1] = tick + 64
        elif ability == 'sunshine' or ability == 'death swiftness':
            self.sun[0] = True
            if self.pf == True:
                self.sun[1] = tick + 64
            else:
                self.sun[1] = tick + 50
        elif ability == 'metamorphosis':
            self.meta[0] = True
            self.meta[1] = tick + 26
        elif ability == 'berserk':
            self.zerk[0] = True
            if self.vestments == True:
                self.zerk[1] = tick + 64
            else:
                self.zerk[1] = tick + 50
        elif ability == 'zgs':
            self.zgs[0] = True
            self.zgs[1] = tick + 26
        else:
            pass

DMG_BOOST_INS = CheckDmgBoosts()
    
