import os
import heapq
import random

CONSTANTS = {
    "GoalFitness": 28,
    "LengthOfState": 8,
    "RangeOfStateValues": 8
}

def UniformCrossover(options):
    # Expected params
    parent1AsList = list(options["parent1"])
    parent2AsList = list(options["parent2"])
    
    parent1Fitness = Fitness(options["parent1"])
    parent2Fitness = Fitness(options["parent1"])
    parent1Ratio = parent1Fitness / (parent1Fitness + parent2Fitness)

    child1 = []
    child2 = []
    for i in range(CONSTANTS["LengthOfState"]):
        randomNum = random.randint(0,99999999) / 100000000
        if parent1Ratio > randomNum:
            child1.append(parent1AsList[i])
            child2.append(parent2AsList[i])
        else:
            child1.append(parent2AsList[i])
            child2.append(parent1AsList[i])
    return ["".join(child1),"".join(child2)]


def TwoPointCrossover(options):
    # Expected params
    parent1AsList = list(options["parent1"])
    parent2AsList = list(options["parent2"])
    crossoverPoint1 = random.randint(1, CONSTANTS["RangeOfStateValues"] - 3) #1..6 = 1
    crossoverPoint2 = random.randint(crossoverPoint1 + 1, CONSTANTS["RangeOfStateValues"] - 1) #(cp1+1)..7 = 2
    child1 = parent1AsList[0:crossoverPoint1] + parent2AsList[crossoverPoint1:crossoverPoint2] + parent1AsList[crossoverPoint2:CONSTANTS["RangeOfStateValues"]]
    child2 = parent2AsList[0:crossoverPoint1] + parent1AsList[crossoverPoint1:crossoverPoint2] + parent2AsList[crossoverPoint2:CONSTANTS["RangeOfStateValues"]]
    return ["".join(child1),"".join(child2)]

def SinglePointCrossover(options):
    # Expected params
    parent1AsList = list(options["parent1"])
    parent2AsList = list(options["parent2"])

    crossoverPoint = random.randint(1, CONSTANTS["RangeOfStateValues"] - 1)
    # Child 1 = [0]..(crossoverPoint) = parent1, crossoverPoint..[7] = parent2
    child1 = parent1AsList[0:crossoverPoint] + parent2AsList[crossoverPoint:CONSTANTS["RangeOfStateValues"]]
    # Child 2 = [0]..(crossoverPoint) = parent2, crossoverPoint..[7] = parent1
    child2 = parent2AsList[0:crossoverPoint] + parent1AsList[crossoverPoint:CONSTANTS["RangeOfStateValues"]]

    return ["".join(child1),"".join(child2)]

def ReproduceWithParents(options):
    # Expected params
    parent1 = options["parent1"]
    parent2 = options["parent2"]
    crossoverOperator = options["crossoverOperator"]

    # Should return pair of children as array of strings
    if crossoverOperator == 0:
        return SinglePointCrossover({
            "parent1": parent1,
            "parent2": parent2
        })
    elif crossoverOperator == 1:
        return TwoPointCrossover({
            "parent1": parent1,
            "parent2": parent2
        })
    elif crossoverOperator == 2:
        print("Implement cut and splice crossover")
    elif crossoverOperator == 3:
        return UniformCrossover({
            "parent1": parent1,
            "parent2": parent2
        })

def GetGoalStateChild(options):
    # Expected params
    childrenWithFitness = options["childrenWithFitness"]

    # Return none if no goal state children
    # Otherwise return just the child (state)
    for child in childrenWithFitness:
        if child["fitness"] == CONSTANTS["GoalFitness"]:
            return child["child"]
    return None

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
    # Expected params
    childrenWithFitness = options["childrenWithFitness"]
    population = options["population"]

    # Should return updated list (queue)
    currIndex = len(population)
    for child in childrenWithFitness:
        heapq.heappush(population, (child["fitness"], currIndex, child["child"]))
        currIndex += 1
    return population

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
            newValue = str(random.randint(1,CONSTANTS["RangeOfStateValues"]))
            stateAsList = list(child)
            stateAsList[indexToMutate] = newValue
            newChild = "".join(stateAsList)
        newChildren.append(newChild)
    return newChildren

