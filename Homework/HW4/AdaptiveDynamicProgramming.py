import utils

class AdaptiveDynamicProgramming:
    def __init__(self, policy, epochLimit, gridInfo, actualRewardDict, actualTransitionModel):
        self.policy = policy
        self.epochLimit = epochLimit
        self.gridInfo = gridInfo
        self.actualRewardDict = actualRewardDict
        self.actualTransitionModel = actualTransitionModel

        # Static variables
        self.prevState = None
        self.prevAction = None
        self.transitionModelData = self.InitializeTransitionModelData()
        self.transitionModel = self.InitializeTransitionModel()
        self.rewardDict = self.InitializeRewardDict()
        self.UtilityDict = self.InitializeUtilityDict()

    def Run(self):
        epochLimit = self.epochLimit
        iterationCount = 0
        while iterationCount < epochLimit:
            # What is an epoch here? Do we iterate on individual states or trial runs?
            self.RunEpoch()
            iterationCount += 1

    def RunEpoch(self):
        # 1 epoch = iterate until we hit a terminal state
        epochDone = False
        while not epochDone:
            state = self.GetNewState(self.prevState, self.prevAction, self.gridInfo, self.actualTransitionModel)
            reward = self.rewardDict[state]
            if self.IsNewState(state):
                self.UpdateStateUtility(state, reward)
                self.UpdateStateReward(state, reward)
            if self.prevState != None:
                self.UpdateTransitionModelData()
                self.UpdateTransitionModel(self.transitionModelData)
            newUtilities = self.EvaluatePolicy()
            isTerminalState = self.IsTerminalState()
            self.UpdatePreviousValues(isTerminalState, state, policy[state])
            epochDone = isTerminalState

    def GetNewState(self, state, action, gridInfo, transitionModel):
        # Simulate with actual transition model here?
        # If action is null you can pick random starting state?

    def IsNewState(self):
    def InitializeTransitionModelData(self):
    def InitializeTransitionModel(self):
    def InitializeRewardDict(self):
    def InitializeUtilityDict(self):
    def UpdateStateReward(self, state, reward):
        self.rewardDict[state] = reward
    def UpdateStateUtility(self, state, reward):

    def UpdateTransitionModelData(self):
        # This keeps track of state-action-state frequencies
    def UpdateTransitionModel(self, transitionFrequencies):
        # This is our actual transition model for MDP

    def EvaluatePolicy(self):
        utils.EvaluatePolicy()
    def UpdatePreviousValues(self, isTerminalState, state):
        if isTerminalState:
            self.prevState = None
            self.prevAction = None
        else:
            self.prevState = state
            self.prevAction = self.policy[state]
