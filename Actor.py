
import random
from random import uniform
import numpy as np

from math import cos
from math import sin
from math import radians

class Actor:

    def __init__(self, aiSettings, name, innerHidden = None, hiddenOuter = None):
        self.xPos = uniform(aiSettings.xMin, aiSettings.xMax)
        self.yPos = uniform(aiSettings.yMin, aiSettings.yMax)

        self.direction = uniform(0, 360)
        self.velocity = uniform(0, aiSettings.velocityMax)
        self.rotSpeed = random.randint(0, aiSettings.rotateMax)

        self.dist_pickup = 100
        self.angle_pickup = 0
        self.fitnessScore = 0

        self.name = name

        #Default the values if none were provided upon actor creation
        if innerHidden is None or hiddenOuter is None:
            self.innerHidden = np.random.uniform(-1, 1, (aiSettings.hiddenNodes, aiSettings.inputNodes))
            self.hiddenOuter = np.random.uniform(-1, 1, (aiSettings.outputNodes, aiSettings.hiddenNodes))
        else:
            self.innerHidden = innerHidden
            self.hiddenOuter = hiddenOuter

        self.nn_velocity = 0
        self.nn_direction = 0

#EXACT DETAILS NOT UNDERSTOOD, BUT THIS DOES STUFF
    def Think(self):
        # SIMPLE MLP
        #print("InnerHidden and HiddenOuter")
        #print("" + str(self.innerHidden) + " : " + str(self.hiddenOuter))
        af = lambda x: np.tanh(x)  # activation function
        h1 = af(np.dot(self.innerHidden, self.angle_pickup))  # hidden layer
        out = af(np.dot(self.hiddenOuter, h1))  # output layer

        #print("af - h1 - out")
        #print("Direction to food" + str(self.angle_pickup))
        #print("" + str(af) + " : " + str(h1) + " : " + str(out))
        #print("" + str(out) + " : " + str(out[0]) + " : " + str(out[0][0]))
        # UPDATE dv AND dr WITH MLP RESPONSE
        self.nn_velocity = float(out[0])  # [-1, 1]  (accelerate=1, deaccelerate=-1)
        self.nn_direction = float(out[1])  # [-1, 1]  (left=1, right=-1)
        #print("nn_velocity and nn_direction")
        #if abs(self.angle_pickup) > .1:
        #    print("" + str(self.nn_velocity) + " : " + str(self.nn_direction) + " ::: " + str(self.angle_pickup))

    def UpdateDirection(self, aiSettings):
        self.direction += self.nn_direction * aiSettings.rotateMax * aiSettings.timeStepFactor
        #self.direction += self.nn_direction * self.rotSpeed
        self.direction = self.direction % 360

    def UpdateVelocity(self, aiSettings):
        #print("" + str(self.direction) + " : " + str(self.velocity) + " : " + str(self.nn_velocity))
        self.velocity += self.nn_velocity * aiSettings.accelMax * aiSettings.timeStepFactor
        if self.velocity < 0:
            self.velocity = 0
        if self.velocity > aiSettings.velocityMax:
            self.velocity = aiSettings.velocityMax

    def UpdatePosition(self, aiSettings):

        distanceX = self.velocity * cos(radians(self.direction)) * aiSettings.timeStepFactor
        distanceY = self.velocity * sin(radians(self.direction)) * aiSettings.timeStepFactor

        self.xPos += distanceX
        self.yPos += distanceY

        if self.xPos > aiSettings.xMax or self.xPos < aiSettings.xMin:
            self.xPos = max(min(self.xPos, aiSettings.xMax), aiSettings.xMin)

        if self.yPos > aiSettings.yMax or self.yPos < aiSettings.yMin:
            self.yPos = max(min(self.yPos, aiSettings.yMax), aiSettings.yMin)