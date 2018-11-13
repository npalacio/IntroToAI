def EvaluatePolicy(rewardDict, utilitiesDict, transitionModel, discountFactor, policies, validCells):
    udpatedUtilities = {}
    for state in utilitiesDict:
        if state not in validCells:
            udpatedUtilities[state] = rewardDict[state]
            continue
        action = policies[state]
        transitions = self.GetTransitionsFromModel(transitionModel, state, action)
        x = GetBellmanPart2(state, rewardDict, utilitiesDict, transitions)
        udpatedUtilities[state] = rewardDict[state] + discountFactor * x
    return udpatedUtilities

# Filter down our frequencies of state-action-state to just this state-action pair
def GetTransitionsFromModel(transitionModel, state, action):
    return [(transition[2], transitionModel[transition]) for transition in transitionModel if transition[0] == state and transition[1] == action]

def GetBellmanPart2(state, rewardDict, utilitiesDict, transitions):
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
            transitions = self.GetTransitionsFromModel(transitionModel, state, action)
            # Since we only care about the action that maximizes the expected utility, 
            # the reward is constant and does not matter
            xArray.append(self.GetBellmanPart2(state, utilitiesDict, transitions))
        maxX = max(xArray)
        policy[state] = actions[xArray.index(maxX)]
    return policy

