from components.organs import Organ

class Body:
    def __init__(self):
        self.organs = [] 
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
        self.l_eye = Organ('left_eye')
        self.l_eye.owner = self
        self.r_eye = Organ('right_eye')
        self.r_eye.owner = self
        self.l_ear = Organ('left_ear')
        self.l_ear.owner = self
        self.r_ear = Organ('right_ear')
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

