import random

class PolicyIterationAlgorithm:
    def __init__(self, rewardDict, transitionDict, discountFactor, gridInfo):
        self.rewardDict = rewardDict
            # {(1,1): -.04}
        self.transitionDict = transitionDict
            # {'U': [[.8,'U'],[.1,'L'],[.1,'R']]}
            # {'U': [{'probability': .8, 'action': 'U'},{'probability': .1, 'action': 'L'}]}
        self.discountFactor = discountFactor
        self.gridInfo = gridInfo

    def Run(self):
        expectedRewardDict = self.GetInitialExpectedRewardDict(self.rewardDict)
        policies = self.GetInitialPolicies(self.rewardDict, self.transitionDict)
            # {(1,2): 'U'}
        done = False
        while not done:
            done = True
            expectedRewardDict = self.EvaluatePolicies(self.rewardDict, expectedRewardDict, self.transitionDict, self.discountFactor, policies)
            for state in self.rewardDict:
                if state not in self.gridInfo['rewardCells']['cells']:
                    newRewardAndAction = self.GetExpectedRewardAndAction(state, self.rewardDict, expectedRewardDict, self.transitionDict)
                    currPolicyReward = self.GetX(state, self.rewardDict, expectedRewardDict, self.transitionDict[policies[state]])
                    if newRewardAndAction['expectedReward'] > currPolicyReward:
                        policies[state] = newRewardAndAction['action']
                        done = False
        return {
            'expectedRewardDict': expectedRewardDict,
            'policy': policies
        }

    def GetExpectedRewardAndAction(self, state, rewardDict, expectedRewardDict, transitionDict):
        # I need to know the action that lead to the max utility
        if state in self.gridInfo['rewardCells']['cells']:
            return {
                'action': 'NA',
                'expectedReward': rewardDict[state]
            }
        # xArray = [self.GetX(state, expectedRewardDict, transitionDict[action]) for action in transitionDict]
        xArray = []
        actions = []
        for action in transitionDict:
            actions.append(action)
            xArray.append(self.GetX(state, rewardDict, expectedRewardDict, transitionDict[action]))
        maxX = max(xArray)
        return {
            'action': actions[xArray.index(maxX)],
            'expectedReward': maxX
        }

    def GetX(self, state, rewardDict, expectedRewardDict, transitions):
        if state in self.gridInfo['rewardCells']['cells']:
            return rewardDict[state]
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

    def GetInitialPolicies(self, rewardDict, transitionDict):
        randomPolicies = {}
        numActions = len(transitionDict)
        for state in rewardDict:
            if state in self.gridInfo['rewardCells']['cells']:
                randomPolicies[state] = 'NA'
                continue
            randomIndex = random.randint(0, numActions - 1)
            randomAction = self.GetRandomAction(randomIndex, transitionDict)
            randomPolicies[state] = randomAction
        return randomPolicies

    def GetRandomAction(self, randomIndex, transitionDict):
        i = 0
        for action in transitionDict:
            if i == randomIndex:
                return action
            i += 1

    def EvaluatePolicies(self, rewardDict, currExpectedRewardDict, transitionDict, discountFactor, policies):
        newExpectedRewardDict = {}
        for state in currExpectedRewardDict:
            if state in self.gridInfo['rewardCells']['cells']:
                newExpectedRewardDict[state] = rewardDict[state]
                continue
            x = self.GetX(state, rewardDict, currExpectedRewardDict, transitionDict[policies[state]])
            newExpectedRewardDict[state] = rewardDict[state] + discountFactor * x
        return newExpectedRewardDict

    def GetInitialExpectedRewardDict(self, rewardDict):
        expectedRewardDict = {}
        # [expectedRewardDict[state] = 0 for state in rewardDict]
        for state in rewardDict:
            expectedRewardDict[state] = 0
        return expectedRewardDict
