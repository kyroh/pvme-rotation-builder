from ability_dmg import AD_INS
from on_hit import HIT_INS
from dmg_boost import DMG_BOOST_INS
from get_entry import ENTRY_INS
from settings import SET_INS
from duration_effects import EFF_INS

SET_INS.get_weapon_style()
AD_INS.calculate_levels()
AD_INS.compute_bonus()
AD_INS.base_ability_dmg()

ENTRY_INS.get_entry('blood essence', 0)
EFF_INS.set_blood_ess()
AD_INS.calculate_levels()
AD_INS.compute_bonus()
AD_INS.base_ability_dmg()

print(AD_INS.magicLvl)