import os
import heapq

CONSTANTS = {
    "GoalFitness": 28
}

def GetHorizontalAttackers(options):
    print("Implement GetHorizontalAttackers")

def GetHorizontalAttackers(options):
    print("Implement GetDiagonalAttackers")

def AddToQueue(options):
    popSize = len(options["population"])
    heapq.heappush(options["population"], (options["childFitness"], popSize + 1, options["child"]))
    # Should return updated list (queue)
    return options["population"]

def Fitness(state):
    stateAsList = list(state)
    attackingPairs = 0
    for i in range(len(stateAsList))
        # Check if any queens horizontal
        attackingPairs += GetHorizontalAttackers({
            "index": i,
            "stateAsList": stateAsList
        })
        # Check if any queens diagonal
        attackingPairs += GetDiagonalAttackers({
            "index": i,
            "stateAsList": stateAsList
        })
    return CONSTANTS["GoalFitness"] - attackingPairs

def Mutate(options):
    print("Implement Mutate")

def GetChild(options):
    print("Implement get child")
    # How do we use chromosomesPerIteration?
        # How many new children are we generating based on this?
    # parent1 = GetNextParent({
    #     "population": population
    # })
    # parent2 = GetNextParent({
    #     "population": population
    # })
    # child = Mutate({
    #     "child": child,
    #     "mutationRate": mutationRate
    # })

# def GetNextParent(options):
#     return heapq.heappop(options["population"])[2]

def PrintSolution(options):
    print("Implement print solution")

def GetSolution(options):
    # Should be a priority Q (fitness, dumbCounter, node)
    population = options["initialPopulation"]
    isIterationLimit = options["maxIterations"] != -1
    iterationCount = 0
    # loop either # of iterations or until goal state is reached
    while true:
        # How do I select what 2 states to reproduce with?
        # Get the top 2 from pop based on their fitness function values
        child = GetChild({
            "population": population,
            "chromosomesPerIteration": options["chromosomesPerIteration"],
            "crossoverOperator": options["crossoverOperator"],
            "mutationRate": mutationRate
        })
        # If maxIterations = -1, check if child is goal state and return it if it is
        if isIterationLimit:
            if iterationCount >= options["maxIterations"]:
                # We are done iterating, return our best
                return heapq.heappop(population)[2]
            iterationCount += 1
        else:
            # Only return when our child is a goal state
            childFitness = Fitness(child)
            if childFitness >= CONSTANTS["GoalFitness"]:
                return child
            else:
                # Add child to q
                population = AddToQueue({
                    "child": child,
                    "childFitness": childFitness,
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

Main()