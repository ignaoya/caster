import math
from random import choice

from components.item import Item

from render_functions import RenderOrder

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, caster=None, ai=None,
                 item=None, inventory=None, stairs=None, fountain=None, level=None, equipment=None, equippable=None, body=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.caster = caster
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.fountain = fountain
        self.level = level
        self.equipment = equipment
        self.equippable = equippable
        self.body = body

        if self.fighter:
            self.fighter.owner = self

        if self.caster:
            self.caster.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self

            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

        if self.body:
            self.body.owner = self

    def move(self, dx, dy):
        # Move entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        path = game_map.compute_path(self.x, self.y, target_x, target_y)

        if path:
            dx = path[0][0] - self.x
            dy = path[0][1] - self.y

            if game_map.walkable[path[0][0], path[0][1]] and not get_blocking_entities_at_location(
                    entities, self.x + dx, self.y + dy):
                self.move(dx, dy)
            else:
                if self.x == target_x:
                    if self.y > target_y:
                        self.move_towards(target_x + choice((1,-1)), target_y + 1, game_map, entities)
                    else:
                        self.move_towards(target_x + choice((1, -1)), target_y - 1, game_map, entities)
                elif self.y == target_y:
                    if self.x > target_x:
                        self.move_towards(target_x + 1, target_y + choice((1, -1)), game_map, entities)
                    else:
                        self.move_towards(target_x - 1, target_y + choice((1, -1)), game_map, entities)
                elif self.x > target_x and self.y > target_y:
                    x, y = choice(((-1,0),(0,-1)))
                    self.move_towards(self.x + x, self.y + y, game_map, entities)
                elif self.x > target_x and self.y < target_y:
                    x, y = choice(((-1,0),(0,1)))
                    self.move_towards(self.x + x, self.y + y, game_map, entities)
                elif self.x < target_x and self.y < target_y:
                    x, y = choice(((1,0),(0,1)))
                    self.move_towards(self.x + x, self.y + y, game_map, entities)
                elif self.x < target_x and self.y > target_y:
                    x, y = choice(((1,0),(0,-1)))
                    self.move_towards(self.x + x, self.y + y, game_map, entities)


    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None
