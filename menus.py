import tdl

import textwrap

def menu(con, root, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header ( after textwrap) and one line per option
    header_wrapped = textwrap.wrap(header, width)
    header_height = len(header_wrapped)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = tdl.Console(width, height)

    # print the header, with wrapped text
    window.draw_rect(0, 0, width, height, None, fg=(255,255,255), bg=None)
    for i, line in enumerate(header_wrapped):
        window.draw_str(0, 0 + i, header_wrapped[i])

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        window.draw_str(0, y, text, bg=None)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = screen_width // 2 - width // 2
    y = screen_height // 2 - height // 2
    root.blit(window, x, y, width, height, 0, 0)

def inventory_menu(con, root, header, player, inventory_width, screen_width, screen_height):
    # show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (on main hand)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (on off hand)'.format(item.name))
            else:
                options.append(item.name)

    menu(con, root, header, options, inventory_width, screen_width, screen_height)

def main_menu(con, root_console, background_image, screen_width, screen_height, colors):
    background_image.blit_2x(root_console, 0, 0)

    title = 'CASTER'
    center = (screen_width - len(title)) // 2
    root_console.draw_str(center, screen_height // 2 - 4, title, bg=None, fg=colors.get('light_yellow'))

    title = 'By Ignacio Oyarzabal'
    center = (screen_width - len(title)) // 2
    root_console.draw_str(center, screen_height - 2, title, bg=None, fg=colors.get('light_yellow'))

    menu(con, root_console, '', ['New Game', 'Continue', 'Quit'], 24, screen_width, screen_height)

def level_up_menu(con, root, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution (+20 HP, from {0})'.format(player.fighter.max_hp),
               'Strength (+1 attack, from {0})'.format(player.fighter.power),
               'Agility (+1 defense, from {0})'.format(player.fighter.defense)]

    menu(con, root, header, options, menu_width, screen_width, screen_height)

def magic_level_up_menu(con, root, header, player, menu_width, screen_width, screen_height):
    options = ['Mana (+2 MP, from {0})'.format(player.caster.max_mana),
               'Focus (+1 focus, from {0})'.format(player.caster.max_focus)]

    menu(con, root, header, options, menu_width, screen_width, screen_height)

def scroll_menu(con, root, scroll, menu_width, screen_width, screen_height):
    header = scroll.name
    options = scroll.item.function_kwargs.get('text')
    menu(con, root, header, options, menu_width, screen_width, screen_height)

def character_screen(root_console, player, character_screen_width, character_screen_height, screen_width,
                     screen_height):
    window = tdl.Console(character_screen_width, character_screen_height)

    window.draw_rect(0, 0, character_screen_width, character_screen_height, None, fg=(255,255,255), bg=None)

    window.draw_str(0, 1, 'Character Information')
    window.draw_str(0, 2, 'Fighting')
    window.draw_str(0, 3, 'Level: {0}'.format(player.level.fighter_level))
    window.draw_str(0, 4, 'Experience: {0}'.format(player.level.fighter_xp))
    window.draw_str(0, 5, 'Experience to Level Up: {0}'.format(player.level.experience_to_next_fighter_level))
    window.draw_str(0, 7, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    if player.fighter.power != player.fighter.base_power:
        window.draw_str(0, 8, 'Attack: {0}(+{1})'.format(player.fighter.base_power, player.equipment.power_bonus))
    else:
        window.draw_str(0, 8, 'Attack: {0}'.format(player.fighter.power))
    if player.fighter.defense != player.fighter.base_defense:
        window.draw_str(0, 9, 'Defense: {0}(+{1})'.format(player.fighter.base_defense, player.equipment.defense_bonus))
    else:
        window.draw_str(0, 9, 'Defense: {0}'.format(player.fighter.defense))
    window.draw_str(31, 2, 'Spellcasting')
    window.draw_str(31, 3, 'Level: {0}'.format(player.level.caster_level))
    window.draw_str(31, 4, 'Experience: {0}'.format(player.level.caster_xp))
    window.draw_str(31, 5, 'Experience to Level Up: {0}'.format(player.level.experience_to_next_caster_level))
    if player.caster.max_mana != player.caster.base_max_mana:
        window.draw_str(31, 7, 'Maximum MP: {0}(+{1})'.format(player.caster.base_max_mana, player.equipment.max_mana_bonus))
    else:
        window.draw_str(31, 7, 'Maximum MP: {0}'.format(player.caster.max_mana))
    if player.caster.max_focus != player.caster.base_max_focus:
        windos.draw_str(31, 8, 'Focus: {0}(+{1})'.format(player.caster.base_max_focus, player.equipment.max_focus_bonus))
    else:
        window.draw_str(31, 8, 'Focus: {0}'.format(player.caster.max_focus))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    root_console.blit(window, x, y, character_screen_width, character_screen_height, 0, 0)

def body_screen(root_console, player, character_screen_width, character_screen_height, screen_width,
                     screen_height):
    window = tdl.Console(character_screen_width, character_screen_height)

    window.draw_rect(0, 0, character_screen_width, character_screen_height, None, fg=(255,255,255), bg=None)

    window.draw_str(0, 1, 'Body Health Information')
    window.draw_str(0, 2, 'Limbs And Non-Vital Organs')
    window.draw_str(0, 3, 'Blood: {0}'.format(player.body.blood))
    window.draw_str(0, 4, 'Left Leg: {0}'.format(player.body.l_leg.state.name))
    window.draw_str(0, 5, 'Right Leg: {0}'.format(player.body.r_leg.state.name))
    window.draw_str(0, 7, 'Left Arm: {0}'.format(player.body.l_arm.state.name))
    window.draw_str(0, 8, 'Right Arm: {0}'.format(player.body.r_arm.state.name))
    window.draw_str(0, 9, 'Left Eye: {0}'.format(player.body.l_eye.state.name))
    window.draw_str(0, 10, 'Right Eye: {0}'.format(player.body.r_eye.state.name))
    window.draw_str(0, 11, 'Left Ear: {0}'.format(player.body.l_ear.state.name))
    window.draw_str(0, 12, 'Right Ear: {0}'.format(player.body.r_ear.state.name))
    window.draw_str(0, 13, 'Kidneys: {0}'.format(player.body.kidneys.state.name))
    window.draw_str(31, 2, 'Vital Organs')
    window.draw_str(31, 3, 'Heart: {0}'.format(player.body.heart.state.name))
    window.draw_str(31, 4, 'Brain: {0}'.format(player.body.brain.state.name))
    window.draw_str(31, 5, 'Stomach: {0}'.format(player.body.stomach.state.name))
    window.draw_str(31, 6, 'Lungs: {0}'.format(player.body.lungs.state.name))
    window.draw_str(31, 7, 'Liver: {0}'.format(player.body.liver.state.name))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    root_console.blit(window, x, y, character_screen_width, character_screen_height, 0, 0)

def help_screen(root_console, character_screen_width, character_screen_height, screen_width, screen_height):

    window = tdl.Console(character_screen_width, character_screen_height)

    window.draw_rect(0, 0, character_screen_width, character_screen_height, None, fg=(255,255,255), bg=None)

    window.draw_str(0, 1, 'Controls')
    window.draw_str(0, 3, '(h,j,k,l) -> left, down, up and right.')
    window.draw_str(0, 4, '(y,u,b,n) -> diagonal directions.')
    window.draw_str(0, 6, '(z) -> wait a turn or drink from fountain.')
    window.draw_str(0, 8, '(g) -> pickup item.')
    window.draw_str(0, 10, '(i) -> show inventory.')
    window.draw_str(0, 11, 'While inventory: (a-z) use or equip item.')
    window.draw_str(0, 13, '(d) -> show inventory to drop item.')
    window.draw_str(0, 14, 'While drop open: (a-z) drop item.')
    window.draw_str(0, 16, '(>) -> take down-stairs.')
    window.draw_str(0, 17, '(<) -> take up-stairs.')
    window.draw_str(0, 19, '(c) -> show character screen.')
    window.draw_str(0, 21, '(o) -> look around.')
    window.draw_str(0, 23, '(s) -> start casting spell.')
    window.draw_str(0, 24, 'While casting: write magic words.')
    window.draw_str(0, 25, 'Magic words are found in scrolls.')
    window.draw_str(0, 26, 'While casting: (.) -> end spell.')
    window.draw_str(0, 28, '(?) -> Show this help screen.')
    window.draw_str(0, 30, '(Esc) -> exit menus or save+quit.')
    window.draw_str(46, 1, 'Symbols')
    window.draw_str(46, 3, '@ -> player character.')
    window.draw_str(46, 5, '> -> down-staircase.')
    window.draw_str(46, 7, '< -> up-staircase.')
    window.draw_str(46, 9, '+ -> fountain.')
    window.draw_str(46, 11, '! -> potion(life or mana).')
    window.draw_str(46, 13, '# -> magic scroll.')
    window.draw_str(46, 15, '/ -> sword.')
    window.draw_str(46, 17, '- -> dagger.')
    window.draw_str(46, 19, '] -> shield.')
    window.draw_str(46, 21, 's -> spider or skeleten.')
    window.draw_str(46, 23, 'g -> goblin.')
    window.draw_str(46, 25, 'o -> orc.')
    window.draw_str(46, 27, 't -> troll.')
    window.draw_str(46, 29, 'D -> Daemon.')

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    root_console.blit(window, x, y, character_screen_width, character_screen_height, 0, 0)

def message_box(con, root_console, header, width, screen_width, screen_height):
    menu(con, root_console, header, [], width, screen_width, screen_height)

