style = input('Enter your weapon type:\n')
magic_level = float(input('Enter your magic level:\n'))
tier_2h = 95
tier_mh = 92
tier_oh = 92
spell_level = float(input('Enter your spell level:\n'))
spell_dmg = 9.6 * spell_level
armor_bonus = 200

def compute__magic_dmg():
    if style == '2h':
        ability_damage = 3.75 * magic_level + min(14.4 * tier_2h, 1.5 * spell_dmg) + 1.5 * armor_bonus
        print(ability_damage)
    elif style == 'dw':
        mainhand_dmg = 2.5 * magic_level + min(9.6 * tier_mh, spell_dmg) + armor_bonus
        offhand_dmg = 1.25 * magic_level + min(4.8 * tier_oh, spell_dmg) + armor_bonus
        ability_damage = mainhand_dmg + offhand_dmg
        print(ability_damage)
    elif style == 'mainhand':
        ability_damage = 2.5 * magic_level + min(9.6 * tier_mh, spell_dmg) + armor_bonus
        print(ability_damage)
    else:
        print('type shit in right nerd')

compute__magic_dmg()
