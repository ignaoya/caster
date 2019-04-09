from random import randint, choice

from tdl.map import Map

from render_functions import RenderOrder
from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs
from components.fountain import Fountain
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from entity import Entity
from item_functions import heal, read, restore
from random_utils import from_dungeon_level, random_choice_from_dict
from game_messages import Message

class GameMap(Map):
    def __init__(self, width, height, dungeon_level=1):
        super().__init__(width, height)
        self.explored = [[False for y in range(height)] for x in range(width)]
        self.dungeon_level = dungeon_level

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

def create_room(game_map, room):
    # go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            game_map.walkable[x, y] = True
            game_map.transparent[x, y] = True

def create_h_tunnel(game_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True

def create_v_tunnel(game_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True

def place_entities(room, entities, dungeon_level, colors, lexicon):
    max_monsters_per_room = from_dungeon_level([[2,1], [3,4], [5,6]], dungeon_level)
    max_items_per_room = from_dungeon_level([[1,1], [2,4]], dungeon_level)
    # Get a random number of monsters
    number_of_monsters = randint(0, max_monsters_per_room)
    number_of_items = randint(0, max_items_per_room)

    monster_chances  = {
            'orc': 80, 
            'troll': from_dungeon_level([[15,3], [30, 5], [60, 7]], dungeon_level),
            }
    item_chances = {
            'small_healing_potion': 35, 
            'small_mana_potion': 10,
            'healing_potion': from_dungeon_level([[5,2], [10,4], [20, 6]], dungeon_level),
            'mana_potion': from_dungeon_level([[5,3], [10, 4], [20,6]], dungeon_level),
            'sword': from_dungeon_level([[5,4]], dungeon_level),
            'shield': from_dungeon_level([[15, 8]], dungeon_level),
            'fire_scroll': from_dungeon_level([[35, 3]], dungeon_level),
            'lightning_scroll': from_dungeon_level([[35, 1]], dungeon_level),
            'numbers_scroll': from_dungeon_level([[35, 2]], dungeon_level),
            'geography_scroll': from_dungeon_level([[35, 4]], dungeon_level),
            'invisibility_scroll': from_dungeon_level([[35, 2]], dungeon_level),
            }

    for i in range(number_of_monsters):
        # Choose a random location in the room
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            monster_choice = random_choice_from_dict(monster_chances)

            if monster_choice == 'orc':
                fighter_component = Fighter(hp=20, defense=0, power=4, xp=35)
                ai_component = BasicMonster()

                monster = Entity(x, y, 'o', colors.get('desaturated_green'), 'Orc', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
            else:
                fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
                ai_component = BasicMonster()

                monster = Entity(x, y, 'T', colors.get('darker_green'), 'Troll', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

            entities.append(monster)

    for i in range(number_of_items):
        x = randint(room.x1 + 1, room.x2 -1)
        y = randint(room.y1 + 1, room.y2 -1)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            item_choice = random_choice_from_dict(item_chances)

            if item_choice == 'small_healing_potion':
                item_component = Item(use_function=heal, amount=25)
                item = Entity(x, y, '!', colors.get('red'), 'Small Healing Potion', render_order=RenderOrder.ITEM,
                              item=item_component)
            elif item_choice == 'small_mana_potion':
                item_component = Item(use_function=restore, amount=5)
                item = Entity(x, y, '!', colors.get('blue'), 'Small Mana Potion', render_order=RenderOrder.ITEM,
                              item=item_component)
            if item_choice == 'healing_potion':
                item_component = Item(use_function=heal, amount=50)
                item = Entity(x, y, '!', colors.get('red'), 'Healing Potion', render_order=RenderOrder.ITEM,
                              item=item_component)
            elif item_choice == 'mana_potion':
                item_component = Item(use_function=restore, amount=10)
                item = Entity(x, y, '!', colors.get('blue'), 'Mana Potion', render_order=RenderOrder.ITEM,
                              item=item_component)
            elif item_choice == 'sword':
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                item = Entity(x, y, '/', colors.get('sky'), 'Sword', equippable=equippable_component)
            elif item_choice == 'shield':
                equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
                item = Entity(x, y, '[', colors.get('darker_orange'), 'Shield', equippable=equippable_component)
            elif item_choice == 'fire_scroll':
                word = [i for i in lexicon.keys() if lexicon[i] in ['fireball', 'burn']]
                item_component = Item(use_function=read, lexicon=lexicon, word=word)
                item = Entity(x, y, '#', colors.get('red'), 'Scroll of Fire', render_order=RenderOrder.ITEM,
                        item=item_component)
            elif item_choice == 'lightning_scroll':
                word = [i for i in lexicon.keys() if lexicon[i] in ['lightning']]
                item_component = Item(use_function=read, lexicon=lexicon, word=word)
                item = Entity(x, y, '#', colors.get('sky'), 'Scroll of Lightning', render_order=RenderOrder.ITEM,
                        item=item_component)
            elif item_choice == 'numbers_scroll':
                word = [i for i in lexicon.keys() if lexicon[i] in ['1', '2', '3', '4', '5']]
                item_component = Item(use_function=read, lexicon=lexicon, word=word)
                item = Entity(x, y, '#', colors.get('black'), 'Scroll of Counting', render_order=RenderOrder.ITEM,
                        item=item_component)
            elif item_choice == 'geography_scroll':
                word = [i for i in lexicon.keys() if lexicon[i] in ['north', 'south', 'east', 'west']]
                item_component = Item(use_function=read, lexicon=lexicon, word=word)
                item = Entity(x, y, '#', colors.get('yellow'), 'Scroll of Moving', render_order=RenderOrder.ITEM,
                        item=item_component)
            elif item_choice == 'invisibility_scroll':
                word = [i for i in lexicon.keys() if lexicon[i] in ['invisibility']]
                item_component = Item(use_function=read, lexicon=lexicon, word=word)
                item = Entity(x, y, '#', colors.get('white'), 'Scroll of Invisibility', render_order=RenderOrder.ITEM,
                        item=item_component)


            entities.append(item)

def make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player,
             entities, colors, lexicon, direction=None):
    rooms = []
    num_rooms = 0

    center_of_last_room_x = None
    center_of_last_room_y = None

    for r in range(max_rooms):
        # random width and height
        w = randint(room_min_size, room_max_size)
        h = randint(room_min_size, room_max_size)
        # random position without going out of the boundaries of the map
        x = randint(0, map_width - w - 1)
        y = randint(0, map_height - h - 1)

        # "Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)

        # Run through the other rooms and see if they intersect  with this one
        for other_room in rooms:
            if new_room.intersect(other_room):
                break
        else:
            # this means there are no intersections, so this room is valid
            
            # paint it to the map's tiles
            create_room(game_map, new_room)

            # center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()

            center_of_last_room_x = new_x
            center_of_last_room_y = new_y

            if num_rooms == 0:
                # this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y
            else:
                # all rooms after the first:
                # connect it to the previous room with a tunnel

                # center coordinates of previous room 
                (prev_x, prev_y) = rooms[num_rooms -1].center()

                # flip a coin (random number that is either 0 or 1)
                if randint(0,1):
                    # first move horizontally, then vertically
                    create_h_tunnel(game_map, prev_x, new_x, prev_y)
                    create_v_tunnel(game_map, prev_y, new_y, new_x)
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(game_map, prev_y, new_y, prev_x)
                    create_h_tunnel(game_map, prev_x, new_x, new_y)

            place_entities(new_room, entities, game_map.dungeon_level, colors, lexicon)

            # finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1
            
    if direction == 'down':
        down_stairs_component = Stairs(game_map.dungeon_level + 1, 'down')
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', (255,255,255), 'Down Stairs',
                            render_order=RenderOrder.STAIRS, stairs=down_stairs_component)
        entities.append(down_stairs)

        up_stairs_component = Stairs(game_map.dungeon_level - 1, 'up')
        up_stairs = Entity(player.x, player.y, '<', (255,255,255), 'Up Stairs',
                           render_order=RenderOrder.STAIRS, stairs=up_stairs_component)
        entities.append(up_stairs)

    elif direction == 'up':
        down_stairs_component = Stairs(game_map.dungeon_level + 1, 'down')
        down_stairs = Entity(player.x, player.y, '>', (255,255,255), 'Down Stairs',
                            render_order=RenderOrder.STAIRS, stairs=down_stairs_component)
        entities.append(down_stairs)

        up_stairs_component = Stairs(game_map.dungeon_level - 1, 'up')
        up_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '<', (255,255,255), 'Up Stairs',
                           render_order=RenderOrder.STAIRS, stairs=up_stairs_component)
        entities.append(up_stairs)

    else:
        down_stairs_component = Stairs(game_map.dungeon_level + 1, 'down')
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', (255,255,255), 'Down Stairs',
                            render_order=RenderOrder.STAIRS, stairs=down_stairs_component)
        entities.append(down_stairs)

    # choose a random room from all rooms except the first and the last, to put a fountain of health
    fountain_location = rooms[randint(1, len(rooms) - 2)]
    (fountain_x, fountain_y) = fountain_location.center()
    fountain_component = Fountain(20 * game_map.dungeon_level)
    fountain = Entity(fountain_x, fountain_y, '+', colors.get('blue'), 'Fountain',
            render_order=RenderOrder.ITEM, fountain=fountain_component)
    entities.append(fountain)

def next_floor(player, message_log, dungeon_level, constants, lexicon, direction):
    game_map = GameMap(constants['map_width'], constants['map_height'], dungeon_level)
    entities = [player]

    make_map(game_map, constants['max_rooms'], constants['room_min_size'],
             constants['room_max_size'], constants['map_width'], constants['map_height'], player,
             entities, constants['colors'], lexicon, direction)

    player.fighter.heal(player.fighter.max_hp // 2)

    message_log.add_message(Message('You take a moment to rest, and recover your strength.',
                                    constants['colors'].get('light_violet')))

    return game_map, entities
