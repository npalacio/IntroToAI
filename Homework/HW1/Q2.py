import heapq
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

def Successor(currState):
    print("Implement")
    # Returns list of (action,resultState) pairs
    emptySpaceIndex = currState.index("0")
    availableMoves = CONSTANTS["SuccessorLookup"][str(emptySpaceIndex)]
    successors = []
    for move in availableMoves:
        nextState = GetNextState(currState, move)
        successors.append([move,nextState])
    return successors

def Expand(state, parent, arrivalAction, depth):
    return {
        "state": state,
        "parent": parent,
        "depth": depth,
        "arrivalAction": arrivalAction
    }

# Step cost so far
def GetCostSoFar(node):
    return node["depth"]

# Heuristic function
def GetCostToGoal(state):
    # Calculate how many tiles are not in correct place (exclude 0 tile)
    numberOutOfPlace = 0
    goalState = list(CONSTANTS["GoalState"])
    currState = list(state)
    for i in range(len(goalState)):
        if goalState[i] != "0" and goalState[i] != currState[i]:
            numberOutOfPlace += 1
    return numberOutOfPlace

def GetAStarSolution(startingState):
    # Initialize priority q
    q = []
    entryCount = 0
    startingNode = Expand(startingState, None, None, 0)
    heapq.heappush(q,(0, entryCount, startingNode))
    entryCount += 1
    currNode = heapq.heappop(q)
    # Iterate while q is not empty
    while currNode != None:
        # Dequeue node, get its children (successors from this state)
        # Will each child need to keep track of its parent as well as the action that generated itself? 
        # Then at end when we have reached our goal node we can back track to get its ancestry (i.e. solution)?
        successors = Successor(currNode["state"])
        # Push children on q, maintaining order
        for successor in successors:
            newNode = Expand(successor[1], currNode, successor[0], currNode["depth"] + 1)
            costSoFar = GetCostSoFar(newNode)
            costToGoal = GetCostToGoal(newNode)

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
    solution = GetAStarSolution(startingState)
    if solution != None:
        PrintSolution(solution)
    else:
        print("No solution could be found using Iterative Deepening Search with a max depth of " + str(CONSTANTS["MaxDepth"]))
