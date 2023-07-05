class CheckDmgBoosts:
    def __init__(self):
        self.pf = False
        self.vestments = False
    
    def check_boost(self, ability, tick):
        check = False
        end = 0
        if ability == 'greater sunshine' or ability == 'greater death swiftness':
            check = True
            end = tick + 64
        elif ability == 'sunshine' or ability == 'death swiftness':
            check = True
            if self.pf == True:
                end = tick + 64
            else:
                end = tick + 50
        elif ability == 'metamorphosis':
            check = True
            end = tick + 26
        elif ability == 'berserk':
            check = True
            if self.vestments == True:
                end = tick + 64
            else:
                end = tick + 50
        elif ability == 'zgs':
            check = True
            end = tick + 26
        else:
            pass
        return [check, end]