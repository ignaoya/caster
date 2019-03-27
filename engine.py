import tdl

from entity import Entity
from input_handlers import handle_keys
from map_utils import GameMap, make_map
from render_functions import render_all, clear_all

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 'BASIC'
    fov_light_walls = True
    fov_radius = 10

    colors = {
            'darkness': (0, 0, 10),
            'dark_wall': (0,0,60),
            'dark_ground': (30,30,100),
            'light_wall': (130, 110, 50),
            'light_ground': (200, 180, 50),
            }

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', (255,255,255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), 'G', (0,255,0))
    entities = [npc, player]

    tdl.set_font('resources/arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(screen_width, screen_height, title='Caster')
    con = tdl.Console(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player)
    
    fov_recompute = True

    while not tdl.event.is_window_closed():
        if fov_recompute:
            game_map.compute_fov(player.x, player.y, fov=fov_algorithm, radius=fov_radius, light_walls=fov_light_walls)

        render_all(con, entities, game_map, fov_recompute, root_console, screen_width, screen_height, colors)
        tdl.flush()

        clear_all(con, entities)

        fov_recompute = False

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
            if game_map.walkable[next_x, next_y]:
                player.move(dx, dy)
                fov_recompute = True

        if exit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

if __name__ == '__main__':
    main()
