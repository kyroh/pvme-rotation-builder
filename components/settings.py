from resources import Utils

class Settings:
    def __init__(self):
        #general
        self.utils = Utils()
        self.dmg_mode = 'MIN'
        self.starting_adren = 100
        self.starting_tick = 0
        self.strength_cape = False
        self.nope = False
        self.no_fear = False
        self.preset = '2h'
        
        #levels
        self.magic_lvl = 99
        self.range_lvl = 99
        self.str_lvl = 99
        self.necro_lvl = 99
        
        #constants
        self.aura = None
        self.potion = None
        self.reaper_crew = True
        self.relic_1 = None
        self.relic_2 = None
        self.relic_3 = None
        
        #armour
        self.helm = None
        
        self.body = {
            'name': None,
            'gizmo 1': {
                'slot 1':{
                    'perk': None,
                    'rank': 0
                },
                'slot 2': {
                    'perk': None,
                    'rank': 0
                }
            },
            'gizmo 2': {
                'slot 1':{
                    'perk': None,
                    'rank': 0
                },
                'slot 2': {
                    'perk': None,
                    'rank': 0
                }
            }
        }
            
        self.legs = {
            'name': None,
            'gizmo 1': {
                'slot 1':{
                    'perk': None,
                    'rank': 0
                },
                'slot 2': {
                    'perk': None,
                    'rank': 0
                }
            },
            'gizmo 2': {
                'slot 1':{
                    'perk': None,
                    'rank': 0
                },
                'slot 2': {
                    'perk': None,
                    'rank': 0
                }
            }
        }
        
        self.boots = None
        self.gloves = None
        self.neck = None
        self.cape = None
        self.ring = None
        self.pocket = None
        
        #weapons
        self.mh = {
            'name': 'Wand of the praesul',
            'gizmo 1': {
                'slot 1':{
                    'perk': 'precise',
                    'rank': 0
                },
                'slot 2': {
                    'perk': None,
                    'rank': 0
                }
            }
        }
        
        self.oh = {
            'name': 'Imperium core',
            'gizmo 1': {
                'slot 1':{
                    'perk': None,
                    'rank': 0
                },
                'slot 2': {
                    'perk': None,
                    'rank': 0
                }
            },
        }
        
        self.th = {
            'name': 'Staff of Sliske',
            'gizmo 1': {
                'slot 1':{
                    'perk': None,
                    'rank': 0
                },
                'slot 2': {
                    'perk': None,
                    'rank': 0
                }
            },
            'gizmo 2': {
                'slot 1':{
                    'perk': None,
                    'rank': 0
                },
                'slot 2': {
                    'perk': None,
                    'rank': 0
                }
            }
        }
        
        self.sh = None
        self.prayer = None
        self.auto_cast = 99
        self.ammo = 99
        
        self.perks = {
            'precise': 0,
            'equilibrium': 0,
            'biting': 0,
            'lunging': 0,
            'invig': 0,
            'turtling': 0
        }
        
        self.style = None
        
    def weapon_switch(self, preset):
        index = preset
        self.mh = index[0]
        self.oh = index[1]
        self.th = index[2]
        self.sh = index[3]
        self.preset = index[4]
        
    def get_perks(self):
        presets = {
            'dw': [self.mh, self.oh],
            '2h': [self.th],
            'ms': [self.th]
        }
        
        for gizmo in presets.get(self.preset, []) + [self.body, self.legs]:
            for gizmo_key in ['gizmo 1', 'gizmo 2']:
                if gizmo_key in gizmo:
                    for slot_key in ['slot 1', 'slot 2']:
                        if 'perk' in gizmo[gizmo_key].get(slot_key, {}):
                            perk = gizmo[gizmo_key][slot_key]['perk']
                            if perk in self.perks:
                                rank = gizmo[gizmo_key][slot_key]['rank']
                                self.perks[perk] = max(self.perks[perk], rank)
                                
    def get_weapon_style(self):
        if self.preset == 'dw' or self.preset == 'ms':
            for weapon in self.utils.weapons:
                if weapon == self.mh:
                    self.style = weapon['style']
        if self.preset == '2h':
            for weapon in self.utils.weapons:
                if weapon == self.th:
                    self.style = weapon['style']
                                
                                
SET_INS = Settings()



