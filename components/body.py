from components.organs import Organ

class Body:
    def __init__(self, body_type, max_blood=100):
        self.organs = [] 
        if body_type == 'anthropod':
            self.max_blood = max_blood
            self.blood = max_blood
            self.l_arm = Organ('left arm')
            self.l_arm.owner = self
            self.r_arm = Organ('right arm')
            self.r_arm.owner = self
            self.l_leg = Organ('left leg')
            self.l_leg.owner = self
            self.r_leg = Organ('right leg')
            self.r_leg.owner = self
            self.heart = Organ('heart', vital=True)
            self.heart.owner = self
            self.brain = Organ('brain', vital=True)
            self.brain.owner = self
            self.l_eye = Organ('left eye')
            self.l_eye.owner = self
            self.r_eye = Organ('right eye')
            self.r_eye.owner = self
            self.l_ear = Organ('left ear')
            self.l_ear.owner = self
            self.r_ear = Organ('right ear')
            self.r_ear.owner = self
            self.stomach = Organ('stomach', vital=True)
            self.stomach.owner = self
            self.lungs = Organ('lungs', vital=True)
            self.lungs.owner = self
            self.liver = Organ('liver', vital=True)
            self.liver.owner = self
            self.kidneys = Organ('kindneys')
            self.kidneys.owner = self
            self.organs.extend([self.l_arm, self.r_arm, self.l_leg, self.r_leg, self.heart, self.brain, self.l_eye, self.r_eye, 
                                self.l_ear, self.r_ear, self.stomach, self.lungs, self.liver, self.kidneys])
        elif body_type == 'octopod':
            self.max_blood = max_blood
            self.blood = max_blood
            self.l_legs = Organ('four left legs')
            self.l_legs.owner = self
            self.r_legs = Organ('four right legs')
            self.r_legs.owner = self
            self.heart = Organ('heart', vital=True)
            self.heart.owner = self
            self.brain = Organ('brain', vital=True)
            self.brain.owner = self
            self.l_eyes = Organ('four left eyes')
            self.l_eyes.owner = self
            self.r_eyes = Organ('four right eyes')
            self.r_eyes.owner = self
            self.l_ear = Organ('left ear')
            self.l_ear.owner = self
            self.r_ear = Organ('right ear')
            self.r_ear.owner = self
            self.stomach = Organ('stomach', vital=True)
            self.stomach.owner = self
            self.lungs = Organ('lungs', vital=True)
            self.lungs.owner = self
            self.liver = Organ('liver', vital=True)
            self.liver.owner = self
            self.kidneys = Organ('kindneys')
            self.kidneys.owner = self
            self.organs.extend([self.l_legs, self.r_legs, self.heart, self.brain, self.l_eyes, self.r_eyes, 
                                self.l_ear, self.r_ear, self.stomach, self.lungs, self.liver, self.kidneys])
        elif body_type == 'anthropod_skeleton':
            self.max_blood = 0
            self.blood = max_blood
            self.l_arm = Organ('left arm')
            self.l_arm.owner = self
            self.r_arm = Organ('right arm')
            self.r_arm.owner = self
            self.l_leg = Organ('left leg')
            self.l_leg.owner = self
            self.r_leg = Organ('right leg')
            self.r_leg.owner = self
            self.skull = Organ('skull', vital=True)
            self.skull.owner = self
            self.organs.extend([self.l_arm, self.r_arm, self.l_leg, self.r_leg, self.skull])
        elif body_type == 'octopod_skeleton':
            self.max_blood = 0
            self.blood = max_blood
            self.l_legs = Organ('four left legs')
            self.l_legs.owner = self
            self.r_legs = Organ('four right legs')
            self.r_legs.owner = self
            self.skull = Organ('skull', vital=True)
            self.organs.extend([self.l_legs, self.r_legs, self.skull])

    def take_turn(self):
        for i in self.organs:
            if i.state.value in [3,4]:
                self.bleed(1)
            elif i.state.value == 5:
                self.bleed(3)
        if self.blood > 0:
            self.pump_blood()

    def bleed(self, amount):
        self.blood -= amount

    def pump_blood(self):
        if self.heart.state == 1:
            amount = 10
        elif self.heart.state == 2:
            amount = 5
        elif self.heart.state == 3:
            amount = 3
        elif self.heart.state == 4:
            amount = 1
        elif self.heart.state == 5:
            amount = 0
        self.blood = max([self.blood + amount, self.max_blood])

