import tdl

from entity import Entity
from input_handlers import handle_keys
from map_utils import make_map
from render_functions import render_all, clear_all

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    colors = {
            'dark_wall': (0,0,100),
            'dark_ground': (50,50,150)
            }

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', (255,255,255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), 'G', (0,255,0))
    entities = [npc, player]

    tdl.set_font('resources/arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(screen_width, screen_height, title='Caster')
    con = tdl.Console(screen_width, screen_height)

    game_map = tdl.map.Map(map_width, map_height)
    make_map(game_map)

    while not tdl.event.is_window_closed():
        render_all(con, entities, game_map, root_console, screen_width, screen_height, colors)

        tdl.flush()

        clear_all(con, entities)

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None
        
        if not user_input:
            continue

        action = handle_keys(user_input)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            next_x = player.x + dx
            next_y = player.y + dy
            if game_map.walkable[next_x, next_y] and 0 < next_x < map_width -1 and 0 < next_y < map_height -1:
                player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

if __name__ == '__main__':
    main()
