class Level:
    def __init__(self, fighter_level=1, fighter_xp=0, caster_level=1, caster_xp=0, level_up_factor=100):
        self.fighter_level = fighter_level
        self.fighter_xp = fighter_xp
        self.caster_level = caster_level
        self.caster_xp = caster_xp
        self.level_up_factor = level_up_factor

    @property
    def experience_to_next_fighter_level(self):
        return self.fighter_level * self.level_up_factor

    @property
    def experience_to_next_caster_level(self):
        return self.caster_level * self.level_up_factor

    def add_fighter_xp(self, xp):
        self.fighter_xp += xp

        if self.fighter_xp >= self.experience_to_next_fighter_level:
            self.fighter_xp -= self.experience_to_next_fighter_level
            self.fighter_level += 1

            return True
        else:
            return False

    def add_caster_xp(self, xp):
        self.caster_xp += xp

        if self.caster_xp >= self.experience_to_next_caster_level:
            self.caster_xp -= self.experience_to_next_caster_level
            self.caster_level += 1

            return True
        else:
            return False
