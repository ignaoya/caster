from magic.spell_functions import cast_fireball, cast_lightning
from game_messages import Message

class Caster:
    def __init__(self, mana=0, xp=0):
        self.mana = mana
        self.xp = xp

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
                cardinal = ['n', 's', 'e', 'w']
                directions = [i for i in verse if i in cardinal] 
                power = 20 + (10 * len([i for i in verse if i == 'burn']))
                x = 0
                y = 0
                for i in directions:
                    if i == 'n':
                        y -= 1
                    elif i == 's':
                        y += 1
                    elif i == 'e':
                        x += 1
                    elif i == 'w':
                        x -= 1
                results.append({'spell_cast': True})
                results.extend(cast_fireball(verse, colors, entities=entities, game_map=game_map, damage=power, radius=3,
                              target_x=self.owner.x + x, target_y=self.owner.y + y))

            elif verse[0] == 'lightning':
                if str.isdigit(verse[1]):
                    maximum_range = int(verse[1])
                    results.append({'spell_cast': True})
                    results.extend(cast_lightning(self.owner, colors, entities=entities, game_map=game_map, damage=40,
                                   maximum_range=maximum_range))
                    if not any(result.get('target') for result in results):
                        results.append({'spell_cast': True})
                        results.extend(self.owner.fighter.take_damage(10 * maximum_range))
                        results.append({'message': Message('The spell hits you instead for {0} damage.'.format(10 * maximum_range),
                                                   colors.get('red'))})
                else:
                    results.append({'spell_failed': True})
                    results.extend(self.owner.fighter.take_damage(10 * len(verse)))
                    results.append({'message': Message('For a wrong word, the electric charge hits you for {0} damage.'.format(
                                                       10 * len(verse)), colors.get('red'))})
            else:
                results.append({'spell_failed': True, 'message': Message('You fail to invoke the proper words. Nothing happens.',
                                                                    colors.get('yellow'))})

        else:
            results.append({'spell_failed': True, 'message': Message('You are an idiot. Nothing happens.',
                                                                colors.get('yellow'))})

                    

        return results
        
