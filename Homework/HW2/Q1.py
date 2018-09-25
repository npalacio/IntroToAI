import os
import heapq

CONSTANTS = {
    "GoalFitness": 28
}

def GetGoalStateChild(options):
    print("Implement GetGoalStateChild")
    # Return none if no goal state children
    # Otherwise return just the child (state)

def CalculateFitnesses(options):
    print("Implement calculate fitnesses")
    # Should return dict of child and their fitness

def Reproduce(options):
    print("Implement get parents")
    # Given a set of parents, reproduce using the crossover operator specified

def GetHorizontalAttackers(options):
    print("Implement GetHorizontalAttackers")

def GetHorizontalAttackers(options):
    print("Implement GetDiagonalAttackers")

def AddChildrenToQueue(options):
    print("Implement AddChildrenToQueue")
    # heapq.heappush(options["population"], (options["childFitness"], popSize + 1, options["child"]))
    # Should return updated list (queue)

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
    # Should mutate a set of children

def GetParents(options):
    print("Implement get parents")
    # Should return n parents probabalistically based on fitness
    # Select n parents based on probabilistic distribution of their fitness functions

def GenerateChildren(options):
    print("Implement generate children")
    parents = GetParents({
        "population": options["population"],
        "chromosomesPerIteration": options["chromosomesPerIteration"]
    })
    children = Reproduce({
        "parents": parents,
        "crossoverOperator": options["crossoverOperator"]
    })
    # How do we use chromosomesPerIteration?
        # How many new children are we generating based on this?
        # Create n chromosomes here, pick top n chromosomes based on fitness function,
        # reproduce by probablistically picking 2 to crossover initially (you replace one of the ones you selected with these 2 children, else )
        # Then crossover the rest of the pairs
    children = Mutate({
        "children": children,
        "mutationRate": mutationRate
    })

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
        children = GenerateChildren({
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