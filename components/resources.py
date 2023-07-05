import os
import json

class Utils:
    def __init__(self):
        self.abilities = self.load_json('v2/utils', 'abilities.json')
        self.gear = self.load_json('v2/utils', 'gear.json')
        self.weapons = self.load_json('v2/utils', 'weapons.json')
        self.timing = self.load_json('v2/utils', 'timing.json')
        self.boosts = self.load_json('v2/utils', 'boosts.json')
        
    def load_json(self, directory, filename):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            return json.load(file)