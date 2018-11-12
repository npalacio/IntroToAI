import utils
import random

class AdaptiveDynamicProgramming:
    def __init__(self, policy, epochLimit, discountFactor, gridInfo, actualRewardDict, actualTransitionModel):
        self.policy = policy
        self.epochLimit = epochLimit
        self.discountFactor = discountFactor
        self.gridInfo = gridInfo
        self.actualRewardDict = actualRewardDict
        self.actualTransitionModel = actualTransitionModel

        # Static variables
        self.gridCells = self.GetGridCells(self.gridInfo)
        self.gridCellsMinusObstacles = self.GetGridCellsMinusObstacles(self.gridCells, self.gridInfo)
        self.prevState = None
        self.prevAction = None
        self.stateActionCount = self.InitializeStateActionCount(self.gridInfo, self.actualTransitionModel)
        self.stateActionStateCount = self.InitializeStateActionStateCount()
        self.transitionModel = self.InitializeTransitionModel()
        self.rewardDict = self.InitializeRewardDict(self.gridCellsMinusObstacles)
        self.utilityDict = self.InitializeUtilityDict()

    def Run(self):
        epochLimit = self.epochLimit
        iterationCount = 0
        while iterationCount < epochLimit:
            # What is an epoch here? Do we iterate on individual states or trial runs?
            self.RunEpoch()
            iterationCount += 1
        # Once we finish learning we need to calculate policies from the utilties

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
                self.UpdateTransitionModel(self.stateActionCount)
            newUtilities = self.EvaluatePolicy()
            isTerminalState = self.IsTerminalState()
            self.UpdatePreviousValues(isTerminalState, state, policy[state])
            epochDone = isTerminalState

    def GetNewState(self, state, action, gridInfo, transitionDict):
        # Simulate with actual transition model here?
        if state == None or action == None:
            return self.GetRandomStartingState(gridInfo)
        newState = self.SimulateTransition(state, transitionDict[action], gridInfo)
        return newState
        
    def SimulateTransition(self, state, transitions, gridInfo):
        randomProbability = random.randint(0,1000) / 1000
        currTransitionValue = 0
        for transition in transitions:
            currTransitionValue += transition['probability']
            if currTransitionValue > randomProbability:
                return utils.GetNextState(state, transition['action'], gridInfo)

    def GetRandomStartingState(self, gridInfo):
        # terminalCells = [terminalCell['cell'] for terminalCell in gridInfo['terminalCells']]
        while True:
            randCol = random.randint(1, gridInfo['width'])
            randRow = random.randint(1, gridInfo['height'])
            randCell = (randCol,randRow)
            if self.IsValidState(randCell, gridInfo):
                return randCell

    def IsValidState(self, state, gridInfo):
        terminalCells = [terminalCell['cell'] for terminalCell in gridInfo['terminalCells']]
        return state not in terminalCells and state not in gridInfo['obstacles']:

    def IsNewState(self, state, rewardDict):
        # If it is not in our reward dictionary, we have not visited it yet
        return rewardDict[state] == 0

    def IsTerminalState(self, state):
        # If it is not in our reward dictionary, we have not visited it yet
        return len([terminalCell for terminalCell in self.gridInfo['terminalCells'] if terminalCell['cell'] == state]) > 0

    def InitializeStateActionCount(self, gridInfo, transitionDict):
        pairs = {}
        for state in self.gridCells:
            if not self.IsValidState(state, gridInfo):
                continue
            for action in transitionDict:
                pairs[(state, action)] = 0
        return pairs

    def InitializeStateActionStateCount(self):
        # This will need to initialize state-action-resultingState triples for all neighboring states of a state
        # TODO: Figure out how to intialize the triples without 800 dict keys

    def InitializeTransitionModel(self):
        # TODO: How do I initialize the transition model? Set the actual move to a probability of 100%?

    def InitializeRewardDict(self, rewardableCells):
        rewardDict = {}
        for state in rewardableCells:
            rewardDict[state] = 0
        return rewardDict

    def InitializeUtilityDict(self):

    def GetGridCellsMinusObstacles(self, gridCells, gridInfo):
        return [cell for cell in gridCells if cell not in gridInfo['obstacles']]

    def GetGridCells(self, gridInfo):
        cells = []
        for col in gridInfo['width']:
            for row in gridInfo['height']:
                cells.append((col + 1, row + 1))
        return cells

    def UpdateStateReward(self, state, reward):
        self.rewardDict[state] = reward

    def UpdateStateUtility(self, state, reward):
        self.utilityDict[state] = reward

    def UpdateTransitionModelData(self, prevState, action, resultingState):
        # This keeps track of state-action-state frequencies
        self.stateActionCount[(prevState, action)] += 1
        self.stateActionStateCount[(prevState, action, resultingState)] += 1

    def UpdateTransitionModel(self, stateActionStateCount, stateActionCount):
        # This is our actual transition model for MDP
        for triple in stateActionStateCount:
            if stateActionStateCount[triple[0],triple[1],triple[2]] != 0:
                self.UpdateTransition(triple, stateActionStateCount[triple[0],triple[1],triple[2]] stateActionCount[(triple[0], triple[1])])

    def UpdateTransition(self, stateActionState, stateActionStateCount, stateActionCount):
        self.transitionModel[(triple[0], triple[1], triple[2])] = stateActionStateCount / stateActionCount

    def EvaluatePolicy(self):
        # TODO: refactor to drop self refs
        updatedUtilities = utils.EvaluatePolicy(self.rewardDict, self.utilitiesDict, self.transitionModel, self.discountFactor, self.policy, self.gridInfo)
        return updatedUtilities

    def UpdatePreviousValues(self, isTerminalState, state):
        if isTerminalState:
            self.prevState = None
            self.prevAction = None
        else:
            self.prevState = state
            self.prevAction = self.policy[state]
