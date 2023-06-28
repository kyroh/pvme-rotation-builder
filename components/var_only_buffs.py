class varOnlyBoosts:
    def __init__(self,damage):
        self.revenge = 0 #num of stacks
        self.pernix_quiver = 0 #equipped yes/no - check if it works off style
        self.spendthrift = 0 #rank
        self.slayer_helm = 0 #tier 0-5
        self.bane = 0 #yes no - only og bane, not jas bane
        self.type = "ability" #ability or auto
        self.damage = damage


    def calc_var_boost(self):
        if self.slayer_helm > 0:
            slayerHelm = 0.12 + 0.5 * self.slayer_helm
        else:
            pass

        if self.type == "ability":
            bane = 0.25
        elif self.type == "auto":
            bane = 0.4
        else:
            bane = 0
            
        return int(self.damage * (1 + self.revenge 8 0.1 + self.pernix_quiver * 0.04
                             + slayerHelm + bane + self.spendthrift**2/100))
