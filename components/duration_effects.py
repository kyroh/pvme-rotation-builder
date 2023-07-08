from resources import Utils
from get_entry import ENTRY_INS
from settings import SET_INS

class Effects:
    def __init__(self):
        self.utils = Utils()
        self.vuln = [False,0]
        self.sc = [False,0]
        self.natty = [False,0]
        self.fsoa = [False,0]
        self.bolg = [False,0]
        self.ecb = [False,0]
        self.nami = [False,0]
        self.meteor = [False,0]
        self.incend = [False,0]
        self.stun = [False,0]
        self.bind = [False,0]
        self.dba = [False,0]
        self.blood_ess = [False, 0, None]
        
    def setEffect(self, check):
        for entry in self.utils.buffs:
            if check == entry['name']:
                duration = entry['duration']
        
        if ENTRY_INS.ability == check:
            setattr(self, check, [True, duration + ENTRY_INS.tick])
        else:
            setattr(self, check, [False, 0])
    
    def set_blood_ess(self):
        if ENTRY_INS.ability == 'blood essence':
            self.blood_ess[0] = True
            self.blood_ess[1] = ENTRY_INS.tick + 34
            self.blood_ess[2] = SET_INS.style

EFF_INS = Effects()