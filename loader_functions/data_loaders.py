import os

import shelve


def save_game(player, entities, game_map, message_log, game_state, lexicon):
    with shelve.open('savegame.dat', 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state
        data_file['lexicon'] = lexicon

def save_floor(player, entities, game_map):
    with shelve.open('savefloor.dat', 'w') as data_file:
        floor = 'floor_{}'.format(game_map.dungeon_level)
        data_file[floor] = {'game_map': game_map, 'entities': entities, 'player_index': entities.index(player)}

def erase_floor_file():
    with shelve.open('savefloor.dat', 'n') as data_file:
        pass

def load_game():
    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError

    with shelve.open('savegame.dat', 'r') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']
        lexicon = data_file['lexicon']

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state, lexicon

def load_floor(level):
    if not os.path.isfile('savefloor.dat'):
        raise FileNotFoundError

    with shelve.open('savefloor.dat', 'r') as data_file:
        floor = 'floor_{}'.format(level)
        try:
            game_map = data_file[floor]['game_map']
            entities = data_file[floor]['entities']
            player_index = data_file[floor]['player_index']

        except KeyError:
            game_map = None
            entities = None
            player_index = None

    return game_map, entities, player_index

