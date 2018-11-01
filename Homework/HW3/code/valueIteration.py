# Input: the grid of states, actions at each state (u/d/l/r), transition function (prob of actually going up when selecting u)
    # rewards at each state, discount factor?

class ValueIterationAlgorithm:
    def __init__(self, rewardDict, transitionDict, discountFactor, gridInfo):
        # self.actions = actions
        self.rewardDict = rewardDict
            # {(1,1): -.04}
        self.transitionDict = transitionDict
            # {'U': [[.8,'U'],[.1,'L'],[.1,'R']]}
            # {'U': [{'probability': .8, 'action': 'U'},{'probability': .1, 'action': 'L'}]}
        self.discountFactor = discountFactor
        self.gridInfo = gridInfo
        self.epsilon = float('1E-3')

    def Run(self):
        done = False
        expectedRewardDict = self.GetInitialExpectedRewardDict(self.rewardDict)
        utilChangeLimit = self.GetUtilChangeLimit(self.discountFactor)
        while not done:
            maxUtilityChange = 0
            newExpectedRewardDict = {}
            for state in self.rewardDict:
                newExpectedRewardDict[state] = self.GetExpectedReward(state, expectedRewardDict, self.rewardDict[state], self.transitionDict, self.discountFactor)
                if abs(newExpectedRewardDict[state] - expectedRewardDict[state]) > maxUtilityChange:
                    maxUtilityChange = abs(newExpectedRewardDict[state] - expectedRewardDict[state])
            expectedRewardDict = newExpectedRewardDict.copy()
            if maxUtilityChange < utilChangeLimit: 
                done = True
        policy = self.GetPolicy(expectedRewardDict, self.rewardDict, self.transitionDict)
        return {
            'expectedRewardDict': expectedRewardDict,
            'policy': policy
        }

    def GetPolicy(self, expectedRewardDict, rewardDict, transitionDict):
        policy = {}
        for state in expectedRewardDict:
            if state in self.gridInfo['rewardCells']['cells']:
                policy[state] = 'NA'
                continue
            xArray = []
            actions = []
            for action in transitionDict:
                actions.append(action)
                xArray.append(self.GetX(state, expectedRewardDict, transitionDict[action]))
            maxX = max(xArray)
            policy[state] = actions[xArray.index(maxX)]
        return policy

    def GetUtilChangeLimit(self, discountFactor):
        # TODO: Figure out terminal state
        # return float('2.22E-17')
        return self.epsilon * (1 - discountFactor) / discountFactor

    def GetInitialExpectedRewardDict(self, rewardDict):
        expectedRewardDict = {}
        # [expectedRewardDict[state] = 0 for state in rewardDict]
        for state in rewardDict:
            expectedRewardDict[state] = 0
        return expectedRewardDict

    def GetExpectedReward(self, state, expectedRewardDict, reward, transitionDict, discountFactor):
        if state in self.gridInfo['rewardCells']['cells']:
            return reward
        xArray = [self.GetX(state, expectedRewardDict, transitionDict[action]) for action in transitionDict]
        maxX = max(xArray)
        return reward + discountFactor * maxX
    
    def GetX(self, state, expectedRewardDict, transitions):
        # x = sum([ for transition in transitions])
        x = []
        for transition in transitions:
            nextState = self.GetNextState(state, transition['action'])
            x.append(transition['probability'] * expectedRewardDict[nextState])
        return sum(x)

    def GetNextState(self, state, action):
        newState = state
        if action == 'U':
            if state[1] < self.gridInfo['height']:
                newState = (state[0], state[1] + 1)
        elif action == 'D':
            if state[1] > 1:
                newState = (state[0], state[1] - 1)
        elif action == 'L':
            if state[0] > 1:
                newState = (state[0] - 1, state[1])
        elif action == 'R':
            if state[0] < self.gridInfo['width']:
                newState = (state[0] + 1, state[1])
        return newState
