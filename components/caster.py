from item_functions import cast_fireball

class Caster:
    def __init__(self, mana=0, xp=0):
        self.mana = mana
        self.xp = xp

    def cast_spell(self, verse, game_map, entities, colors):
        results = []
        if verse[0] == 'fireball':
            if verse[1] == 'north':
                results.append(cast_fireball(verse, colors, entities=entities, game_map=game_map, damage=40, radius=3,
                              target_x=self.owner.x, target_y=self.owner.y + 3))
                results.append({'spell_cast': True})

        return results
        
