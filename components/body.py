from components.organs import Organ
from components.organ_states import OrganStates
from game_messages import Message

class Body:
    def __init__(self, body_type, max_blood=100):
        self.organs = [] 
        self.alive = True
        self.animated = True
        self.body_type = body_type
        if body_type == 'anthropod':
            self.blooded = True
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
            self.blooded = True
            self.max_blood = max_blood
            self.blood = max_blood
            self.l_arm = Organ('four left legs')
            self.l_arm.owner = self
            self.r_arm = Organ('four right legs')
            self.r_arm.owner = self
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
            self.organs.extend([self.l_arm, self.r_arm, self.heart, self.brain, self.l_eyes, self.r_eyes, 
                                self.l_ear, self.r_ear, self.stomach, self.lungs, self.liver, self.kidneys])
        elif body_type == 'anthropod_skeleton':
            self.alive = False
            self.blooded = False
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
            self.alive = False
            self.blooded = False
            self.max_blood = 0
            self.blood = max_blood
            self.l_arm = Organ('four left legs')
            self.l_arm.owner = self
            self.r_arm = Organ('four right legs')
            self.r_arm.owner = self
            self.skull = Organ('skull', vital=True)
            self.skull.owner = self
            self.organs.extend([self.l_arm, self.r_arm, self.skull])

    def take_turn(self):
        results = []
        blood_loss = 0
        for i in self.organs:
            if i.state.value > 2:
                blood_loss += i.state.value - 2
        if blood_loss > 0:
            results.append({'message': Message('{0} loses {1} liters of blood.'.format(
                self.owner.name.capitalize(), blood_loss))})
            self.bleed(blood_loss)
        if (self.blooded and self.blood < 1):
            results.append({'message': Message('{0} lost too much blood.'.format(
                self.owner.name.capitalize()))})
            results.append({'dead': self.owner})

        return results

    def bleed(self, amount):
        self.blood -= amount

    def pump_blood(self):
        if self.heart.state == OrganStates.PERFECT:
            amount = 10
        elif self.heart.state == OrganStates.WEAK:
            amount = 7
        elif self.heart.state == OrganStates.BLEEDING:
            amount = 5
        elif self.heart.state == OrganStates.BROKEN:
            amount = 2
        self.blood = min([self.blood + amount, self.max_blood])
        for i in self.organs:
            if i.wound:
                i.wound.repair()

