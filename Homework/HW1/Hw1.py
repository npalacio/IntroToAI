import random
CONSTANTS = {
    "GoalState": "123450",
    "SuccessorLookup": {
        "0": ["L","U"],
        "1": ["L","R","U"],
        "2": ["R","U"],
        "3": ["L","D"],
        "4": ["L","R","D"],
        "5": ["R","D"]
    }
}

def ValidateMove(state, invalidEmptySpaceIndices, moveDirection):
    emptySpaceIndex = state.index("0")
    if emptySpaceIndex in invalidEmptySpaceIndices:
        raise Exception("Invalid state to move " + moveDirection + ": " + state)

def MoveLeft(state):
    ValidateMove(state, [2,5], "left")
    emptySpaceIndex = state.index("0")
    stateAsList = list(state)
    # If in spot 0, move value in spot 1 to spot 0, "0" to 1
    # If in spot 1, move value in spot 2 to spot 1, "0" to 2
    # If in spot 3, move value in spot 4 to spot 3, "0" to 4
    stateAsList[emptySpaceIndex] = stateAsList[emptySpaceIndex + 1]
    stateAsList[emptySpaceIndex + 1] = "0"
    return "".join(stateAsList)

def MoveRight(state):
    # TODO: Implement
    ValidateMove(state, [0,3], "right")
def MoveUp(state):
    # TODO: Implement
    ValidateMove(state, [3,4,5], "up")
def MoveDown(state):
    # TODO: Implement
    ValidateMove(state, [0,1,2], "down")

def GetRandomStartingState(goalState, numberOfMoves):
    # Start with end state
    # Decide how many moves it should take (random?) = m
    # Perform m random valid moves
    # TODO: Implement
    print("Implement getting random start state")

def GetNextState(state, action):
    # action is string representation
    # modify state according to action
    # return modified state
    # TODO: Implement
    if action == "L":
        return MoveLeft(state)
    elif action == "R":
        return MoveRight(state)
    elif action == "U":
        return MoveUp(state)
    elif action == "R":
        return MoveDown(state)

# Successor and expand function?
def Successor(currState):
    # Returns list of (action,resultState) pairs
    # TODO: Implement
    emptySpaceIndex = currState.index("0")
    availableMoves = CONSTANTS["SuccessorLookup"][str(emptySpaceIndex)]
    successors = []
    for move in availableMoves:
        nextState = GetNextState(currState, move)
        successors.append([move,nextState])
    return successors

def GetLimitedDSSolution(currNode, currDepth, maxDepth, solutionSequence):
    # Take node (state), check if it is goal state
    if currNode["state"] == CONSTANTS["GoalState"]:
        return solutionSequence
    else:
        if currDepth == maxDepth:
            return None
        # Get successors and put on a stack
        successors = Successor(currNode["state"])
        for successor in successors:
            newNode = {
                "state": successor[1]
            }
            solution = GetLimitedDSSolution(newNode, currDepth + 1, maxDepth, solutionSequence + [successor[0]])
            if solution != None:
                return solution
    # If we explored as far as we can with this node without finding a solution, return none
    return None

def GetIterativeDSSolution(startingState, maxDepth):
    # This will actually solve the puzzle using iterative deepening search and return the moves
    # TODO: Implement
    startingNode = {
        "state": startingState
    }
    for currMaxDepth in range(maxDepth):
        solution = GetLimitedDSSolution(startingNode, 0, currMaxDepth, [])

def PrintSolution(startingState, solution):
    # Prints the solution (sequence of moves)
    # TODO: Implement
    print("Implement printing solution")

def Main():
    # generate tests
    for runNumber in range(10):
        numberOfMoves = random.randint(1,10)
        startingState = GetRandomStartingState(CONSTANTS["GoalState"],numberOfMoves)
        solution = GetIDSSolution(startingState)
        PrintSolution(startingState, solution)

print(MoveLeft("123540"))