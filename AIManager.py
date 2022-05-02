import random

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

    def CreateNewPickups(self):
        self.pickups = []
        for i in range(0, self.aiSettings.pickupCount):
            newPickup = Pickup.Pickup(self.aiSettings)
            self.pickups.append(newPickup)

    def CreateNewActors(self):
        self.actors = []
        for i in range(0, self.aiSettings.populationCount):
            newActor = Actor.Actor(self.aiSettings, "Actor: " + str(i), random.uniform(8, 10))
            self.actors.append(newActor)

#Runs the simulation of generations and the evolutions in between
    def RunLoop(self):

        simulation = Simulation.Simulation()
        evolution = Evolution.Evolution()

        self.CreateNewActors()

        for generation in range(0, self.aiSettings.generationCount):

            print()
            print('Generation: ',generation)

            self.CreateNewPickups()

            self.actors = simulation.RunSimulation(self.aiSettings, self.actors, self.pickups, generation, self.pygameScreen)
            self.actors, stats = evolution.Evolve(self.aiSettings, self.actors, generation)

            print('Fitness - BEST: ',stats.best,' WORST: ',stats.worst)
            print('Score - SUM: ',stats.sum,' AVG:',stats.average)
            print('Sizes - BIG: ',stats.biggest,' SMALL ',stats.smallest)
            print('Best Size: ',stats.bestSize)
            print('Average Size: ',stats.averageSize)
        pass

AIManager().StartAI()