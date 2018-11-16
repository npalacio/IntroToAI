from QLearning import QLearningAlgorithm

config = {
    'epochLimit': 10000,
    'defaultReward': -.04
}
def GetTerminalTTTStates():

def Main(epochLimit, defaultReward):
    terminalStates = GetTerminalTTTStates()
    q = QLearningAlgorithm(epochLimit, defaultReward, terminalStates)