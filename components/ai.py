from random import randint, choice
from entity import get_blocking_entities_at_location

from game_messages import Message

class BasicMonster:
    def __init__(self):
        self.last_target_x = None
        self.last_target_y = None
        self.ally = False
    def take_turn(self, target, game_map, entities):
        results = []
        monster = self.owner

        if game_map.fov[monster.x, monster.y] and target.fighter.visible:
            self.last_target_x = target.x
            self.last_target_y = target.y
            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_map, entities)
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
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

    def __init__(self):
        self.last_player_x = None
        self.last_player_y = None
        self.ally = True
        self.target = None

    def take_turn(self, player, game_map, entities):
        results = []
        monster = self.owner
        enemies = [entity for entity in entities if (game_map.fov[entity.x, entity.y] and entity.ai and not entity.ai.ally)]
        if self.target and (self.target.name.split()[0] == 'remains' or not game_map.fov[self.target.x, self.target.y]):
            self.target = None

        if len(enemies) > 0:
            if self.target is None:
                self.target = choice(enemies)
            if monster.distance_to(self.target) >= 2:
                monster.move_towards(self.target.x, self.target.y, game_map, entities)
            elif self.target.fighter.hp > 0:
                attack_results = monster.fighter.attack(self.target)
                results.extend(attack_results)
        else:
            if game_map.fov[monster.x, monster.y] and player.fighter.visible:
                self.last_player_x = player.x
                self.last_player_y = player.y
                if monster.distance_to(player) >= 2:
                    monster.move_towards(player.x, player.y, game_map, entities)
            elif self.last_player_x and self.last_player_y:
                monster.move_towards(self.last_player_x, self.last_player_y, game_map, entities)
            
        return results
