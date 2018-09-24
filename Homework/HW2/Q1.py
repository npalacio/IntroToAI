import os
CONSTANTS = {
    "InitialPopulationSize": 10,
    "ChromosomesPerIteration": 2,
    "MutationRate": .3,
    "MaxIterations": 10000,
    "CrossoverOperator": 0
}
def GetAlgorithm():
    algorithm = input("Please specify crossover operator:" + os.linesep + "Single point = 0" + os.linesep + "Two point = 1" + os.linesep + "Cut and splice = 2" + os.linesep + "Uniform = 3" + os.linesep)
    CONSTANTS["CrossoverOperator"] = int(algorithm)
def GetInputs():
    inputs = input("Please provide the following parameters separated by a space: <Initial population size> <Number of chromosomes to select per iteration> <Mutation Rate> <Number of iterations to run for>:" + os.linesep)
    inputs = inputs.split()
    CONSTANTS["InitialPopulationSize"] = int(inputs[0])
    CONSTANTS["ChromosomesPerIteration"] = int(inputs[1])
    CONSTANTS["MutationRate"] = float(inputs[2])
    CONSTANTS["MaxIterations"] = int(inputs[3])
def Main():
    # Prompt user for inputs
    GetInputs()
    GetAlgorithm()
Main()