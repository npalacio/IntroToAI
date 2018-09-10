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
        "8": ["R","D"]
    },
    "MaxIterations": 10000
}

def ValidateMove(state, emptySpaceIndex, invalidEmptySpaceIndices, moveDirection):
    if emptySpaceIndex in invalidEmptySpaceIndices:
        PrintState(state)
        raise Exception("Invalid state to move " + moveDirection)

def MoveLeft(state):
    emptySpaceIndex = state.index("0")
    ValidateMove(state, emptySpaceIndex, [2,5,8], "left")
    stateAsList = list(state)
    stateAsList[emptySpaceIndex] = stateAsList[emptySpaceIndex + 1]
    stateAsList[emptySpaceIndex + 1] = "0"
    return "".join(stateAsList)

def MoveRight(state):
    emptySpaceIndex = state.index("0")
    ValidateMove(state, emptySpaceIndex, [0,3,6], "right")
    stateAsList = list(state)
    stateAsList[emptySpaceIndex] = stateAsList[emptySpaceIndex - 1]
    stateAsList[emptySpaceIndex - 1] = "0"
    return "".join(stateAsList)

def MoveUp(state):
    emptySpaceIndex = state.index("0")
    ValidateMove(state, emptySpaceIndex, [6,7,8], "up")
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
def GetCostToGoal(node):
    # Need to calculate Manhattan distance for each tile and sum them up
    total = 0
    for tile in list(node["state"]):
        if tile == "0": 
            continue
        total += GetManhattanDistance(tile, node["state"], CONSTANTS["GoalState"])
    return total

def GetManhattanDistance(tile, state, goalState):
    tileIndex = state.index(tile)
    goalIndex = goalState.index(tile)
    if tileIndex == goalIndex:
        return 0
    horizontalDistance = GetHorizontalDistance(tileIndex, goalIndex)
    verticalDistance = GetVerticalDistance(tileIndex, goalIndex)
    return horizontalDistance + verticalDistance

def GetHorizontalDistance(tileIndex, goalStateIndex):
    return abs((tileIndex % 3) - (goalStateIndex % 3))

def GetVerticalDistance(tileIndex, goalStateIndex):
    return abs((tileIndex // 3) - (goalStateIndex // 3))

def GetSolution(finalNode):
    solution = []
    currNode = finalNode
    while currNode != None:
        if currNode["arrivalAction"] == None:
            return list(reversed(solution))
        solution.append(currNode["arrivalAction"])
        currNode = currNode["parent"]
    return list(reversed(solution))

def GetAStarSolution(startingState):
    # Initialize priority q
    q = []
    # Entry count is used as a tiebreaker for nodes with identical total costs
    entryCount = 0
    iteration = 0
    currNode = Expand(startingState, None, None, 0)
    # Iterate while q is not empty
    while currNode != None and iteration < CONSTANTS["MaxIterations"]:
        # Check if node is goal state
        if currNode["state"] == CONSTANTS["GoalState"]:
            return GetSolution(currNode)
        # Get its children (successors from this state)
        successors = Successor(currNode["state"])
        # Push children on q, maintaining order
        for successor in successors:
            newNode = Expand(successor[1], currNode, successor[0], currNode["depth"] + 1)
            costSoFar = GetCostSoFar(newNode)
            costToGoal = GetCostToGoal(newNode)
            totalCost = costSoFar + costToGoal
            heapq.heappush(q, (totalCost, entryCount, newNode))
            entryCount += 1
        # Dequeue next node
        currNode = heapq.heappop(q)[2]
        iteration += 1

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
    startingState = str(input("Please input starting state: "))
    ValidateState(startingState)
    solution = GetAStarSolution(startingState)
    if solution != None:
        PrintSolution(solution)
    else:
        print("No solution could be found using A* Search with a max depth of " + str(CONSTANTS["MaxIterations"]))

Main()
