import utils
import random

class DirectUtilEstimationAlgorithm:
    def __init__(self, policy, epochLimit, gridInfo, actualRewardDict, actualTransitionModel):
        self.policy = policy
        self.epochLimit = epochLimit * 10
        self.gridInfo = gridInfo
        self.actualRewardDict = actualRewardDict
        self.actualTransitionModel = actualTransitionModel

        # Grid stuff
        self.gridCells = utils.GetGridCells(self.gridInfo)
        self.gridCellsMinusObstacles = utils.GetGridCellsMinusObstacles(self.gridCells, self.gridInfo)
        self.validGridCells = utils.GetValidGridCells(self.gridCells, self.gridInfo)

        # Static vars
        self.startStateCount = self.InitializeStateDict(self.gridCellsMinusObstacles, 0)
        self.startStateTotalReward = self.InitializeStateDict(self.gridCellsMinusObstacles, 0)
# startStateCount = {(1,3): 4}
    # Initialize all states to zero
# startStateTotalReward = {(1,3): 10.68}
    # Initialize all states to zero
# while under epoch limit:
    # startState = get random starting state (cannot be obstacle or terminal state)
    # state = startState
    # totalReward = reward at state
    # done = state is terminal state
    # while not done
        # action = action from policy[state]
        # state = simulate action at this state
        # totalReward += reward at state
        # done = state is terminal state
    # startStateCount += 1
    # startStateTotalReward += totalReward
# utilities = get utlities using startStateCount and startStateTotalReward
# policy = get greedy policy using utilities
# return policy

    def Run(self):
        iterationCount = 0
        while iterationCount < self.epochLimit:
            self.RunEpoch()
            iterationCount += 1
        utilities = self.GetUtilities(self.startStateCount, self.startStateTotalReward)
        policy = utils.GetGreedyPolicy(utilities, self.validGridCells, self.gridInfo, self.gridCellsMinusObstacles, self.actualTransitionModel)
        return policy
        
    def RunEpoch(self):
        # Should be able to handle starting at terminal state
        startingState = self.GetRandomStartingState(self.gridInfo['height'], self.gridInfo['width'], self.gridCellsMinusObstacles)
        state = startingState
        totalReward = self.actualRewardDict[state]
        # This should only be true if state is a terminal state
        done = state not in self.validGridCells
        while not done:
            # action = action from policy[state]
            action = self.policy[state]
            # state = simulate action at this state
            state = self.SimulateTransition(state, self.actualTransitionModel[action], self.gridInfo, self.gridCellsMinusObstacles)
            # totalReward += reward at state
            totalReward += self.actualRewardDict[state]
            # done = state is terminal state
            done = state not in self.validGridCells
        # startStateCount += 1
        self.startStateCount[startingState] += 1
        # startStateTotalReward += totalReward
        self.startStateTotalReward[startingState] += totalReward

    def SimulateTransition(self, state, transitions, gridInfo, validCells):
        randomProbability = random.randint(0,1000) / 1000
        currTransitionValue = 0
        for transition in transitions:
            currTransitionValue += transition['probability']
            if currTransitionValue >= randomProbability:
                return utils.GetNextState(state, transition['action'], gridInfo, validCells)
        raise Exception("transition did not find right one")

    def GetUtilities(self, startStateCount, startStateTotalReward):
        utilities = {}
        for state in startStateCount:
            # TODO: Decide if we need to handle the case where we never started on a particular state?
            utilities[state] = startStateTotalReward[state] / startStateCount[state]
        return utilities

    def GetRandomStartingState(self, height, width, validStates):
        while True:
            randCol = random.randint(1, width)
            randRow = random.randint(1, height)
            randCell = (randCol,randRow)
            if randCell in validStates:
                return randCell
        raise Exception('should never be hit in getting rand start state')

    def InitializeStateDict(self, states, value):
        startStateCounts = {}
        for state in states:
            startStateCounts[state] = value
        return startStateCounts
