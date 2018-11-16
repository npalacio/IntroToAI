import random

def EvaluatePolicy(rewardDict, utilitiesDict, transitionModel, discountFactor, policies, validCells):
    udpatedUtilities = {}
    for state in utilitiesDict:
        if state not in validCells:
            udpatedUtilities[state] = rewardDict[state]
            continue
        action = policies[state]
        transitions = GetTransitionsFromModel(transitionModel, state, action)
        x = GetBellmanPart2(state, utilitiesDict, transitions)
        udpatedUtilities[state] = rewardDict[state] + discountFactor * x
    return udpatedUtilities

# Filter down our frequencies of state-action-state to just this state-action pair
def GetTransitionsFromModel(transitionModel, state, action):
    return [(transition[2], transitionModel[transition]) for transition in transitionModel if transition[0] == state and transition[1] == action]

def GetBellmanPart2(state, utilitiesDict, transitions):
    x = []
    for transition in transitions:
        # transition = (resultingState, probability)
        nextState = transition[0]
        x.append(transition[1] * utilitiesDict[nextState])
    return sum(x)

# Try to move given the grid/obstacles
def GetNextState(state, action, gridInfo, validCells):
    newState = state
    if action == 'U':
        if state[1] < gridInfo['height']:
            newState = (state[0], state[1] + 1)
    elif action == 'D':
        if state[1] > 1:
            newState = (state[0], state[1] - 1)
    elif action == 'L':
        if state[0] > 1:
            newState = (state[0] - 1, state[1])
    elif action == 'R':
        if state[0] < gridInfo['width']:
            newState = (state[0] + 1, state[1])
    if newState not in validCells:
        return state
    return newState

# Given our utilities, the transition frequencies we have seen and our grid, calculate the policy
# TODO: Decide if we want to do this or greedy policy
def GetPolicy(utilitiesDict, transitionDict, transitionModel, validCells):
    policy = {}
    for state in utilitiesDict:
        if state not in validCells:
            policy[state] = 'NA'
            continue
        xArray = []
        actions = []
        for action in transitionDict:
            actions.append(action)
            transitions = GetTransitionsFromModel(transitionModel, state, action)
            # Since we only care about the action that maximizes the expected utility, 
            # the reward is constant and does not matter
            xArray.append(GetBellmanPart2(state, utilitiesDict, transitions))
        maxX = max(xArray)
        policy[state] = actions[xArray.index(maxX)]
    return policy

def GetGridCells(gridInfo):
    cells = []
    for col in range(gridInfo['width']):
        for row in range(gridInfo['height']):
            cells.append((col + 1, row + 1))
    return cells

def GetValidGridCells(gridCells, gridInfo):
    terminalCells = [cellObj['cell'] for cellObj in gridInfo['terminalCells']]
    return [cell for cell in gridCells if cell not in gridInfo['obstacles'] and cell not in terminalCells]

def GetGridCellsMinusObstacles(gridCells, gridInfo):
    return [cell for cell in gridCells if cell not in gridInfo['obstacles']]

def GetGreedyPolicy(utilities, validGridCells, gridInfo, gridCellsMinusObstacles, transitionModel):
    policy = {}
    for state in utilities:
        policyAtState = GetPolicyAtState(state, utilities, validGridCells, gridInfo, gridCellsMinusObstacles, transitionModel)
        policy[state] = policyAtState
    return policy

def GetPolicyAtState(state, utilities, validGridCells, gridInfo, gridCellsMinusObstacles, transitionModel):
    if state not in validGridCells:
        return 'NA'
    actionNeighborPairs = GetValidActionNeighborPairs(state, validGridCells, gridInfo, gridCellsMinusObstacles, transitionModel)
    neighborUtils = [utilities[pair["neighbor"]] for pair in actionNeighborPairs]
    maxIndex = neighborUtils.index(max(neighborUtils))
    return actionNeighborPairs[maxIndex]["action"]

def GetValidActionNeighborPairs(state, validGridCells, gridInfo, gridCellsMinusObstacles, transitionModel):
    pairs = []
    for action in transitionModel:
        nextState = GetNextState(state, action, gridInfo, gridCellsMinusObstacles)
        if nextState != state:
            pairs.append({"action": action, "neighbor": nextState})
    return pairs

def GetRandomStartingState(height, width, validStates):
    while True:
        randCol = random.randint(1, width)
        randRow = random.randint(1, height)
        randCell = (randCol,randRow)
        if randCell in validStates:
            return randCell
    raise Exception('should never be hit in getting rand start state')

def InitializeStateDict(states, value):
    startStateCounts = {}
    for state in states:
        startStateCounts[state] = value
    return startStateCounts

def SimulateTransition(state, transitions, gridInfo, validCells):
    randomProbability = random.randint(0,1000) / 1000
    currTransitionValue = 0
    for transition in transitions:
        currTransitionValue += transition['probability']
        if currTransitionValue >= randomProbability:
            return utils.GetNextState(state, transition['action'], gridInfo, validCells)
    raise Exception("transition did not find right one")