def GetParentsWithDistribution(options):
    # Expected params
    popWithDistr = options["populationWithDistribution"]
    chromosomesPerIteration = options["chromosomesPerIteration"]

    parents = []

    while len(parents) < chromosomesPerIteration:
        randomNum = random.randint(0,99999999) / 100000000
        currSum = 0
        for i in range(len(popWithDistr)):
            currChild = popWithDistr[i]
            currSum += currChild["distribution"]
            if currSum > randomNum:
                if currChild["child"] not in parents:
                    parents.append(currChild["child"])
                break
    return parents

def GetParentsByDistribution(options):
    # Expected params
    chromosomesPerIteration = options["chromosomesPerIteration"]
    population = options["population"].copy()

    populationWithDistribution = GetChildrenWithDistribution({
        "population": population
    })

    parents = GetParentsWithDistribution({
        "populationWithDistribution": populationWithDistribution,
        "chromosomesPerIteration": chromosomesPerIteration
    })
    return parents

def GetChildrenWithDistribution(options):
    # Expected params
    population = options["population"]
    
    sumOfFitnessValues = sum([x[0] for x in population])
    # Get sum of all fitness values, use this to calculate each ones distribution
    return [{"child": x[2], "distribution": x[0] / sumOfFitnessValues} for x in population]

def GetParents(options):
    # Expected params
    population = options["population"]
    chromosomesPerIteration = options["chromosomesPerIteration"]

    parents = GetParentsByDistribution({
        "population": population,
        "chromosomesPerIteration": chromosomesPerIteration
    })
    # return [parent["child"] for parent in parents]
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

def GetCrossoverOperatorName(crossoverOperator):
    if crossoverOperator == 0:
        return "Single Point"
    elif crossoverOperator == 1:
        return "Two Point"
    elif crossoverOperator == 2:
        return "Cut and splice"
    elif crossoverOperator == 3:
        return "Uniform"

def PrintSolution(options):
    # Expected params
    finalState = options["solution"]["finalState"]
    finalStateFitness = options["solution"]["finalStateFitness"]
    iterations = options["solution"]["iterations"]
    initialPopSize = options["parameters"]["initialPopSize"]
    chromosomesPerIteration = options["parameters"]["chromosomesPerIteration"]
    mutationRate = options["parameters"]["mutationRate"]
    maxIterations = options["parameters"]["maxIterations"]
    crossoverOperator = options["parameters"]["crossoverOperator"]

    print("")
    print("Solution found with the following parameters:")
    parameterString = "Initial Population Size: " + str(initialPopSize)
    parameterString += ", Chromosomes generated per iteration: " + str(chromosomesPerIteration)
    parameterString += ", MutationRate: " + str(mutationRate)
    parameterString += ", Max Iterations: " + str(maxIterations)
    parameterString += ", Crossover operator used: " + GetCrossoverOperatorName(crossoverOperator)
    print(parameterString)

    print("Iterations used: " + str(iterations))
    print("Final State: " + str(finalState))
    print("Final State Fitness: " + str(finalStateFitness))
    print("")

def GetSolution(options):
    # Expected params
    population = options["initialPopulation"]
    chromosomesPerIteration = options["chromosomesPerIteration"]
    crossoverOperator = options["crossoverOperator"]
    maxIterations = options["maxIterations"]
    mutationRate = options["mutationRate"]

    # Should be a priority Q (fitness, dumbCounter, node)
    isIterationLimit = maxIterations != -1
    iterationCount = 0
    # loop either # of iterations or until goal state is reached
    while True:
        # How do I select what 2 states to reproduce with?
        # Get the top 2 from pop based on their fitness function values
        children = GenerateChildren({
            "population": population,
            "chromosomesPerIteration": chromosomesPerIteration,
            "crossoverOperator": crossoverOperator,
            "mutationRate": mutationRate
        })
        childrenWithFitness = CalculateFitnesses({
            "children": children
        })
        # If maxIterations = -1, check if child is goal state and return it if it is
        if isIterationLimit:
            if iterationCount >= maxIterations:
                # We are done iterating, return our best
                finalState = heapq.nlargest(1,population)[0][2]
                # finalState = heapq.heappop(population)[2]
                return {
                    "finalState": finalState,
                    "finalStateFitness": Fitness(finalState),
                    "iterations": iterationCount
                }
        else:
            # Only return when our child is a goal state
            goalStateChild = GetGoalStateChild({
                "childrenWithFitness": childrenWithFitness
            })
            if goalStateChild != None:
                # return goalStateChild
                return {
                    "finalState": goalStateChild,
                    "finalStateFitness": CONSTANTS["GoalFitness"],
                    "iterations": iterationCount
                }
        # Always need to add children to q if we are continuing
        population = AddChildrenToQueue({
            "childrenWithFitness": childrenWithFitness,
            "population": population
        })
        iterationCount += 1

