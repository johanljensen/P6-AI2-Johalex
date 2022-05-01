import operator
import random
from math import floor

import Stats
import Actor


class Evolution():

    def __init__(self):
        print("Evolution initiated")

    def Evolve(self, aiSettings, oldActors, generation):

#Determines how many to keep as elites and how many to replace
        elitismAmount = int(floor(aiSettings.elitism * aiSettings.populationCount))
        newActorCount = aiSettings.populationCount - elitismAmount

#Create stats object for stat tracking
        stats = Stats.Stats()
        for actor in oldActors:
            if actor.fitnessScore > stats.best:
                stats.best = actor.fitnessScore

            if actor.fitnessScore < stats.worst or stats.worst == 0:
                stats.worst = actor.fitnessScore

            stats.sum += actor.fitnessScore
            stats.count += 1
        stats.average = stats.sum / stats.count

#Sort based on the fitnessScore, only time we have to use the attribute name?
        actorsSorted = sorted(oldActors, key=operator.attrgetter('fitnessScore'), reverse=True)
        newActors = []

#Populate the new list of actors with the elitism% best performing actor from last generation
        for i in range(0, elitismAmount):
            newActor = Actor.Actor(aiSettings, actorsSorted[i].name, actorsSorted[i].innerHidden, actorsSorted[i].hiddenOuter)
            newActors.append(newActor)

#Create new actors to refill the rest of the population
        for i in range(0, newActorCount):

#Randomly pick candicates from which to base the new weights on
            candidates = range(0, elitismAmount)
            randomIndex = random.sample(candidates, 2)
            actor1 = actorsSorted[randomIndex[0]]
            actor2 = actorsSorted[randomIndex[1]]

            crossWeight = random.random()
            newInnerHidden = (crossWeight * actor1.innerHidden) + ((1 - crossWeight) * actor2.innerHidden)
            newHiddenOuter = (crossWeight * actor1.hiddenOuter) + ((1 - crossWeight) * actor2.hiddenOuter)

#Random chance for a new actor to randomly change one of the attributes
            mutateRoll = random.random()
            if mutateRoll <= aiSettings.mutateRate:

                attributeToMutate = random.randint(0,1)

                if(attributeToMutate == 0):
                    indexRow = random.randint(0, aiSettings.hiddenNodes -1)
                    newInnerHidden[indexRow] = newInnerHidden[indexRow] * random.uniform(0.9, 1.1)
                    if newInnerHidden[indexRow] > 1:
                        newInnerHidden[indexRow] = 1
                    if newInnerHidden[indexRow] < -1:
                        newInnerHidden[indexRow] = -1

                if (attributeToMutate == 1):
                    indexRow = random.randint(0, aiSettings.outputNodes - 1)
                    indexCol = random.randint(0, aiSettings.hiddenNodes - 1)
                    newHiddenOuter[indexRow][indexCol] = newHiddenOuter[indexRow][indexCol] * random.uniform(0.9, 1.1)
                    if newHiddenOuter[indexRow][indexCol] > 1:
                        newHiddenOuter[indexRow][indexCol] = 1
                    if newHiddenOuter[indexRow][indexCol] < -1:
                        newHiddenOuter[indexRow][indexCol] = -1

            newActor = Actor.Actor(aiSettings, 'gen['+str(generation)+']-actor['+str(i)+']', newInnerHidden, newHiddenOuter)
            newActors.append(newActor)

        return newActors, stats