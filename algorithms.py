import numpy as np
import random

temp0 = 1000            # start temperature from literature
tempEnd = 0.1           # end temperature
beta = temp0 / 10000    # linear cooling parameter
alpha = 0.95            # geometric cooling parameter
typeReduce = "geo"      # geo/lin/log

class Algorithms():
    def __init__(self, matrixDistances, capacity, numPoints, basePosition):
        self.matrixDistances = matrixDistances
        self.capacity = capacity
        self.numPoints = numPoints
        self.basePosition = basePosition

    # the function that returns the total distance for the given permutation
    def calculateDistance(self, sequence):
        distance = 0
        pointTemp = 0
        for point in sequence:
            distance += self.matrixDistances[pointTemp][point]
            pointTemp = point
        return distance

    # the function that returns the number of the nearest point from the current position
    def minDistancePoint(self, position, freePoints):
        distances = [self.matrixDistances[position][x] for x in freePoints]
        return freePoints[distances.index(min(distances))]

    # the function that returns the number of the farthest point from the current position
    def maxDistancePoint(self, position, freePoints):
        distances = [self.matrixDistances[position][x] for x in freePoints]
        return freePoints[distances.index(max(distances))]

    # greedy algorithm, returns permutation
    def greedyAlg(self):
        freePoints = [x for x in range(self.numPoints) if x != self.basePosition] # available points
        permutation = []                
        tasks = self.capacity     # number of points for one course
        task = 0
        while(len(freePoints) > 0):         # until available points
            permutation.append(self.basePosition)
            nextPoint = self.maxDistancePoint(self.basePosition, freePoints)
            permutation.append(nextPoint)
            freePoints.remove(nextPoint)
            task += 1
            while(tasks > task and len(freePoints) > 0):      # until a point can be added to the course
                nextPoint = self.minDistancePoint(nextPoint, freePoints)
                permutation.append(nextPoint)
                freePoints.remove(nextPoint)
                task += 1
            task = 0
        permutation.append(self.basePosition)
        return permutation

    # the function that swap two points, returns new permutation
    def swap(self, x, y, permutation):
        permutationTemp = permutation.copy()
        i = permutationTemp.index(x)
        j = permutationTemp.index(y)
        permutationTemp[i], permutationTemp[j] = permutationTemp[j], permutationTemp[i]
        return permutationTemp


    # the function that reduces the temperature (linear / geometric / logarithmic)
    def reduceTemp(self, T, iteration, typeReduce):
        temp = 0
        if typeReduce == "lin":
            temp = T - beta
        elif typeReduce == "geo":
            temp = T * alpha
        elif typeReduce == "log":
            T / np.log(iteration + 1)
        return temp

   
    # simulated annealing algorithm, returns tuple (total distance, permutation)
    def simAnnealing(self):
        points = [x for x in range(self.numPoints)]
        t0 = temp0   # start temperature
        tEnd = tempEnd   # end temperature
        permutation = self.greedyAlg()  # initial permutation from the greedy algorithm
        distance = self.calculateDistance(permutation)  # initial distance from the greedy algorithm
        numIter = 1 # iteration number
        while t0 > tEnd:        # until the temperature drops to tEnd
            for i in range(1, self.numPoints):  
                pos1, pos2 = random.sample([x for x in points if x != self.basePosition], 2)   # random points to swap
                #pos1, pos2 = random.sample(points,2)
                newPermutation = self.swap(pos1, pos2, permutation)
                newDistance = self.calculateDistance(newPermutation)
                if newDistance < distance:          # if the cost is better
                    distance = newDistance
                    permutation = newPermutation
                else:
                    probability = random.random()
                    if probability < np.exp((distance - newDistance) / t0):   # with the given probability do the swap as well
                        distance = newDistance
                        permutation = newPermutation
            t0 = self.reduceTemp(t0, numIter, typeReduce)  # reduce temperature
            numIter += 1
        return (distance, permutation)