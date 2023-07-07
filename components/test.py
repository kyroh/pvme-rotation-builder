from ability_dmg import AD_INS
from on_cast import CAST_INS
from dmg_boost import DMG_BOOST_INS
from settings import SET_INS
from duration_effects import EFF_INS

AD_INS.calculate_levels()
AD_INS.compute_bonus()
ad = AD_INS.base_ability_dmg()

CAST_INS.get_abil('sunshine', 0)
DMG_BOOST_INS.check_boost(CAST_INS.ability, CAST_INS.tick)



print(DMG_BOOST_INS.sun)