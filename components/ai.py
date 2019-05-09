from random import randint, choice
from entity import get_blocking_entities_at_location

from game_messages import Message

class BasicMonster:
    def __init__(self):
        self.last_target_x = None
        self.last_target_y = None
        self.ally = False
        self.target = None
    def take_turn(self, target, game_map, entities):
        results = []
        monster = self.owner
        target_allies = [entity for entity in entities if entity.ai and entity.ai.ally]
        target_allies.append(target)
        if self.target is None or self.target.name.split()[0] in ['remains', 'dust']:
            self.target = target
        for entity in target_allies:
            if monster.distance_to(entity) < monster.distance_to(self.target):
                self.target = entity

        if (game_map.fov[monster.x, monster.y] and self.target.fighter.visible) or monster.distance_to(self.target) < 2:
            self.last_target_x = self.target.x
            self.last_target_y = self.target.y
            if monster.distance_to(self.target) >= 2:
                monster.move_towards(self.target.x, self.target.y, game_map, entities)
            elif self.target.fighter.hp > 0:
                attack_results = monster.fighter.attack(self.target)
                results.extend(attack_results)
        elif self.last_target_x and self.last_target_y:
            monster.move_towards(self.last_target_x, self.last_target_y, game_map, entities)
            
        return results

class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns
        self.ally = False

    def take_turn(self, target, game_map, entities):
        results = []
        monster = self.owner

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                random_target = None
                for entity in entities:
                    if entity.x == random_x and entity.y == random_y and entity.fighter:
                        random_target = entity
                if random_target:
                    attack_results = monster.fighter.attack(random_target) 
                    results.extend(attack_results)
                else:
                    self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name))})

        return results

class AlliedMonster:

    def __init__(self, life_turns=None):
        self.ally = True
        self.target = None
        self.life_turns = life_turns

    def take_turn(self, player, game_map, entities):
        results = []
        monster = self.owner
        if self.target and (self.target.name.split()[0] == 'remains'):
            self.target = None
        enemies = [entity for entity in entities if (game_map.fov[entity.x, entity.y] and entity.ai and not entity.ai.ally) or
                                                     entity is self.target]

        if len(enemies) > 0:
            if self.target is None:
                self.target = choice(enemies)
            if monster.distance_to(self.target) >= 2:
                monster.move_towards(self.target.x, self.target.y, game_map, entities)
            elif self.target.fighter.hp > 0:
                attack_results = monster.fighter.attack(self.target)
                results.extend(attack_results)
        else:
            if monster.distance_to(player) >= 3:
                monster.move_towards(player.x, player.y, game_map, entities)

        if self.life_turns is not None:
            self.life_turns -= 1
            if self.life_turns <= 0:
                results.append({'dead': self.owner})
                results.append({'message': Message('The {0} returns to dust.'.format(self.owner.name))})
            
        return results

class GhostMonster:
    def __init__(self):
        self.last_target_x = None
        self.last_target_y = None
        self.ally = False
        self.target = None
    def take_turn(self, target, game_map, entities):
        results = []
        monster = self.owner
        target_allies = [entity for entity in entities if entity.ai and entity.ai.ally]
        target_allies.append(target)
        if self.target is None or self.target.name.split()[0] in ['remains', 'dust']:
            self.target = target
        for entity in target_allies:
            if monster.distance_to(entity) < monster.distance_to(self.target):
                self.target = entity

        if (game_map.fov[monster.x, monster.y] and self.target.fighter.visible) or monster.distance_to(self.target) < 2:
            self.last_target_x = self.target.x
            self.last_target_y = self.target.y
            if monster.distance_to(self.target) >= 2:
                monster.move_towards(self.target.x, self.target.y, game_map, entities)
        elif self.last_target_x and self.last_target_y:
            monster.move_towards(self.last_target_x, self.last_target_y, game_map, entities)
            
        return results
