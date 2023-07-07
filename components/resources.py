import os
import json

class Utils:
    def __init__(self):
        self.abilities = self.load_json('utils', 'abilities.json')
        self.gear = self.load_json('utils', 'gear.json')
        self.weapons = self.load_json('utils', 'weapons.json')
        self.timing = self.load_json('utils', 'timing.json')
        self.boosts = self.load_json('utils', 'boosts.json')
        self.buffs = self.load_json('utils', 'buffs.json')
        
    def load_json(self, directory, filename):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            return json.load(file)