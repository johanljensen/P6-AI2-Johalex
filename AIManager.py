import pygame

import Actor
import Pickup
import AISettings
import Simulation
import Evolution


class AIManager:

    def __init__(self):
        self.pygameScreen = None
        self.aiSettings = AISettings.AISettings()

        self.pickups = []
        self.actors = []

#Entry point of the AI simulation
    def StartAI(self):
        self.SetupLoop()
        self.RunLoop()

#Initiates pygame, pickups and actors
    def SetupLoop(self):

        if self.aiSettings.showPygame:
            pygame.init()
            self.pygameScreen = pygame.display.set_mode([900,600])

        for i in range(0, self.aiSettings.pickupCount):
            newPickup = Pickup.Pickup(self.aiSettings)
            self.pickups.append(newPickup)

        for i in range(0, self.aiSettings.populationCount):
            newActor = Actor.Actor(self.aiSettings, "Actor")
            self.actors.append(newActor)

#Runs the simulation of generations and the evolutions in between
    def RunLoop(self):

        simulation = Simulation.Simulation()
        evolution = Evolution.Evolution()

        for generation in range(0, self.aiSettings.generationCount):

            self.actors = simulation.RunSimulation(self.aiSettings, self.actors, self.pickups, generation, self.pygameScreen)
            self.actors, stats = evolution.Evolve(self.aiSettings, self.actors, generation)

            print('Gen:',generation,'BEST:',stats.best,'AVG:',stats.average,'WORST:',stats.worst)
        pass
