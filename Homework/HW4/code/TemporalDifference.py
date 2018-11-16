import utils
import random

class TemporalDifferenceAlgorithm:
    def __init__(self, policy, epochLimit, discountFactor, gridInfo, actualRewardDict, actualTransitionModel):
        self.policy = policy
        self.epochLimit = epochLimit * 10
        # TODO: Decide if this is df
        self.discountFactor = 1
        self.gridInfo = gridInfo
        self.actualRewardDict = actualRewardDict
        self.actualTransitionModel = actualTransitionModel

        # Grid Stuff
        self.gridCells = utils.GetGridCells(self.gridInfo)
        self.gridCellsMinusObstacles = utils.GetGridCellsMinusObstacles(self.gridCells, self.gridInfo)
        self.validGridCells = utils.GetValidGridCells(self.gridCells, self.gridInfo)

        self.stateVisitedCount = utils.InitializeStateDict(self.gridCellsMinusObstacles, 0)
        self.utilities = {}

    def Run(self):
        epochLimit = self.epochLimit
        iterationCount = 0
        while iterationCount < epochLimit:
            self.RunEpoch()
            iterationCount += 1
        policy = utils.GetGreedyPolicy(self.utilities, self.validGridCells, self.gridInfo, self.gridCellsMinusObstacles, self.actualTransitionModel)
        return policy

    def RunEpoch(self):
        state = utils.GetRandomStartingState(self.gridInfo['height'], self.gridInfo['width'], self.validGridCells)
        done = False
        while not done:
            reward = self.actualRewardDict[state]
            if self.stateVisitedCount[state] == 0:
                self.utilities[state] = reward
            self.stateVisitedCount[state] += 1
            action = self.policy[state]
            nextState = utils.SimulateTransition(state, self.actualTransitionModel[action], self.gridInfo, self.gridCellsMinusObstacles)
            if self.stateVisitedCount[nextState] == 0:
                self.utilities[nextState] = self.actualRewardDict[nextState]
            self.utilities[state] = self.GetUpdatedUtility(self.utilities[state], self.stateVisitedCount[state], reward, self.utilities[nextState], self.discountFactor)
            state = nextState
            done = nextState not in self.validGridCells

    def GetUpdatedUtility(self, currUtility, timesVisited, reward, nextStateUtlity, discountFactor):
        alpha = self.GetAlpha(timesVisited)
        return currUtility + alpha * (reward + (discountFactor * nextStateUtlity) - currUtility)

    def GetAlpha(self, timesVisited):
        return 1 / (timesVisited + 1)