from random import choice, randint
from game_messages import Message
from components.organ_states import OrganStates

class Fighter:
    def __init__(self, hp, defense, power, xp=0, visible=True):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp
        self.visible = visible
        self.previous_color = None

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return (self.base_power + bonus) // self.owner.body.r_arm.state.value

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return (self.base_defense + bonus) // self.owner.body.l_arm.state.value

    def take_damage(self, amount):
        results = []

        organ_dam_prob = ((self.max_hp - self.hp) / self.max_hp) * 100
        self.hp = max([self.hp - amount, 0])

        if randint(1, 100) <= organ_dam_prob:
            if organ_dam_prob < 100:
                dam_level = randint(1,2) 
            else:
                dam_level = randint(2,4)
            results.extend(choice(self.owner.body.organs).reduce_state(dam_level))

        if any(i for i in self.owner.body.organs if i.state == OrganStates.LOST and i.vital) or (self.owner.body.blooded and 
                                                                                                 self.owner.body.blood < 1):
            results.append({'dead': self.owner})

        return results

    def make_invisible(self):
        self.visible = False
        self.previous_color = self.owner.color
        self.owner.color = (255, 200, 100)

    def make_visible(self):
        self.visible = True
        self.owner.color = self.previous_color

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)))})
            results.extend(target.fighter.take_damage(damage))
            results.append({'xp': damage})

        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name))})

        return results
