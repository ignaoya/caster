from game_messages import Message
from components.organ_states import OrganStates

class Limb:
    def __init__(self, name, state=OrganStates.PERFECT):
        self.name = name
        self.state = state

    def reduce_state(self, levels):
        val = self.state.value + levels
        try:
            self.state = OrganStates(val)
        except:
            val -= 1
            self.reduce_state(val)

    def improve_state(self, levels):
        if self.state == OrganStates.LOST:
            message = "The {}'s {} cannot be recovered.".format(self.owner.owner.name, self.name)
            return [{'message': Message(message)}]
        else:
            val = self.state.value - levels
            self.state = States(max([1, val]))
