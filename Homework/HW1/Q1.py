import os
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
    },
    "MaxDepth": 20
}
VisitedStates = []

def ValidateMove(state, emptySpaceIndex, invalidEmptySpaceIndices, moveDirection):
    if emptySpaceIndex in invalidEmptySpaceIndices:
        PrintState(state)
        raise Exception("Invalid state to move " + moveDirection)

def MoveLeft(state):
    emptySpaceIndex = state.index("0")
    ValidateMove(state, emptySpaceIndex, [2,5], "left")
    stateAsList = list(state)
    stateAsList[emptySpaceIndex] = stateAsList[emptySpaceIndex + 1]
    stateAsList[emptySpaceIndex + 1] = "0"
    return "".join(stateAsList)

def MoveRight(state):
    emptySpaceIndex = state.index("0")
    ValidateMove(state, emptySpaceIndex, [0,3], "right")
    stateAsList = list(state)
    stateAsList[emptySpaceIndex] = stateAsList[emptySpaceIndex - 1]
    stateAsList[emptySpaceIndex - 1] = "0"
    return "".join(stateAsList)

def MoveUp(state):
    emptySpaceIndex = state.index("0")
    ValidateMove(state, emptySpaceIndex, [3,4,5], "up")
    stateAsList = list(state)
    stateAsList[emptySpaceIndex] = stateAsList[emptySpaceIndex + 3]
    stateAsList[emptySpaceIndex + 3] = "0"
    return "".join(stateAsList)

def MoveDown(state):
    emptySpaceIndex = state.index("0")
    ValidateMove(state, emptySpaceIndex, [0,1,2], "down")
    stateAsList = list(state)
    stateAsList[emptySpaceIndex] = stateAsList[emptySpaceIndex - 3]
    stateAsList[emptySpaceIndex - 3] = "0"
    return "".join(stateAsList)

# def GetRandomStartingState(goalState, numberOfMoves):
#     # Start with end state
#     # Decide how many moves it should take (random?) = m
#     # Perform m random valid moves
#     print("Implement getting random start state")
#     moves = []
#     currState = goalState
#     for i in range(numberOfMoves):
#         randomMoveNumber = random.randint(1,4)
#         successors = Successor(currState)
#         randomSuccessor = successors[randomMoveNumber % len(successors)]
#         moves.append(randomSuccessor[0])
#         currState = randomSuccessor[1]
#     return {
#         "state": currState,
#         "solution": list(reversed(moves))
#     }

def GetNextState(state, action):
    if action == "L":
        return MoveLeft(state)
    elif action == "R":
        return MoveRight(state)
    elif action == "U":
        return MoveUp(state)
    elif action == "D":
        return MoveDown(state)

def Successor(currState):
    # Returns list of (action,resultState) pairs
    emptySpaceIndex = currState.index("0")
    availableMoves = CONSTANTS["SuccessorLookup"][str(emptySpaceIndex)]
    successors = []
    for move in availableMoves:
        nextState = GetNextState(currState, move)
        successors.append([move,nextState])
    return successors

def Expand(state):
    return {
        "state": state
    }

def GetLimitedDSSolution(currNode, currDepth, maxDepth, solutionSequence, visitedStates):
    # Take node (state), check if it is goal state
    if currNode["state"] == CONSTANTS["GoalState"]:
        return solutionSequence
    else:
        if currDepth == maxDepth:
            return None
        # Get successors and put on a stack
        successors = Successor(currNode["state"])
        for successor in successors:
            if successor[1] not in visitedStates:
                newNode = Expand(successor[1])
                solution = GetLimitedDSSolution(newNode, currDepth + 1, maxDepth, solutionSequence + [successor[0]], visitedStates + [successor[1]])
                if solution != None:
                    return solution
    # If we explored as far as we can with this node without finding a solution, return none
    return None

def GetIterativeDSSolution(startingState, maxDepth):
    startingNode = Expand(startingState)
    for currMaxDepth in range(maxDepth):
        VisitedStates.append(startingState)
        solution = GetLimitedDSSolution(startingNode, 0, currMaxDepth, [], [])
        if solution != None:
            return solution
        del VisitedStates[:]
    return None

def PrintSolution(solution):
    print("Goal state is: " + CONSTANTS["GoalState"])
    print("Moves: " + "-".join(solution))

def PrintState(state):
    print("State:")
    print(state[:3])
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
    startingState = input("Please input starting state..." + os.linesep)
    ValidateState(startingState)
    solution = GetIterativeDSSolution(startingState, CONSTANTS["MaxDepth"])
    if solution != None:
        PrintSolution(solution)
    else:
        print("No solution could be found using Iterative Deepening Search with a max depth of " + str(CONSTANTS["MaxDepth"]))

Main()