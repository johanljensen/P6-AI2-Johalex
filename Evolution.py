import operator
import random
from math import floor

import Stats
import Actor


class Evolution():

    def __init__(self):
        print("Evolution initiated")

    def Evolve(self, aiSettings, oldActors, generation):

        elitismAmount = int(floor(aiSettings.elitism * aiSettings.populationCount))
        newActorCount = aiSettings.populationCount - elitismAmount

        stats = Stats.Stats()
        for actor in oldActors:
            if actor.fitnessScore > stats.best:
                stats.best = actor.fitnessScore

            if actor.fitnessScore < stats.worst or stats.worst == 0:
                stats.worst = actor.fitnessScore

            stats.sum += actor.fitnessScore
            stats.count += 1
        stats.average = stats.sum / stats.count

        actorsSorted = sorted(oldActors, key=operator.attrgetter('fitnessScore'), reverse=True)
        newActors = []
        for i in range(0, elitismAmount):
            newActor = Actor.Actor(aiSettings, actorsSorted[i].name)
            newActor.SetNodes(aiSettings, actorsSorted[i].innerHidden, actorsSorted[i].hiddenOuter)
            newActors.append(newActor)

        for i in range(0, newActorCount):

            candidates = range(0, elitismAmount)
            randomIndex = random.sample(candidates, 2)
            actor1 = actorsSorted[randomIndex[0]]
            actor2 = actorsSorted[randomIndex[1]]

            crossWeight = random.random()
            newInnerHidden = (crossWeight * actor1.innerHidden) + ((1 - crossWeight) * actor2.innerHidden)
            newHiddenOuter = (crossWeight * actor1.hiddenOuter) + ((1 - crossWeight) * actor2.hiddenOuter)

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

            newActor = Actor.Actor(aiSettings, 'gen['+str(generation)+']-org['+str(i)+']')
            newActor.SetNodes(aiSettings, newInnerHidden, newHiddenOuter)
            newActors.append(newActor)

        return newActors, stats