from components.limbs import Limb
from components.organs import Organ

class Body:
    def __init__(self):
        l_arm = Limb('left arm')
        l_arm.owner = self
        r_arm = Limb('right arm')
        r_arm.owner = self
        l_leg = Limb('left leg')
        l_leg.owner = self
        r_leg = Limb('right leg')
        r_leg.owner = self
        heart = Organ('heart', vital=True)
        heart.owner = self
        brain = Organ('brain', vital=True)
        brain.owner = self
        l_eye = Organ('left_eye')
        l_eye.owner = self
        r_eye = Organ('right_eye')
        l_eye.owner = self
        l_ear = Organ('left_ear')
        l_ear.owner = self
        r_ear = Organ('right_ear')
        r_ear.owner = self
        stomach = Organ('stomach', vital=True)
        stomach.owner = self
        lungs = Organ('lungs', vital=True)
        lungs.owner = self
        liver = Organ('liver', vital=True)
        liver.owner = self
        kidneys = Organ('kindneys')
        kidneys.owner = self

