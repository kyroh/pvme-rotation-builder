style = input('Enter your weapon type:\n')
range_level = float(input('Enter your range level:\n'))
tier_2h = 95
tier_mh = 92
tier_oh = 92
ammo_dmg = 950
armor_bonus = 200

def calculate_dmg():
    if style == '2h':
        ability_damage = 3.75 * range_level + min(14.4 * tier_2h, 1.5 * ammo_dmg) + 1.5 * armor_bonus
        print(ability_damage)
    elif style == 'dw':
        mainhand_dmg = 2.5 * range_level + min(9.6 * tier_mh, ammo_dmg) + armor_bonus
        offhand_dmg = 1.25 * range_level + min(4.8 * tier_oh, ammo_dmg) + armor_bonus
        ability_damage = mainhand_dmg + offhand_dmg
        print(ability_damage)
    elif style == 'mainhand':
        ability_damage = 2.5 * range_level + min(9.6 * tier_mh, ammo_dmg) + armor_bonus
        print(ability_damage)
    else:
        print('type shit in right nerd')

calculate_dmg()
