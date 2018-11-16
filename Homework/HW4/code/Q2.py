import os
import utils
from QLearning import QLearningAlgorithm

config = {
    'epochLimit': 10000,
    'cpuPlayer': 2,
    'otherPlayer': 1,
    'defaultReward': -.04
}

def PrintResult(state, cpuPlayer, otherPlayer):
    winner = utils.GetTTTWinner(state)
    if winner == None:
        print('Scratch!')
    elif winner == cpuPlayer:
        print('I win!')
    elif winner == otherPlayer:
        print('You win!')
    PrintState(state)

def GetCellValue(stateValue):
    if stateValue == 0:
        return '(empty)'
    elif stateValue == 1:
        return 'O'
    elif stateValue == 2:
        return 'X'

def PrintState(state):
    print('Current board:')
    cellWidth = 15
    cellNum = 0
    boardRows = []
    for row in range(3):
        rowCells = []
        for column in range(3):
            cellValue = GetCellValue(state[cellNum])
            cellContent = str(cellNum) + '=' + cellValue if cellValue == '(empty)' else cellValue
            cellContent = cellContent.center(cellWidth, ' ')
            rowCells.append(cellContent)
            cellNum += 1
        boardRows.append('|'.join(rowCells))
    rowSeparator = os.linesep + ('-' * ((cellWidth * 3) + 2)) +  os.linesep
    print(rowSeparator.join(boardRows))

def IsValidAction(state, action):
    stateAsList = list(state)
    if action not in list(range(9)):
        return False
    return stateAsList[action] == 0

def GetOtherPlayersAction(state, otherPlayer):
    isValidAction = False
    action = -1
    while not isValidAction:
        action = int(input('Please provide the number for your next move:' + os.linesep))
        isValidAction = IsValidAction(state, action)
        if not isValidAction:
            print('Invalid move! Try again')
    return action

def SimulateOtherPlayersMove(state, otherPlayer):
    action = GetOtherPlayersAction(state, otherPlayer)
    resultingState = utils.SimulateActionByPlayer(state, action, otherPlayer)
    return resultingState

def SimulateCPUMove(state, Q, cpuPlayer):
    action = utils.GetNextTTTAction(state, Q)
    resultingState = utils.SimulateActionByPlayer(state, action, cpuPlayer)
    return resultingState

def PlayTTT(Q, cpuPlayer, otherPlayer):
    print('Let\'s play...')
    state = utils.GetTTTStartingState()
    PrintState(state)
    done = False
    while not done:
        print('My turn...')
        state = SimulateCPUMove(state, Q, cpuPlayer)
        if utils.IsTerminalTTTState(state):
            done = True
            continue
        print('Your turn...')
        PrintState(state)
        state = SimulateOtherPlayersMove(state, otherPlayer)
        if utils.IsTerminalTTTState(state):
            done = True
            continue
    PrintResult(state, cpuPlayer, otherPlayer)

def Main(epochLimit, defaultReward, cpuPlayer, otherPlayer):
    print('Training tic tac toe simulator...')
    qAlgo = QLearningAlgorithm(epochLimit, defaultReward, cpuPlayer, otherPlayer)
    Q = qAlgo.Run()
    # Now I have the best action to take at every state
    PlayTTT(Q, cpuPlayer, otherPlayer)

# PrintState(GetStartingState())
Main(config['epochLimit'], config['defaultReward'], config['cpuPlayer'], config['otherPlayer'])