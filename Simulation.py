import pygame.event
import pygame

from math import cos
from math import sin
from math import radians
from math import sqrt
from math import degrees
from math import atan2

class Simulation:

    def __init__(self):
        self.font = pygame.font.Font(None, 30)
        print("Simulation initiated")

    def RunSimulation(self, aiSettings, actors, pickups, generation, screen):
        print("Simulating generation")

#Lower timeStepFactor = smaller timeSteps = slower simulation time = more observable
        timeSteps = int(aiSettings.generationTime / aiSettings.timeStepFactor)
        for timeStep in range(0, timeSteps, 1):

#All of the pygame draw calls are accessed within this loop
            if aiSettings.showPygame:
                running = True
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        running = False
                if not running:
                    break

                self.drawPygameFrame(actors, pickups, generation, timeStep, screen)
#End of pygame draw

#Detect if any pickups are close enough to collect
            for pickup in pickups:
                for actor in actors:
                    distance = self.GetDistance(pickup.xPos, actor.xPos, pickup.yPos, actor.yPos)

                    if distance <= 0.5:
                        actor.fitnessScore += pickup.fitnessWorth
                        pickup.respawn(aiSettings)

                    actor.dist_pickup = 10000

#Detect distance and angle to closest pickup
            for pickup in pickups:
                for actor in actors:
                    distance = self.GetDistance(pickup.xPos, actor.xPos, pickup.yPos, actor.yPos)

                    if distance < actor.dist_pickup:
                        actor.dist_pickup = distance
                        actor.angle_pickup = self.GetAngle(actor, pickup)

            for actor in actors:
                actor.Think()

            for actor in actors:
                actor.UpdateDirection(aiSettings)
                actor.UpdateVelocity(aiSettings)
                actor.UpdatePosition(aiSettings)

        return actors

    def drawPygameFrame(self, actors, pickups, generation, timeStep, screen):

        screen.fill((255,255,255))
        pygame.draw.rect(screen, (0,0,0), [(175,25), (550,550)], 2)

        for actor in actors:
            point = self.GetPoint(actor.xPos, actor.yPos)
            self.drawActor(point[0], point[1], actor.direction, screen)

        for pickup in pickups:
            point = self.GetPoint(pickup.xPos, pickup.yPos)
            self.drawPickup(point[0], point[1], screen)

        textGen = self.font.render(r'Generation: '+str(generation), 1, (0,0,0))
        textTime = self.font.render(r'Timestep: '+str(timeStep), 1, (0,0,0))
        screen.blit(textGen, (80, 75))
        screen.blit(textTime, (80, 150))
        pygame.display.flip()

    def drawActor(self, xPos, yPos, rotation, screen):
        radius = 10
        pygame.draw.circle(screen, (0, 100, 0), (xPos, yPos), radius)
        pygame.draw.circle(screen, (144, 238, 144), (xPos, yPos), radius - 3)

        tailLength = 12
        xPos2 = cos(radians(rotation)) * tailLength + xPos
        yPos2 = sin(radians(rotation)) * tailLength + yPos
        pygame.draw.line(screen, (0, 100, 0), (xPos, yPos), (xPos2, yPos2), 2)

    def drawPickup(self, xPos, yPos, screen):
        radius = 7
        pygame.draw.circle(screen, (72, 61, 139), (xPos, yPos), radius)
        pygame.draw.circle(screen, (123, 104, 238), (xPos, yPos), radius - 3)

    def GetDistance(self, xPos1, xPos2, yPos1, yPos2):
        return sqrt((xPos1-xPos2)**2 + (yPos1-yPos2)**2)

    def GetAngle(self, actor, pickup):
        distance_x = pickup.xPos - actor.xPos
        distance_y = pickup.yPos - actor.yPos
        rotation = degrees(atan2(distance_y, distance_x)) - actor.direction
        if abs(rotation) > 180:
            rotation += 360
        return rotation / 180

#Modifies the positioning of all the pygame drawn stuff
    def GetPoint(self, xPos, yPos):
        xPlus = 300         #450
        yPlus = 100         #300
        multiplier = 4    #112
        return int(xPos * multiplier + xPlus), int(yPos * multiplier + yPlus)
