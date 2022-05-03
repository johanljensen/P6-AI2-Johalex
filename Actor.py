
import random
from random import uniform
import numpy as np

from math import cos
from math import sin
from math import radians

class Actor:

    def __init__(self, aiSettings, name, size, innerHidden=None, hiddenOuter=None):
        self.xPos = uniform(aiSettings.xMin, aiSettings.xMax)
        self.yPos = uniform(aiSettings.yMin, aiSettings.yMax)

        size = max(min(size, aiSettings.maxSize), aiSettings.minSize)
        self.size = size

        #Adjust these to affect to balance between big and small actors
        self.maxSpeed = 8 - .6 * self.size
        self.accel = 3 - .02 * self.size
        self.rotSpeed = 180 - 10 * self.size
        self.reach = 1 + 2 * self.size

        self.direction = uniform(0, 360)
        self.velocity = self.maxSpeed / 2

        self.dist_pickup = 100
        self.angle_pickup = 0
        self.fitnessScore = 1

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

#Neural Network nodes, affects direction and velocity when turning to face the next pickup
    def Think(self):
        # SIMPLE MLP
        af = lambda x: np.tanh(x)  # activation function
        h1 = af(np.dot(self.innerHidden, self.angle_pickup))  # hidden layer
        out = af(np.dot(self.hiddenOuter, h1))  # output layer

        # UPDATE dv AND dr WITH MLP RESPONSE
        self.nn_velocity = float(out[0])  # [-1, 1]  (accelerate=1, deaccelerate=-1)
        self.nn_direction = float(out[1])  # [-1, 1]  (left=1, right=-1)

    def UpdateDirection(self, aiSettings):
        self.direction += self.nn_direction * self.rotSpeed * aiSettings.timeStepFactor
        self.direction = self.direction % 360

    def UpdateVelocity(self, aiSettings):

        rotateSlowdown = abs(self.nn_velocity)
        self.velocity += self.accel * aiSettings.timeStepFactor - rotateSlowdown / 10
        if self.velocity < 0:
            self.velocity = 0
        if self.velocity > self.maxSpeed:
            self.velocity = self.maxSpeed

    def UpdatePosition(self, aiSettings):

        distanceX = self.velocity * cos(radians(self.direction)) * aiSettings.timeStepFactor
        distanceY = self.velocity * sin(radians(self.direction)) * aiSettings.timeStepFactor

        self.xPos += distanceX
        self.yPos += distanceY

        if self.xPos > aiSettings.xMax or self.xPos < aiSettings.xMin:
            self.xPos = max(min(self.xPos, aiSettings.xMax), aiSettings.xMin)

        if self.yPos > aiSettings.yMax or self.yPos < aiSettings.yMin:
            self.yPos = max(min(self.yPos, aiSettings.yMax), aiSettings.yMin)