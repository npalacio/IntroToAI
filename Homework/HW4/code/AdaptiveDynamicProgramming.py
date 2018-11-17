import utils
import random

class AdaptiveDynamicProgrammingAlgorithm:
    def __init__(self, policy, epochLimit, discountFactor, gridInfo, actualRewardDict, actualTransitionModel):
        self.policy = policy
        # self.epochLimit = epochLimit
        self.epochLimit = 300
        self.discountFactor = discountFactor
        self.gridInfo = gridInfo
        self.actualRewardDict = actualRewardDict
        self.actualTransitionModel = actualTransitionModel

        # Static variables
        self.gridCells = utils.GetGridCells(self.gridInfo)
        self.gridCellsMinusObstacles = utils.GetGridCellsMinusObstacles(self.gridCells, self.gridInfo)
        self.validGridCells = utils.GetValidGridCells(self.gridCells, self.gridInfo)
        self.prevState = None
        self.prevAction = None
        self.stateActionCount = self.InitializeStateActionCount()
        self.stateActionStateCount = self.InitializeStateActionStateCount()
        self.transitionModel = self.InitializeTransitionModel()
        # Every cell should have some reward
        self.rewardDict = self.InitializeRewardDict(self.gridCells)
        self.utilityDict = self.InitializeUtilityDict(self.gridCells)

    def Run(self):
        epochLimit = self.epochLimit
        iterationCount = 0
        while iterationCount < epochLimit:
            # What is an epoch here? Do we iterate on individual states or trial runs?
            self.RunEpoch()
            iterationCount += 1
        # Once we finish learning we need to calculate policies from the utilties
        # policy = self.GetPolicy(self.utilityDict, self.actualTransitionModel, self.transitionModel, self.validGridCells)
        policy = utils.GetGreedyPolicy(self.utilityDict, self.validGridCells, self.gridInfo, self.gridCellsMinusObstacles, self.actualTransitionModel)
        return policy

    def RunEpoch(self):
        # 1 epoch = iterate until we hit a terminal state
        epochDone = False
        while not epochDone:
            state = self.GetNewState(self.prevState, self.prevAction, self.gridInfo, self.actualTransitionModel)
            reward = self.actualRewardDict[state]
            if self.IsNewState(state, self.rewardDict):
                self.UpdateStateUtility(state, reward)
                self.UpdateStateReward(state, reward)
            if self.prevState != None:
                # This is not a starting state, we came here from somewhere
                self.UpdateTransitionModelData(self.prevState, self.prevAction, state)
                self.UpdateTransitionModel(self.stateActionStateCount, self.stateActionCount)
            self.utilityDict = self.EvaluatePolicy(self.rewardDict, self.utilityDict, self.transitionModel, self.discountFactor, self.policy, self.validGridCells)
            isTerminalState = self.IsTerminalState(state)
            self.UpdatePreviousValues(isTerminalState, state, self.policy[state])
            epochDone = isTerminalState

    def GetNewState(self, state, action, gridInfo, transitionDict):
        # Simulate with actual transition model here?
        if state == None or action == None:
            return self.GetRandomStartingState(gridInfo)
        newState = self.SimulateTransition(state, transitionDict[action], gridInfo, self.gridCellsMinusObstacles)
        return newState
        
    def SimulateTransition(self, state, transitions, gridInfo, validCells):
        randomProbability = random.randint(0,1000) / 1000
        currTransitionValue = 0
        for transition in transitions:
            currTransitionValue += transition['probability']
            if currTransitionValue >= randomProbability:
                return utils.GetNextState(state, transition['action'], gridInfo, validCells)
        print('should never be hit')

    def GetRandomStartingState(self, gridInfo):
        # terminalCells = [terminalCell['cell'] for terminalCell in gridInfo['terminalCells']]
        while True:
            randCol = random.randint(1, gridInfo['width'])
            randRow = random.randint(1, gridInfo['height'])
            randCell = (randCol,randRow)
            if self.IsValidState(randCell, gridInfo):
                return randCell
        raise Exception('should never be hit')

    def IsValidState(self, state, gridInfo):
        terminalCells = [terminalCell['cell'] for terminalCell in gridInfo['terminalCells']]
        return state not in terminalCells and state not in gridInfo['obstacles']

    def IsNewState(self, state, rewardDict):
        # If it is not in our reward dictionary, we have not visited it yet
        return rewardDict[state] == 0

    def IsTerminalState(self, state):
        # If it is not in our reward dictionary, we have not visited it yet
        return len([terminalCell for terminalCell in self.gridInfo['terminalCells'] if terminalCell['cell'] == state]) > 0

    def InitializeStateActionCount(self):
        return {}

    def InitializeStateActionStateCount(self):
        return {}

    def InitializeTransitionModel(self):
        return {}

    def InitializeRewardDict(self, rewardableCells):
        rewardDict = {}
        for state in rewardableCells:
            rewardDict[state] = 0
        return rewardDict

    def InitializeUtilityDict(self, gridCells):
        utilDict = {}
        for state in gridCells:
            utilDict[state] = 0
        return utilDict

    def UpdateStateReward(self, state, reward):
        self.rewardDict[state] = reward

    def UpdateStateUtility(self, state, reward):
        self.utilityDict[state] = reward

    def UpdateTransitionModelData(self, prevState, action, resultingState):
        # This keeps track of state-action-state frequencies
        if (prevState, action) in self.stateActionCount:
            self.stateActionCount[(prevState, action)] += 1
        else:
            self.stateActionCount[(prevState, action)] = 1
        if (prevState, action, resultingState) in self.stateActionStateCount:
            self.stateActionStateCount[(prevState, action, resultingState)] += 1
        else:
            self.stateActionStateCount[(prevState, action, resultingState)] = 1

    def UpdateTransitionModel(self, stateActionStateCount, stateActionCount):
        # This is our actual transition model for MDP
        for triple in stateActionStateCount:
            if stateActionStateCount[triple] != 0:
                # If you are in the state-action-state dict you are also in the state-action dict
                self.UpdateTransition(triple, stateActionStateCount[triple], stateActionCount[(triple[0], triple[1])])

    def UpdateTransition(self, stateActionState, stateActionStateCount, stateActionCount):
        self.transitionModel[(stateActionState[0], stateActionState[1], stateActionState[2])] = stateActionStateCount / stateActionCount

    def EvaluatePolicy(self, rewardDict, utilitiesDict, transitionModel, discountFactor, policy, validCells):
        updatedUtilities = utils.EvaluatePolicy(rewardDict, utilitiesDict, transitionModel, discountFactor, policy, validCells)
        return updatedUtilities

    def UpdatePreviousValues(self, isTerminalState, state, action):
        if isTerminalState:
            self.prevState = None
            self.prevAction = None
        else:
            self.prevState = state
            self.prevAction = action

    def GetPolicy(self, utilitiesDict, transitionDict, transitionModel, validCells):
        return utils.GetPolicy(utilitiesDict, transitionDict, transitionModel, validCells)