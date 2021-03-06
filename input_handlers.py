from game_states import GameStates


def handle_keys(user_input, game_state, *args):
    if user_input:
        if game_state == GameStates.PLAYERS_TURN:
            return handle_player_turn_keys(user_input)
        elif game_state == GameStates.PLAYER_DEAD:
            return handle_player_dead_keys(user_input)
        elif game_state == GameStates.TARGETING:
            return handle_targeting_keys(user_input)
        elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
            return handle_inventory_keys(user_input)
        elif game_state == GameStates.LEVEL_UP:
            return handle_level_up_menu(user_input)
        elif game_state == GameStates.MAGIC_LEVEL_UP:
            return handle_magic_level_up_menu(user_input)
        elif game_state == GameStates.CHARACTER_SCREEN:
            return handle_character_screen(user_input)
        elif game_state == GameStates.BODY_SCREEN:
            return handle_body_screen(user_input)
        elif game_state == GameStates.HELP_SCREEN:
            return handle_help_screen(user_input)
        elif game_state == GameStates.CASTING_SPELL:
            return handle_spell_casting(user_input)
        elif game_state == GameStates.READ_SCROLL:
            return handle_read_scroll(user_input)

    return {}


def handle_player_turn_keys(user_input):
    # Movement keys
    key_char = user_input.char

    if user_input.key == 'UP' or key_char == 'k':
        return {'move': (0, -1)}
    elif user_input.key == 'DOWN' or key_char == 'j':
        return {'move': (0, 1)}
    elif user_input.key == 'LEFT' or key_char == 'h':
        return {'move': (-1, 0)}
    elif user_input.key == 'RIGHT' or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}
    elif key_char == 'z':
        return {'wait': True}

    elif key_char == 'g':
        return {'pickup': True}

    elif key_char == 'i':
        return {'show_inventory': True}

    elif key_char == 'd':
        return {'drop_inventory': True}

    elif key_char == '.' and user_input.shift:
        return {'take_down_stairs': True}

    elif key_char == ',' and user_input.shift:
        return {'take_up_stairs': True}

    elif key_char == 'c':
        return {'show_character_screen': True}

    elif key_char == 'm':
        return {'show_body_screen': True}

    elif key_char == 's':
        return {'cast_spell': True}

    elif key_char == 'o':
        return {'look_around': True}

    elif key_char == '/' and user_input.shift:
        return {'show_help_screen': True}

    elif user_input.key == 'ENTER' and user_input.alt:
        # Alt-Enter: toggle full screen
        return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_targeting_keys(user_input):
    if user_input.key == 'ESCAPE':
        return {'exit': True}

    return {}

def handle_player_dead_keys(user_input):
    key_char = user_input.char

    if user_input.key == 'UP' or key_char == 'k':
        return {'move': (0, -1)}
    elif user_input.key == 'DOWN' or key_char == 'j':
        return {'move': (0, 1)}
    elif user_input.key == 'LEFT' or key_char == 'h':
        return {'move': (-1, 0)}
    elif user_input.key == 'RIGHT' or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}
    elif key_char == 'z':
        return {'wait': True}

    elif key_char == 'o':
        return {'look_around': True}

    elif key_char == '/' and user_input.shift:
        return {'show_help_screen': True}

    elif key_char == 'i':
        return {'show_inventory': True}

    elif user_input.key == 'ENTER' and user_input.alt: 
        # Alt-Enter: toggle full screen
        return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_mouse(mouse_event):
    if mouse_event:
        (x,y) = mouse_event.cell

        if mouse_event.button == 'LEFT':
            return {'left_click': (x, y)}
        elif mouse_event.button == 'RIGHT':
            return {'right_click': (x, y)}

    return {}

def handle_inventory_keys(user_input):
    if not user_input.char:
        return {}

    index = ord(user_input.char) - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if user_input.key == 'ENTER' and user_input.alt: 
        # Alt-Enter: toggle full screen
        return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_main_menu(user_input):
    if user_input:
        key_char = user_input.char

        if key_char == 'a':
            return {'new_game': True}
        elif key_char == 'b':
            return {'load_game': True}
        elif key_char == 'c' or user_input.key == 'ESCAPE':
            return {'exit': True}

    return {}

def handle_level_up_menu(user_input):
    if user_input:
        key_char = user_input.char

        if key_char == 'a':
            return {'level_up': 'hp'}
        elif key_char == 'b':
            return {'level_up': 'str'}
        elif key_char == 'c':
            return {'level_up': 'def'}

    return {}

def handle_magic_level_up_menu(user_input):
    if user_input:
        key_char = user_input.char

        if key_char == 'a':
            return {'level_up': 'mp'}
        elif key_char == 'b':
            return {'level_up': 'fcs'}

    return {}

def handle_character_screen(user_input):
    if user_input.key == 'ESCAPE':
        return {'exit': True}

    return {}

def handle_body_screen(user_input):
    if user_input.key == 'ESCAPE':
        return {'exit': True}

    return {}

def handle_help_screen(user_input):
    if user_input.key == 'ESCAPE':
        return {'exit': True}

    return {}

def handle_spell_casting(user_input):
    if user_input:
        letter = user_input.char
        return {'letter': letter}
    
    return {}

def handle_read_scroll(user_input):
    if user_input.key == 'ESCAPE':
        return {'exit': True}

    return {}
