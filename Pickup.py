from random import uniform

class Pickup:

    xPos = 0
    yPos = 0
    fitnessWorth = 0

    def __init__(self, aiSettings):

        self.xPos = uniform(aiSettings.xMin, aiSettings.xMax)
        self.yPos = uniform(aiSettings.yMin, aiSettings.yMax)
        self.fitnessWorth = 1

    def respawn(self, aiSettings):
        self.xPos = uniform(aiSettings.xMin, aiSettings.xMax)
        self.yPos = uniform(aiSettings.yMin, aiSettings.yMax)
