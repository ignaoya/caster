from magic.spell_functions import cast_fireball, cast_lightning

class Caster:
    def __init__(self, mana=0, xp=0):
        self.mana = mana
        self.xp = xp

    def cast_spell(self, verse, game_map, entities, colors):
        results = []
        if verse[0] == 'fireball':
            results.append({'spell_cast': True})
            results.extend(cast_fireball(verse, colors, entities=entities, game_map=game_map, damage=40, radius=3,
                          target_x=self.owner.x, target_y=self.owner.y))
        elif verse[0] == 'lightning':
            maximum_range = int(verse[1])
            results.append({'spell_cast': True})
            results.extend(cast_lightning(self.owner, colors, entities=entities, game_map=game_map, damage=40,
                           maximum_range=maximum_range))

        return results
        
