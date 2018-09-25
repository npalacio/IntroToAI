import os
import heapq
import random

CONSTANTS = {
    "GoalFitness": 28,
    "LengthOfState": 8,
    "RangeOfStateValues": 8
}

def ReproduceWithParents(options):
    # Expected params
    crossoverOperator = options["crossoverOperator"]

    # Should return pair of children as array of strings
    if crossoverOperator == 0:
        print("Implement singlePoint crossover")
    elif crossoverOperator == 1:
        print("Implement twpoPoint crossover")
    elif crossoverOperator == 2:
        print("Implement cut and splice crossover")
    elif crossoverOperator == 3:
        print("Implement uniform crossover")

def GetGoalStateChild(options):
    print("Implement GetGoalStateChild")
    # Return none if no goal state children
    # Otherwise return just the child (state)

def CalculateFitnesses(options):
    # Expected params
    children = options["children"] #Array of strings

    childrenWithFitness = []
    for child in children:
        fitness = Fitness(child)
        childrenWithFitness.append({
            "child": child,
            "fitness": fitness
        })
    return childrenWithFitness

def Reproduce(options):
    # Expected params
    parents = options["parents"]
    crossoverOperator = options["crossoverOperator"]

    # Given a set of parents, reproduce using the crossover operator specified
    # For each pair of parents create pair of kids using specified crossover operator
    newChildren = []
    numberOfPairs = int(len(parents) / 2)
    for i in range(numberOfPairs):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        offspringPair = ReproduceWithParents({
            "parent1": parent1,
            "parent2": parent2,
            "crossoverOperator": crossoverOperator
        })
        newChildren.append(offspringPair[0])
        newChildren.append(offspringPair[1])
    return newChildren

def GetHorizontalAttackers(options):
    # Expected params
    slicedState = options["slicedState"]

    attackers = 0
    currValue = slicedState[0]
    valuesToCheck = slicedState[1:]
    for value in valuesToCheck:
        # Queens on same row can attack eachother horizontally
        if value == currValue:
            attackers += 1
    return attackers

def GetDiagonalAttackers(options):
    # Expected params
    slicedState = options["slicedState"]

    # If the value to the right of you by n moves is equal to (you +- n), it is a diagonal attacker
    attackers = 0
    sliceLength = len(slicedState)
    # for i in range(sliceLength):
    currValue = int(slicedState[0])
    for k in range(sliceLength - 1):
        nextIndex = k + 1
        nextValue = int(slicedState[nextIndex])
        if nextValue == (currValue + (nextIndex)) or nextValue == (currValue - (nextIndex)):
            attackers += 1
    return attackers


def AddChildrenToQueue(options):
    print("Implement AddChildrenToQueue")
    # heapq.heappush(options["population"], (options["childFitness"], popSize + 1, options["child"]))
    # Should return updated list (queue)

def Fitness(state):
    stateAsList = list(state)
    horAttackingPairs = 0
    diaAttackingPairs = 0
    # Dont need to check the last value (all attacking previous values would have already paired up with it)
    for i in range(len(stateAsList) - 1):
        slicedState = stateAsList[i:]
        # Check if any queens horizontal
        horAttackingPairs += GetHorizontalAttackers({
            "slicedState": slicedState,
        })
        # Check if any queens diagonal
        diaAttackingPairs += GetDiagonalAttackers({
            "slicedState": slicedState,
        })
    return CONSTANTS["GoalFitness"] - (horAttackingPairs + diaAttackingPairs)

def Mutate(options):
    # Expected params
    children = options["children"]
    mutationRate = options["mutationRate"]

    # Children should just be array of strings (states)
    newChildren = []
    for child in children:
        newChild = child
        randomNum = random.randint(0,100000) / 100000
        if mutationRate > randomNum:
            # Randomly change one of its values
            indexToMutate = random.randint(0,CONSTANTS["LengthOfState"] - 1)
            newValue = str(random.randint(0,CONSTANTS["RangeOfStateValues"] - 1))
            stateAsList = list(child)
            stateAsList[indexToMutate] = newValue
            newChild = "".join(stateAsList)
        newChildren.append(newChild)
    return newChildren

    # Should mutate a set of children and return new list

def GetParentByDistribution(options):
    # Expected params
    popWithDistr = options["populationWithDistribution"]

    randomNum = random.randint(0,100000) / 100000
    # Could I keep adding up the children percentages until I go higher than the random number?
    currSum = 0
    for child in popWithDistr:
        currChild = child["child"]
        currSum += child["distribution"]
        if currSum > randomNum:
            return currChild

def GetParentsByDistribution(options):
    # Expected params
    chromosomesPerIteration = options["chromosomesPerIteration"]
    popWithDistr = options["populationWithDistribution"]

    parents = []
    for i in range(chromosomesPerIteration):
        parents.append(GetParentByDistribution({
            "populationWithDistribution": popWithDistr
        }))
    return parents

