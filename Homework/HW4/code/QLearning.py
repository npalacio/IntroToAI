import utils
import random

class QLearningAlgorithm:

    def __init__(self, epochLimit, defaultReward, terminalStates):
        # Q(x,y) needs to be initialized somehow? Or we use a default value whenever it is undefined?
        self.epochLimit = epochLimit
        self.defaultReward = defaultReward
        self.terminalStates = terminalStates

        self.Q = self.InitializeQ()
        self.rewards = {}
        self.stateLength = 9
        self.cellValues = [0,1,2]
        self.cpuPlayer = 2
        self.discountFactor = 1
        self.stateVisitedCount = {}
    
    def Run(self):
        epochLimit = self.epochLimit
        iterationCount = 0
        while iterationCount < epochLimit:
            self.RunEpoch()
            iterationCount += 1
        # Could just return Q, calculate policy on the fly?
        return self.Q

    def RunEpoch(self):
        # while not over epoch limit
            # s = random starting state
            # while not done
                # pick action a that maximizes Q(s,a)
                # do action a, get next state s' and its reward r'
                    # initially all rewards are 0 except for terminal states (-1,0,1)
                # Q(s,a) = equation with update using Q(s,a) and Q(s',x) (and N(s) for learning rate?)
                    # will need to find x that maximizes Q(s',x)
                # s = s'
                # done = s is terminal
            # iterate epoch limit
        # End up with a filled out Q(s,a) that can be used to calculate a policy (pick action at state s that maximizes Q)
        state = self.GetRandomStartingState(self.stateLength, self.cellValues)
        done = False
        while not done:
            if state in self.stateVisitedCount:
                self.stateVisitedCount[state] += 1
            else:
                self.stateVisitedCount[state] = 1
            action = self.GetNextAction(state, self.Q)
            nextState = self.SimulateAction(state, action)
            nextStateReward = self.GetReward(nextState, self.defaultReward)
            # What is the reward at any state? -.04 except for terminal states
            self.Q[(state,action)] = self.GetUpdatedQValue(state, action, nextState, Q, self.stateVisitedCount, self.defaultReward, self.discountFactor)
            state = nextState
            done = state in self.terminalStates

    def InitializeQ(self):
        return {}

    def GetRandomStartingState(self, stateLength, cellValues):
        while True:
            state = []
            for cellIndex in range(stateLength):
                randomCellValue = self.GetRandomCellValue(cellValues)
                state[cellIndex] = randomCellValue
            if state not in self.terminalStates:
                return state

    def GetRandomCellValue(self, cellValues):
        randomIndex = random.randint(0,len(cellValues))
        return cellValues[randomIndex]

    def GetNextAction(self, state, Q):
        # pick action a that maximizes Q(s,a)
        availableActions = utils.GetAvailableTTTActions(state)
        qValues = self.GetQValues(state, availableActions, Q)
        maxIndex = qValues.index(max(qValues))
        return availableActions[maxIndex]

    def GetQValues(self, state, actions, Q):
        qValues = []
        for action in actions:
            qValues.append(self.GetQValue(state, action, Q))
        return qValues

    def GetQValue(self, state, action, Q):
        # TODO: Do we need to insert new value into Q here?
        if (state,action) in Q:
            return Q(state,action)
        else:
            return 0

    def SimulateAction(self, state, action, player):
        newState = state.copy()
        newState[action] = player
        return newState

    def GetReward(self, state, defaultReward):
        if state in self.terminalStates:
            return self.GetTerminalStateReward(state)
        else:
            return defaultReward

    def GetTerminalStateReward(self, terminalState, player):
        # Find out which player won
        winner = utils.GetTTTWinner(terminalState)
        if winner == player:
            return 1
        elif winner == None:
            return 0
        else:
            return -1

    def GetUpdatedQValue(self, Q, state, action, nextState, timesVisited, defaultReward, discountFactor):
        bestActionAtNextState = self.GetNextAction(nextState, Q)
        nextStateBestQValue = self.GetQValue(state, bestActionAtNextState, Q)
        nextStateReward = self.GetReward(state, defaultReward)
        alpha = self.GetAlpha(timesVisited)
        currQValue = self.GetQValue(state, action)
        return currQValue + alpha * (nextStateReward + nextStateBestQValue - currQValue)

    def GetAlpha(self, timesVisited):
        return 1 / (timesVisited + 1)
