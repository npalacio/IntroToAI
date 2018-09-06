CONSTANTS = {
    "GoalState": "123456780",
    "SuccessorLookup": {
        "0": ["L","U"],
        "1": ["L","R","U"],
        "2": ["R","U"],
        "3": ["L","U","D"],
        "4": ["L","R","U","D"],
        "5": ["R","U","D"],
        "6": ["L","D"],
        "7": ["L","R","D"],
        "8": ["L","R"]
    }
}

def PrintSolution(solution):
    print("Goal state is " + CONSTANTS["GoalState"])
    print("Solution: " + "-".join(solution))

def PrintState(state):
    print("State:")
    print(state[:3])
    print(state[3:6])
    print(state[-3:])

def ValidateState(state):
    stateAsList = list(state)
    goalStateAsList = list(CONSTANTS["GoalState"])
    if len(stateAsList) != len(goalStateAsList):
        raise Exception("Invalid state length")
    for value in stateAsList:
        if value not in goalStateAsList:
            raise Exception("Invalid character in state: " + value)


def Main():
    startingState = input("Please input starting state: ")
    ValidateState(startingState)
    solution = GetAStarSolution(startingState, CONSTANTS["MaxDepth"])
    if solution != None:
        PrintSolution(solution)
    else:
        print("No solution could be found using Iterative Deepening Search with a max depth of " + str(CONSTANTS["MaxDepth"]))