def GetParents(options):
    # Expected params
    population = options["population"]
    chromosomesPerIteration = options["chromosomesPerIteration"]

    # Should return n parents probabalistically based on fitness
    # Select n parents based on probabilistic distribution of their fitness functions
    sumOfFitnessValues = sum([x[0] for x in population])
    # Get sum of all fitness values, use this to calculate each ones distribution
    populationWithDistribution = [{"child": x["2"], "distribution": x[0] / sumOfFitnessValues} for x in population]
    parents = GetParentsByDistribution({
        "populationWithDistribution": populationWithDistribution,
        "chromosomesPerIteration": chromosomesPerIteration
    })
    return parents

def GenerateChildren(options):
    # Expected params
    population = options["population"]
    chromosomesPerIteration = options["chromosomesPerIteration"]
    crossoverOperator = options["crossoverOperator"]
    mutationRate = options["mutationRate"]

    parents = GetParents({
        "population": population,
        "chromosomesPerIteration": chromosomesPerIteration
    })
    children = Reproduce({
        "parents": parents,
        "crossoverOperator": crossoverOperator
    })
    children = Mutate({
        "children": children,
        "mutationRate": mutationRate
    })
    return children

def PrintSolution(options):
    print("Implement print solution")

def GetSolution(options):
    # Expected params
    population = options["initialPopulation"]
    chromosomesPerIteration = options["chromosomesPerIteration"]
    crossoverOperator = options["crossoverOperator"]
    maxIterations = options["maxIterations"]

    # Should be a priority Q (fitness, dumbCounter, node)
    isIterationLimit = maxIterations != -1
    iterationCount = 0
    # loop either # of iterations or until goal state is reached
    while true:
        # How do I select what 2 states to reproduce with?
        # Get the top 2 from pop based on their fitness function values
        children = GenerateChildren({
            "population": population,
            "chromosomesPerIteration": chromosomesPerIteration,
            "crossoverOperator": crossoverOperator,
            "mutationRate": mutationRate
        })
        # If maxIterations = -1, check if child is goal state and return it if it is
        if isIterationLimit:
            if iterationCount >= maxIterations:
                # We are done iterating, return our best
                return heapq.heappop(population)[2]
            iterationCount += 1
        else:
            # Only return when our child is a goal state
            childrenWithFitness = CalculateFitnesses({
                "children": children
            })
            goalStateChild = GetGoalStateChild({
                "childrenWithFitness": childrenWithFitness
            })
            if goalStateChild != None:
                return goalStateChild
            else:
                # Add child to q
                population = AddChildrenToQueue({
                    "childrenWithFitness": childrenWithFitness,
                    "population": population
                })

def GetInitialPopulation(options):
    # TODO: Make sure that no one in initial pop is goal state
    print("Implement get initial pop")

def Solve(options):
    # Get initial population
    initialPop = GetInitialPopulation({
        "initialSize": options["initialPopulationSize"]
    })

    # Get solution
    solution = GetSolution({
        "initialPopulation": initialPop,
        "chromosomesPerIteration": options["chromosomesPerIteration"],
        "mutationRate": options["mutationRate"],
        "maxIterations": options["maxIterations"],
        "crossoverOperator": options["crossoverOperator"]
    })

    # Print solution
    PrintSolution({
        "solution": solution
    })

def GetAlgorithm():
    algorithm = input("Please specify crossover operator:" + os.linesep + "Single point = 0" + os.linesep + "Two point = 1" + os.linesep + "Cut and splice = 2" + os.linesep + "Uniform = 3" + os.linesep)
    return int(algorithm)

def GetInputs():
    # TODO: chromosomesPerIteration needs to be even
    # TODO: mutation rate must be <1
    inputs = input("Please provide the following parameters separated by a space: <Initial population size> <Number of chromosomes to select per iteration> <Mutation Rate> <Number of iterations to run for>:" + os.linesep)
    inputs = inputs.split()
    return {
        "initialPopulationSize": int(inputs[0]),
        "chromosomesPerIteration": int(inputs[1]),
        "mutationRate": float(inputs[2]),
        "maxIterations": int(inputs[3])
    }

def Main():
    # Prompt user for inputs
    inputs = GetInputs()
    crossoverOperator = GetCrossoverOperator()
    Solve({
        "initialPopulationSize": inputs["initialPopulationSize"],
        "chromosomesPerIteration": inputs["chromosomesPerIteration"],
        "mutationRate": inputs["mutationRate"],
        "maxIterations": inputs["maxIterations"],
        "crossoverOperator": crossoverOperator
    })

# Fitness("32752411")
# Fitness("24748552")
