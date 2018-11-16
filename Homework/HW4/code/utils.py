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
            return GetNextState(state, transition['action'], gridInfo, validCells)
    raise Exception("transition did not find right one")

def GetAvailableTTTActions(state):
    return [index for index in range(len(state)) if state[index] == 0]

def GetTTTWinningIndexArrays():
    winningIndexArrays = [[0,4,8],[2,4,6],[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8]]
    return winningIndexArrays

def GetTTTWinner(terminalState):
    # Get arrays of all indices that would need to be x for player x to win
    winningIndexArrays = GetTTTWinningIndexArrays()
    for indexArray in winningIndexArrays:
        player1Arr = [index for index in indexArray if terminalState[index] == 1]
        player1Wins = len(player1Arr) == 3
        player2Arr = [index for index in indexArray if terminalState[index] == 2]
        player2Wins = len(player2Arr) == 3
        if player1Wins and player2Wins:
            raise Exception("Both players cannot win")
        elif player1Wins:
            return 1
        elif player2Wins:
            return 2
    # If neither player matched to a winning array
    return None

def IsTerminalTTTState(state):
    allCellsFilled = 0 not in state
    winnerExists = GetTTTWinner(state) != None
    isTerminal = allCellsFilled or winnerExists
    return isTerminal

def GetTTTStartingState():
    return [0 for i in range(9)]

def SimulateActionByPlayer(state, action, player):
    newState = list(state)
    newState[action] = player
    # TODO: Simulate other player's action as well if not a terminal state?
    return tuple(newState)

def GetNextTTTAction(state, Q):
    # pick action a that maximizes Q(s,a)
    availableActions = GetAvailableTTTActions(state)
    qValues = GetQValues(state, availableActions, Q)
    maxIndex = qValues.index(max(qValues))
    return availableActions[maxIndex]

def GetQValues(state, actions, Q):
    qValues = []
    for action in actions:
        qValues.append(GetQValue(state, action, Q))
    return qValues

def GetQValue(state, action, Q):
    state = tuple(state)
    if (state,action) in Q:
        return Q[(state,action)]
    else:
        return 0

