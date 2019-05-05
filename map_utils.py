from random import randint, choice

from tdl.map import Map

from render_functions import RenderOrder
from components.ai import BasicMonster
from components.fighter import Fighter
from components.body import Body
from components.item import Item
from components.stairs import Stairs
from components.fountain import Fountain
from components.inventory import Inventory
from components.equipment import Equipment, EquipmentSlots
from components.equippable import Equippable
from entity import Entity
from item_functions import heal, restore
from random_utils import from_dungeon_level, random_choice_from_dict
from game_messages import Message
from loader_functions.data_loaders import load_floor


monsters = {'spider': {'name': 'Spider', 'hp': 5, 'defense': 0, 'power': 2, 'xp': 35, 'item_probability': 100,
    'item_level': 1, 'color': 'black', 'char': 's', 'body': 'octopod'},
            'goblin': {'name': 'Goblin', 'hp': 10, 'defense': 0, 'power': 3, 'xp': 35, 'item_probability': 10,
                'item_level': 1, 'color': 'desaturated_green', 'char': 'g', 'body': 'anthropod'},
            'orc': {'name': 'Orc', 'hp': 20, 'defense': 0, 'power': 4, 'xp': 35, 'item_probability': 5,
                'item_level': 1, 'color': 'desaturated_green', 'char': 'o', 'body': 'anthropod'},
            'troll': {'name': 'Troll', 'hp': 30, 'defense': 2, 'power': 8, 'xp': 100, 'item_probability': 2,
                'item_level': 2, 'color': 'darkness', 'char': 't', 'body': 'anthropod'},
            'daemon': {'name': 'Daemon', 'hp': 100, 'defense': 4, 'power': 20, 'xp': 200, 'item_probability': 1,
                'item_level': 2, 'color': 'darker_orange', 'char': 'D', 'body': 'anthropod'}
                    }

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
            'spider': from_dungeon_level([[100,1], [80, 3], [50, 6], [10, 8]], dungeon_level),
            'goblin': from_dungeon_level([[90,1], [70, 3], [40, 6], [0, 8]], dungeon_level),
            'orc': 80, 
            'troll': from_dungeon_level([[15,3], [30, 5], [60, 7]], dungeon_level),
            'daemon': from_dungeon_level([[15,8], [30, 10], [60, 15]], dungeon_level),
            }

    item_chances = {
            'small_healing_potion': 35, 
            'small_mana_potion': 10,
            'healing_potion': from_dungeon_level([[5,2], [10,4], [20, 6]], dungeon_level),
            'mana_potion': from_dungeon_level([[5,3], [10, 4], [20,6]], dungeon_level),
            'short_sword': from_dungeon_level([[20, 2]], dungeon_level),
            'sword': from_dungeon_level([[5,4]], dungeon_level),
            'small_shield': from_dungeon_level([[20, 4]], dungeon_level),
            'shield': from_dungeon_level([[15, 8]], dungeon_level),
            'fire_scroll': from_dungeon_level([[35, 3]], dungeon_level),
            'lightning_scroll': from_dungeon_level([[35, 1]], dungeon_level),
            'numbers_scroll': from_dungeon_level([[35, 2]], dungeon_level),
            'geography_scroll': from_dungeon_level([[35, 4]], dungeon_level),
            'invisibility_scroll': from_dungeon_level([[35, 2]], dungeon_level),
            'skeleton_scroll': from_dungeon_level([[20, 1]], dungeon_level),
            }

    items = {
            'small_healing_potion': {'name': 'Small Healing Potion', 'item_type': 'potion', 'use_function': heal,
                                     'amount': 25, 'char': '!', 'color': 'red'},
            'small_mana_potion': {'name': 'Small Mana Potion', 'item_type': 'potion', 'use_function': restore,
                                  'amount': 5, 'char': '!', 'color': 'blue'},
            'healing_potion': {'name': 'Healing Potion', 'item_type': 'potion', 'use_function': heal,
                               'amount': 50, 'char': '!', 'color': 'red'},
            'mana_potion': {'name': 'Mana Potion', 'item_type': 'potion', 'use_function': restore,
                                  'amount': 10, 'char': '!', 'color': 'blue'},
            'short_sword': {'name': 'Short Sword', 'item_type': 'equipment', 'char': '/', 'color': 'sky', 'bonuses':
                {'power': 3}, 'slot': EquipmentSlots.MAIN_HAND},
            'sword': {'name': 'Sword', 'item_type': 'equipment', 'char': '/', 'color': 'sky', 'bonuses':
                {'power': 7}, 'slot': EquipmentSlots.MAIN_HAND},
            'small_shield': {'name': 'Small Shield', 'item_type': 'equipment', 'char': ']', 'color': 'darker_orange',
                       'bonuses': {'defense': 1}, 'slot': EquipmentSlots.OFF_HAND},
            'shield': {'name': 'Shield', 'item_type': 'equipment', 'char': ']', 'color': 'darker_orange',
                       'bonuses': {'defense': 3}, 'slot': EquipmentSlots.OFF_HAND},
            'fire_scroll': {'name': 'Scroll of Fire', 'item_type': 'scroll', 'color':'red', 'char': '#',
                            'words': [i for i in lexicon.keys() if lexicon[i] in ['fireball', 'burn']],
                            'lexicon': lexicon, 'addendum': ['Add cardinal directions to set epicenter', 
                                                             'Burn enhances damage']},
            'lightning_scroll': {'name': 'Scroll of Lightning', 'item_type': 'scroll', 'color':'sky', 'char': '#',
                            'words': [i for i in lexicon.keys() if lexicon[i] in ['lightning']],
                            'lexicon': lexicon, 'addendum': ['Add one number to set max range and increase power']},
            'numbers_scroll': {'name': 'Scroll of Counting', 'item_type': 'scroll', 'color':'blue', 'char': '#',
                            'words': [i for i in lexicon.keys() if lexicon[i] in ['1', '2', '3', '4', '5']],
                            'lexicon': lexicon},
            'geography_scroll': {'name': 'Scroll of Moving', 'item_type': 'scroll', 'color':'yellow', 'char': '#',
                            'words': [i for i in lexicon.keys() if lexicon[i] in ['north', 'south', 'east', 'west']],
                             'lexicon': lexicon},
            'invisibility_scroll': {'name': 'Scroll of Invisibility', 'item_type': 'scroll', 'color':'white', 'char': '#',
                            'words': [i for i in lexicon.keys() if lexicon[i] in ['invisibility']],
                             'lexicon': lexicon},
            'skeleton_scroll': {'name': 'Scroll of Raise Skeleton', 'item_type': 'scroll', 'color': 'black', 'char': '#',
                            'words': [i for i in lexicon.keys() if lexicon[i] in ['skeleton']],
                            'lexicon': lexicon},
            }

    for i in range(number_of_monsters):
        # Choose a random location in the room
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            n = random_choice_from_dict(monster_chances)
            monster = create_monster(monsters[n]['name'], monsters[n]['hp'], monsters[n]['defense'], 
                    monsters[n]['power'], monsters[n]['xp'], monsters[n]['item_probability'], monsters[n]['item_level'],
                    colors, monsters[n]['color'], monsters[n]['char'], x, y, monsters[n]['body'])
            entities.append(monster)

    for i in range(number_of_items):
        x = randint(room.x1 + 1, room.x2 -1)
        y = randint(room.y1 + 1, room.y2 -1)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            n = random_choice_from_dict(item_chances)
            item = create_item(items[n]['name'], items[n]['item_type'], colors, items[n]['color'], items[n]['char'],
                               x, y, items[n])

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
    game_map, entities, player_index = load_floor(dungeon_level)
    if game_map is not None and direction == 'up':
        entities[player_index] = player
        start_loc = [(i.x, i.y) for i in entities if i.name == 'Down Stairs']
        player.x = start_loc[0][0]
        player.y = start_loc[0][1]
    else:
        game_map = GameMap(constants['map_width'], constants['map_height'], dungeon_level)
        entities = [player]

        make_map(game_map, constants['max_rooms'], constants['room_min_size'],
                 constants['room_max_size'], constants['map_width'], constants['map_height'], player,
                 entities, constants['colors'], lexicon, direction)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.',
                                        constants['colors'].get('light_violet')))

    return game_map, entities