def GetInitialPopulation(options):
    # Expected params
    size = options["initialSize"]

    population = []
    populationSize = 0
    while populationSize < size:
        stateAsList = []
        for i in range(CONSTANTS["LengthOfState"]):
            stateAsList.append(str(random.randint(1,CONSTANTS["RangeOfStateValues"])))
        state = "".join(stateAsList)
        stateFitness = Fitness(state)
        if stateFitness < CONSTANTS["GoalFitness"]:
            heapq.heappush(population, (stateFitness, populationSize, state))
            populationSize += 1
    return population

def Solve(options):
    initialPopSize = options["initialPopulationSize"]

    # Get initial population
    initialPop = GetInitialPopulation({
        "initialSize": initialPopSize
    })

    initialPopSize = len(initialPop)
    # Get solution
    parameters = {
        "initialPopulation": initialPop,
        "chromosomesPerIteration": options["chromosomesPerIteration"],
        "mutationRate": options["mutationRate"],
        "maxIterations": options["maxIterations"],
        "crossoverOperator": options["crossoverOperator"]
    }
    solution = GetSolution(parameters)
    parameters["initialPopSize"] = initialPopSize

    # Print solution
    PrintSolution({
        "solution": solution,
        "parameters": parameters
    })

def GetCrossoverOperator():
    algorithm = int(input(os.linesep + "Please specify crossover operator:" + os.linesep + "Single point = 0" + os.linesep + "Two point = 1" + os.linesep + "Cut and splice = 2" + os.linesep + "Uniform = 3" + os.linesep + "Exit = 4" + os.linesep))
    if algorithm > 4 or algorithm < 0:
        raise Exception("Please enter a valid option")
    return algorithm

def GetInputs():
    inputs = input("Please provide the following parameters separated by a space: <Initial population size> <Number of chromosomes to select per iteration> <Mutation Rate> <Number of iterations to run for>:" + os.linesep)
    inputs = inputs.split()
    initialPopSize = int(inputs[0])
    chromPerIteration = int(inputs[1])
    mutationRate = float(inputs[2])
    if chromPerIteration % 2 != 0:
        raise Exception("Chromosome per iteration value must be even so we have pairs of parents to generate them")
    if initialPopSize < chromPerIteration:
        raise Exception("Initial population size cannot be smaller than the number of chromosomes to generate per iteration")
    if mutationRate > 1:
        raise Exception("Mutation rate must be <1")
    return {
        "initialPopulationSize": initialPopSize,
        "chromosomesPerIteration": chromPerIteration,
        "mutationRate": mutationRate,
        "maxIterations": int(inputs[3])
    }

def Main():
    inputs = GetInputs()
    while True:
        # Prompt user for inputs
        crossoverOperator = GetCrossoverOperator()
        if crossoverOperator == 4:
            break
        Solve({
            "initialPopulationSize": inputs["initialPopulationSize"],
            "chromosomesPerIteration": inputs["chromosomesPerIteration"],
            "mutationRate": inputs["mutationRate"],
            "maxIterations": inputs["maxIterations"],
            "crossoverOperator": crossoverOperator
        })

# Fitness("32752411")
# Fitness("24748552")
# SinglePointCrossover({
#     "parent1": "32543213",
#     "parent2": "31234523"
# })
# UniformCrossover({
#     "parent1": "45798432",
#     "parent2": "98672546"
# })
Main()