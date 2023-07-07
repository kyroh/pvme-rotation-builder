from ability_dmg import AD_INS
from on_cast import CAST_INS
from settings import SET_INS
from duration_effects import EFF_INS

AD_INS.calculate_levels()
AD_INS.compute_bonus()
ad = AD_INS.base_ability_dmg()

CAST_INS.get_abil('wrack', 0)
CAST_INS.fixedDmg()
CAST_INS.varDmg()
CAST_INS.prayer_dmg()
CAST_INS.dpl()

print(CAST_INS.fixed)