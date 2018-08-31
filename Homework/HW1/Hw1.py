import random
CONSTANTS = {
    "GoalState": "123450"
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
        raise Exception("Invalid state to move " + moveDirection)

def MoveLeft(state):
    # TODO: Implement
    ValidateMove(state, [2,5], "left")
    emptySpaceIndex = state.index("0")
    

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

def GetNextState(state, action):
    # action is string representation
    # modify state according to action
    # return modified state
    # TODO: Implement
    if action == "L":
        return MoveLeft(state)
    else if action == "R":
        return MoveRight(state)
    else if action == "U":
        return MoveUp(state)
    else if action == "R":
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
    for currMaxDepth in range(maxDepth):
        solution = GetLimitedDSSolution(startingState,currMaxDepth)

def PrintSolution(startingState, solution):
    # Prints the solution (sequence of moves)
    # TODO: Implement

def Main():
    # generate tests
    for runNumber in range(10):
        numberOfMoves = random.randint(1,10)
        startingState = GetRandomStartingState(CONSTANTS["GoalState"],numberOfMoves)
        solution = GetIDSSolution(startingState)
        PrintSolution(startingState, solution)