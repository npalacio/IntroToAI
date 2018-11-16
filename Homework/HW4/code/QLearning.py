import utils
import random

class QLearningAlgorithm:

    def __init__(self, epochLimit, defaultReward):
        # Q(x,y) needs to be initialized somehow? Or we use a default value whenever it is undefined?
        self.epochLimit = epochLimit
        self.defaultReward = defaultReward

        self.Q = self.InitializeQ()
        self.rewards = {}
        self.stateLength = 9
        self.cellValues = [0,1,2]
        self.cpuPlayer = 2
        self.otherPlayer = 1
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
            nextState = utils.SimulateActionByPlayer(state, action, self.cpuPlayer)
            if not utils.IsTerminalTTTState(nextState):
                nextState = self.SimulateRandomActionByPlayer(nextState, self.otherPlayer)
            nextStateReward = self.GetReward(nextState, self.defaultReward, self.cpuPlayer)
            self.Q[(state,action)] = self.GetUpdatedQValue(state, action, nextState, self.Q, self.stateVisitedCount[state], nextStateReward, self.discountFactor)
            state = nextState
            done = utils.IsTerminalTTTState(state)

    def InitializeQ(self):
        return {}

    def GetRandomStartingState(self, stateLength, cellValues):
        state = []
        turns = random.randint(0,4)
        done = False    
        while not done:
            done = True
            state = utils.GetTTTStartingState()
            for turnCount in range(turns):
                if not utils.IsTerminalTTTState(state):
                    randomAction = self.GetRandomAction(state)
                    state = list(utils.SimulateActionByPlayer(state, randomAction, self.cpuPlayer))
                else:
                    # This is a terminal state, will not work
                    done = False
                    continue
                if not utils.IsTerminalTTTState(state):
                    randomAction = self.GetRandomAction(state)
                    state = list(utils.SimulateActionByPlayer(state, randomAction, self.otherPlayer))
                else:
                    # This is a terminal state, will not work
                    done = False
                    continue
        return tuple(state)
    
    def SimulateRandomActionByPlayer(self, state, player):
        randomAction = self.GetRandomAction(state)
        state = utils.SimulateActionByPlayer(state, randomAction, player)
        return state

    def GetRandomCellValue(self, cellValues):
        randomIndex = random.randint(0,len(cellValues) - 1)
        return cellValues[randomIndex]

    def GetRandomAction(self, state):
        availableActions = utils.GetAvailableTTTActions(state)
        randomActionIndex = random.randint(0,len(availableActions) - 1)
        return availableActions[randomActionIndex]

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

    def GetReward(self, state, defaultReward, player):
        if utils.IsTerminalTTTState(state):
            return self.GetTerminalStateReward(state, player)
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

    def GetUpdatedQValue(self, state, action, nextState, Q, timesVisited, nextStateReward, discountFactor):
        # If nextState is a terminal state, best action does not matter, use 0? yes, reward will already be -1,1,0
        nextStateBestQValue = 0
        if not utils.IsTerminalTTTState(nextState):
            bestActionAtNextState = self.GetNextAction(nextState, Q)
            nextStateBestQValue = self.GetQValue(state, bestActionAtNextState, Q)
        alpha = self.GetAlpha(timesVisited)
        currQValue = self.GetQValue(state, action)
        return currQValue + alpha * (nextStateReward + nextStateBestQValue - currQValue)

    def GetAlpha(self, timesVisited):
        return 1 / (timesVisited + 1)
