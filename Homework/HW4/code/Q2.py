import os
from QLearning import QLearningAlgorithm

config = {
    'epochLimit': 10000,
    'defaultReward': -.04
}

def PrintState(state):
    print('Current board:')
    cellNum = 0
    boardRows = []
    for row in range(3):
        rowCells = []
        for column in range(3):
            rowCells.append('  ' + str(cellNum) + '  ')
            cellNum += 1
        boardRows.append('|'.join(rowCells))
    rowSeparator = os.linesep + '-----------------' +  os.linesep
    print(rowSeparator.join(boardRows))

def PlayTTT(Q):
    startingState = GetStartingState()
    PrintState(startingState)

def Main(epochLimit, defaultReward):
    print('Training tic tac toe simulator...')
    qAlgo = QLearningAlgorithm(epochLimit, defaultReward)
    Q = qAlgo.Run()
    # Now I have the best action to take at every state
    PlayTTT(Q)
# PrintState(GetStartingState())
Main(config['epochLimit'], config['defaultReward'])