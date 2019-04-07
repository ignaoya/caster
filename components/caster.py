from magic.spell_functions import cast_fireball, cast_lightning, cast_invisibility
from game_messages import Message

class Caster:
    def __init__(self, mana, focus, regeneration=1):
        self.mana = mana
        self.base_max_mana = mana
        self.focus = focus
        self.base_max_focus = focus
        self.regeneration = regeneration


    @property
    def max_mana(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_mana_bonus
        else:
            bonus = 0

        return self.base_max_mana + bonus

    @property
    def max_focus(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_focus_bonus
        else:
            bonus = 0

        return self.base_max_focus + bonus

    def restore(self, amount):
        self.mana += amount
        if self.mana > self.max_mana:
            self.mana = self.max_mana

    
    def cast_spell(self, verse, game_map, entities, colors):
        results = []
        if verse:
            if verse[0] == 'fireball':
                # The player can direct the location of the fireball by writing the initials of the cardinal locations
                # the amount of times necessary, and he can augment the power of the spell by adding the word burn,
                # also as many times as he wants. The base damage is 20, and for every burn he adds 10 more damage.
                # For example, if he wanted to cast a fireball at three diagonal squares to the north-east with a 
                # power of 40, he would type "fireball n n n e e e burn burn."
                # Note that the order of the operands is irrelevant except for 'fireball', which has to be the first.
                # the above could also be written as "fireball burn n e n burn e e n."
                cardinal = ['north', 'south', 'east', 'west', 'n', 's', 'e', 'w']
                directions = [i for i in verse if i in cardinal] 
                power = 20 + (10 * len([i for i in verse if i == 'burn']))
                x = 0
                y = 0
                for i in directions:
                    if i in ['north', 'n']:
                        y -= 1
                    elif i in ['south', 's']:
                        y += 1
                    elif i in ['east', 'e']:
                        x += 1
                    elif i in ['west', 'w']:
                        x -= 1
                # The order in which results are appended or extended is very important for the game logic, I'm not
                # sure why, but 'spell_cast' should be added first and 'magic_xp' last. Otherwise there are some weird
                # bugs enabled. I should try to simplify the logic eventually.
                results.append({'spell_cast': True})
                results.extend(cast_fireball(verse, colors, entities=entities, game_map=game_map, damage=power, radius=3,
                              target_x=self.owner.x + x, target_y=self.owner.y + y))
                results.append({'magic_xp': power + (power * len(directions))})
                if not results[1].get('consumed'):
                    results.append({'message': Message('The fireball returns to you and deals {0} damage.'.format(
                                                      power * len(directions)), colors.get('red'))})
                    results.extend(self.owner.fighter.take_damage(power * len(directions)))
                    results.append({'magic_xp': power})


            elif verse[0] == 'lightning':
                if len(verse) > 1:
                    if str.isdigit(verse[1]):
                        maximum_range = int(verse[1])
                        damage = 10 * maximum_range
                        results.append({'spell_cast': True})
                        results.extend(cast_lightning(self.owner, colors, entities=entities, game_map=game_map, damage=damage,
                                       maximum_range=maximum_range))
                        if not any(result.get('target') for result in results):
                            results.append({'magic_xp': damage})
                            results.extend(self.owner.fighter.take_damage(damage))
                            results.append({'message': Message('The spell hits you instead for {0} damage.'.format(10 * maximum_range),
                                                       colors.get('red'))})
                        else:
                            results.append({'magic_xp': 20 * maximum_range})
                    else:
                        results.append({'spell_cast': True, 'magic_xp': 10})
                        results.extend(self.owner.fighter.take_damage(10 * len(verse)))
                        results.append({'message': Message('For a wrong word, the electric charge hits you for {0} damage.'.format(
                                                           10 * len(verse)), colors.get('red'))})
                else:
                    maximum_range = 1
                    damage = 10
                    results.append({'spell_cast': True})
                    results.extend(cast_lightning(self.owner, colors, entities=entities, game_map=game_map, damage=damage,
                                   maximum_range=maximum_range))
                    if not any(result.get('target') for result in results):
                        results.append({'magic_xp': 10})
                        results.extend(self.owner.fighter.take_damage(10))
                        results.append({'message': Message('The spell hits you instead for {0} damage.'.format(10),
                                                   colors.get('red'))})
                    else:
                        results.append({'magic_xp': 20})
                    
            elif verse[0] == 'invisibility':
                if len(verse) > 1 and str.isdigit(verse[1]):
                    entity = self.owner
                    turns = 5 * int(verse[1])
                    results.append({'spell_cast': True})
                    results.extend(cast_invisibility(entity, colors, turns=turns))
                    if any(result.get('invisible') for result in results):
                        results.append({'magic_xp': 5 * turns})
                else:
                    entity = self.owner
                    turns = 5
                    results.append({'spell_cast': True})
                    results.extend(cast_invisibility(entity, colors, turns=turns))
                    if any(result.get('invisible') for result in results):
                        results.append({'magic_xp': 25})
            else:
                results.append({'spell_failed': True, 'message': Message('You fail to invoke the proper words. Nothing happens.',
                                                                    colors.get('yellow'))})

        else:
            results.append({'spell_failed': True, 'message': Message('You are an idiot. Nothing happens.',
                                                                colors.get('yellow'))})

                    

        return results
        
