from game_messages import Message
from render_functions import RenderOrder
from game_states import GameStates
from components.fighter import Fighter
from components.ai import AlliedMonster, ConfusedMonster, BasicMonster
from components.body import Body
from map_utils import monsters


def kill_player(player, colors):
    player.char = '%'
    player.color = colors.get('dark_red')

    return Message('You died!', colors.get('red')), GameStates.PLAYER_DEAD


def kill_monster(monster, entities, colors):
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), colors.get('orange'))

    if any(word for word in monster.name.split() if word == 'skeleton'):
        monster.char = ':'
        monster.color = colors.get('white')
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.body = None
        monster.name = 'dust of ' + monster.name
        monster.render_order = RenderOrder.CORPSE
    else:
        monster.char = '%'
        monster.color = colors.get('dark_red')
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.body.alive = False
        monster.body.animated = False
        monster.name = 'remains of ' + monster.name
        monster.render_order = RenderOrder.CORPSE

    if monster.inventory:
        for i in monster.inventory.items:
            entities.append(i)
            monster.inventory.drop_item(i, colors)

    return death_message

def raise_monster_skeleton(monster, life_turns, entities, colors):
    origin = monster.name.split()[2].lower()
    monster.char = 's'
    monster.color = colors.get('white')
    monster.blocks = True
    fighter_component = Fighter(hp=monsters[origin]['hp']//2, defense=0, power=monsters[origin]['power']//2)
    fighter_component.owner = monster
    #basic_ai = BasicMonster()
    #basic_ai.owner = monster
    ai_component = AlliedMonster(life_turns)
    ai_component.owner = monster
    body_component = Body(body_type = monster.body.body_type + '_skeleton')
    body_component.owner = monster
    monster.fighter = fighter_component
    monster.ai = ai_component
    monster.body = body_component
    monster.name = ' '.join([origin, 'skeleton'])
    monster.render_order = RenderOrder.ACTOR

    message = {'message': Message('The {0} rises from the dead.'.format(monster.name), colors.get('red'))}

    return message
