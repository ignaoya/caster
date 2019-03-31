class Fountain:
    def __init__(self, water):
        self.water = water

    def drink(self, player):
        player.fighter.heal(1)
        self.water -= 1
