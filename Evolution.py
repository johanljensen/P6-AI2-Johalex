import operator
import random
from math import floor

import Stats
import Actor


class Evolution():

    def __init__(self):
        print("Evolution initiated")

    def Evolve(self, aiSettings, oldActors, generation):
        print("Evolving generation")

#Determines how many to keep as elites and how many to replace
        elitismAmount = int(floor(aiSettings.elitism * aiSettings.populationCount))
        newActorCount = aiSettings.populationCount - elitismAmount

#Create stats object for stat tracking
        stats = Stats.Stats()
        for actor in oldActors:
            if actor.fitnessScore > stats.best:
                stats.best = actor.fitnessScore
                stats.bestSize = actor.size

            if actor.fitnessScore < stats.worst or stats.worst == -1:
                stats.worst = actor.fitnessScore

            if actor.size > stats.biggest or stats.biggest == -1:
                stats.biggest = actor.size

            if actor.size < stats.smallest or stats.smallest == -1:
                stats.smallest = actor.size

            stats.sum += actor.fitnessScore
            stats.totalSize += actor.size
            stats.count += 1
        stats.average = stats.sum / stats.count
        stats.averageSize = stats.totalSize / stats.count

#Sort based on the fitnessScore, only time we have to use the attribute name?
        actorsSorted = sorted(oldActors, key=operator.attrgetter('fitnessScore'), reverse=True)
        elites = []
        newActors = []

#Populate the new list of actors with the elitism% best performing actor from last generation
        for i in range(0, elitismAmount):
            #newActor = Actor.Actor(aiSettings, actorsSorted[i].name, actorsSorted[i].innerHidden, actorsSorted[i].hiddenOuter)
            #newActors.append(newActor)
            elite = Actor.Actor(aiSettings, actorsSorted[i].name, actorsSorted[i].size, actorsSorted[i].innerHidden, actorsSorted[i].hiddenOuter)
            elites.append(elite)

#Create new actors to refill the rest of the population
        for i in range(0, newActorCount):

#Randomly pick candicates from which to base the new weights on
            candidates = range(0, elitismAmount)
            randomIndex = random.sample(candidates, 2)
            actor1 = actorsSorted[randomIndex[0]]
            actor2 = actorsSorted[randomIndex[1]]
            sortedCandidates = sorted((actor1, actor2), key=operator.attrgetter('fitnessScore'))

            crossWeight = .5 + random.random() / 2
            newInnerHidden = (crossWeight * sortedCandidates[0].innerHidden) + ((1 - crossWeight) * sortedCandidates[1].innerHidden)
            newHiddenOuter = (crossWeight * sortedCandidates[0].hiddenOuter) + ((1 - crossWeight) * sortedCandidates[1].hiddenOuter)

#Randomly manipulate the size in favour of the candidate who performed better
            sizeSortedCandidates = sorted((actor1, actor2), key=operator.attrgetter('size'))
            if actor1.fitnessScore == actor2.fitnessScore:
                newSize = random.uniform(sizeSortedCandidates[0].size - .2, sizeSortedCandidates[1].size + .2)
            else:
                fitSortedCandidates = sorted((actor1, actor2), key=operator.attrgetter('fitnessScore'))
                relativeFitness = fitSortedCandidates[0].fitnessScore / fitSortedCandidates[1].fitnessScore

                #bring all values below 0.5 so the winner always benefits more
                relativeFitness = relativeFitness / 2


                #if the smaller candidate scored the most
                if sizeSortedCandidates[0] == fitSortedCandidates[1]:
                    newSize = random.uniform(sizeSortedCandidates[0].size - 1 + relativeFitness, sizeSortedCandidates[1].size + relativeFitness)
                else:
                    newSize = random.uniform(sizeSortedCandidates[0].size - relativeFitness, sizeSortedCandidates[1].size + 1 - relativeFitness)


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

                newSize = random.uniform(1, 10)

            newActor = Actor.Actor(aiSettings, 'gen['+str(generation)+']-actor['+str(i)+']', newSize, newInnerHidden, newHiddenOuter)
            newActors.append(newActor)

        for i in range(0, elites.__len__()):
            newActors.append(elites[i])
        return newActors, stats