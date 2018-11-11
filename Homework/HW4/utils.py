def EvaluatePolicy(rewardDict, utilitiesDict, transitionDict, discountFactor, policies, gridInfo):
    udpatedUtilities = {}
    for state in utilitiesDict:
        if state in gridInfo['rewardCells']['cells']:
            udpatedUtilities[state] = rewardDict[state]
            continue
        x = GetBellmanPart2(state, rewardDict, utilitiesDict, transitionDict[policies[state]])
        udpatedUtilities[state] = rewardDict[state] + discountFactor * x
    return udpatedUtilities

def GetBellmanPart2(state, rewardDict, expectedRewardDict, transitions, gridInfo):
    if state in gridInfo['rewardCells']['cells']:
        return rewardDict[state]
    x = []
    for transition in transitions:
        nextState = GetNextState(state, transition['action'])
        x.append(transition['probability'] * expectedRewardDict[nextState])
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