def create_monster(name, hp, defense, power, xp, item_probability, item_level, colors, color, char, x, y, body_type):
    fighter_component = Fighter(hp=hp, defense=defense, power=power, xp=xp)
    ai_component = BasicMonster()
    body_component = Body(body_type)
    if randint(1, item_probability) == item_probability:
        inventory_component = Inventory(1)
        equipment_component = Equipment()
        loot_component = Item(use_function=heal, amount=25)
        loot = Entity(0,0, '!', colors.get('red'), 'Small Healing Potion', render_order=RenderOrder.ITEM,
                      item=loot_component)
        inventory_component.add_item(loot, colors)
        monster = Entity(x, y, char, colors.get(color), name, blocks=True,
                         render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component,
                         equipment=equipment_component, ai=ai_component, body=body_component)
    else:
        monster = Entity(x, y, char, colors.get(color), name, blocks=True,
                         render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component, body=body_component)
    
    return monster

def create_item(name, item_type, colors, color, char, x, y, kwargs):
    if item_type == 'potion':
        use_function = kwargs.get('use_function')
        amount = kwargs.get('amount')
        item_component = Item(use_function=use_function, amount=amount)
        item = Entity(x, y, char, colors.get(color), name, render_order=RenderOrder.ITEM,
                      item=item_component)

    elif item_type == 'equipment':
        slot = kwargs.get('slot')
        bonuses = kwargs.get('bonuses')
        power_bonus = bonuses.get('power', 0)
        defense_bonus = bonuses.get('defense', 0)
        max_hp_bonus = bonuses.get('hp', 0)
        max_mana_bonus = bonuses.get('mana', 0)
        max_focus_bonus = bonuses.get('focus', 0)
        equippable_component = Equippable(slot, power_bonus=power_bonus, defense_bonus=defense_bonus, max_hp_bonus=max_hp_bonus,
                                          max_mana_bonus=max_mana_bonus, max_focus_bonus=max_focus_bonus)
        item = Entity(x, y, char, colors.get(color), name, equippable=equippable_component)

    elif item_type == 'scroll':
        words = kwargs.get('words')
        lexicon = kwargs.get('lexicon')
        addendum = kwargs.get('addendum')
        text = ['The magic word for {} is {}.'.format(lexicon[word], word) for word in words]
        if addendum:
            text.extend(addendum)
        item_component = Item(text=text)
        item = Entity(x, y, char, colors.get(color), name, render_order=RenderOrder.ITEM,
                item=item_component)

    return item
