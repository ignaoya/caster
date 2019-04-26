from game_messages import Message
from components.organ_states import OrganStates

class Organ:
    def __init__(self, name, state=OrganStates.PERFECT, vital=False):
        self.name = name
        self.state = state
        self.vital = vital

    def reduce_state(self, levels):
        val = min([self.state.value + levels, 5])
        result = []
        self.state = OrganStates(val)
        result.append({'message': Message("The {}'s {} is now {}".format(self.owner.owner.name, self.name, self.state.name))})

        return result

    def improve_state(self, levels):
        if self.state == OrganStates.LOST:
            message = "The {}'s {} cannot be recovered.".format(self.owner.owner.name, self.name)
            return [{'message': Message(message)}]
        else:
            val = max([self.state.value - levels, 1])
            self.state = States(val)

