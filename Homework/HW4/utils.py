def EvaluatePolicy(rewardDict, utilitiesDict, transitionModel, discountFactor, policies, gridInfo):
    udpatedUtilities = {}
    for state in utilitiesDict:
        if state in gridInfo['rewardCells']['cells']:
            udpatedUtilities[state] = rewardDict[state]
            continue
        # x = GetBellmanPart2(state, rewardDict, utilitiesDict, transitionDict[policies[state]])
        action = policies[state]
        x = GetBellmanPart2(state, rewardDict, utilitiesDict, [(transition[2], transitionModel[transition]) for transition in transitionModel if transition[0] == state and transition[1] == action])
        udpatedUtilities[state] = rewardDict[state] + discountFactor * x
    return udpatedUtilities

def GetBellmanPart2(state, rewardDict, utilitiesDict, transitions, gridInfo):
    if state in gridInfo['rewardCells']['cells']:
        return rewardDict[state]
    x = []
    for transition in transitions:
        # transition = (resultingState, probability)
        nextState = transition[0]
        x.append(transition[1] * utilitiesDict[nextState])
    return sum(x)

def GetNextState(state, action, gridInfo):
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
    return newState
