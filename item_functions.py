from game_messages import Message
from components.ai import ConfusedMonster



""" DEPRECATED FUNCTION!!!! 

def read(*args, **kwargs):
    text = kwargs.get('text')
    colors = args[1]

    results = []

    for sentence in text:
        results.append({'message': Message('The magic word for {0} is {1}'.format(
                                    lexicon[word], word), colors.get('white'))})

    return results
"""
    
def heal(*args, **kwargs):
    entity = args[0]
    colors = args[1]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp and not any(organ for organ in entity.body.organs if organ.state.name != 'PERFECT'):
        results.append({'consumed': False, 'message': Message('You are already at full health', colors.get('yellow'))})
    else:
        entity.fighter.heal(amount)
        for organ in entity.body.organs:
            organ.improve_state(1)
        results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', colors.get('green'))})

    return results

def restore(*args, **kwargs):
    entity = args[0]
    colors = args[1]
    amount = kwargs.get('amount')

    results = []

    if entity.caster.mana == entity.caster.max_mana:
        results.append({'consumed': False, 'message': Message('You are already at full mana', colors.get('yellow'))})
    else:
        entity.caster.restore(amount)
        results.append({'consumed': True, 'message': Message('You restore some energy', colors.get('green'))})

    return results
