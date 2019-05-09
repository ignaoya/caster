from game_messages import Message
from render_functions import RenderOrder
from game_states import GameStates
from entity import Entity
from components.fighter import Fighter
from components.ghost import Ghost
from components.ai import AlliedMonster, ConfusedMonster, BasicMonster, GhostMonster
from map_utils import monsters


def kill_player(player, colors):
    player.char = '&'
    player.color = colors.get('dark_red')
    ghost_component = Ghost()
    ghost_component.owner = player
    player.ghost = ghost_component

    return Message('You died and are now a ghost! Put the souls of your victims to rest if you want to reincarnate!', 
                    colors.get('red')), GameStates.PLAYER_DEAD


def kill_monster(monster, entities, colors):
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), colors.get('orange'))

    if any(word for word in monster.name.split() if word == 'skeleton'):
        monster.char = ':'
        monster.color = colors.get('white')
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.name = 'dust of ' + monster.name
        monster.render_order = RenderOrder.CORPSE
    else:
        monster.char = '%'
        monster.color = colors.get('dark_red')
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.name = 'remains of ' + monster.name
        monster.render_order = RenderOrder.CORPSE

        ghost_component = Ghost()
        ai_component = GhostMonster()
        ghost_name = 'ghost of ' + monster.name.split()[-1]
        ghost = Entity(monster.x, monster.y, '&', colors.get('white'), ghost_name, blocks=False, 
                       render_order=RenderOrder.ACTOR, ai=ai_component, ghost=ghost_component)
        entities.append(ghost)    
        
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
    monster.fighter = fighter_component
    monster.ai = ai_component
    monster.name = ' '.join([origin, 'skeleton'])
    monster.render_order = RenderOrder.ACTOR

    message = {'message': Message('The {0} rises from the dead.'.format(monster.name), colors.get('red'))}

    return message
