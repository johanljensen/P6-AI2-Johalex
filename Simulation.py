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
        totalTimeSteps = int(aiSettings.generationTime / aiSettings.timeStepFactor)
        for timeStep in range(0, totalTimeSteps, 1):

#All of the pygame draw calls are accessed within this loop
            if aiSettings.showPygame:
                running = True
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        running = False
                if not running:
                    break

                self.drawPygameFrame(actors, pickups, generation, totalTimeSteps, timeStep, screen)
#End of pygame draw

#Detect if any pickups are close enough to collect
            for pickup in pickups:
                for actor in actors:
                    distance = self.GetDistance(pickup.xPos, actor.xPos, pickup.yPos, actor.yPos)

                    if distance <= 0.5 * actor.reach:
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

    def drawPygameFrame(self, actors, pickups, generation, totalTimeSteps, timeStep, screen):

        screen.fill((55,55,55))
        pygame.draw.rect(screen, (0,0,0), [(10,0), (880,580)], 2)

        for actor in actors:
            point = self.GetPoint(actor.xPos, actor.yPos)
            self.drawActor(actor, point[0], point[1], actor.direction, screen)

        for pickup in pickups:
            point = self.GetPoint(pickup.xPos, pickup.yPos)
            self.drawPickup(point[0], point[1], screen)

        textGen = self.font.render(r'Generation: '+str(generation), 1, (0,0,0))
        textTime = self.font.render(r'Timestep: '+str(timeStep), 1, (0,0,0))
        totalTimeStep = self.font.render(r'/'+str(totalTimeSteps), 1, (0,0,0))
        screen.blit(textGen, (20, 555))
        screen.blit(textTime, (180, 555))
        screen.blit(totalTimeStep, (330, 555))
        pygame.display.flip()

    def drawActor(self, actor, xPos, yPos, rotation, screen):
        actorScaler = actor.size / (3 - 2 / actor.size)
        pointA = (-5 * actorScaler, 4 * actorScaler)
        pointB = (-5 * actorScaler, -4 * actorScaler)
        pointC = (7 * actorScaler, 0 * actorScaler)

        pointD = (-5.5 * actorScaler, 4.5 * actorScaler)
        pointE = (-5.5 * actorScaler, -4.5 * actorScaler)
        pointF = (8 * actorScaler, 0 * actorScaler)

        points2 = [pointD, pointE, pointF]
        points2 = [pygame.math.Vector2(p).rotate(rotation) for p in points2]
        points2 = [((xPos, yPos) + p) for p in points2]
        pygame.draw.polygon(screen, (0, 0, 0), points2)

        points = [pointA, pointB, pointC]
        points = [pygame.math.Vector2(p).rotate(rotation) for p in points]
        points = [((xPos,yPos) + p) for p in points]
        pygame.draw.polygon(screen, (155, 0, 0), points)


    def drawPickup(self, xPos, yPos, screen):
        radius = 7
        pygame.draw.circle(screen, (0, 225, 75), (xPos, yPos), radius)
        pygame.draw.circle(screen, (175, 225, 0), (xPos, yPos), radius - 2)

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
        xPlus = 0         #450
        yPlus = 0         #300
        multiplier = 1    #112
        return int(xPos * multiplier + xPlus), int(yPos * multiplier + yPlus)
