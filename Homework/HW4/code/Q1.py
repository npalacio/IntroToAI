import os
import sys
import time
# from policyIteration import PolicyIterationAlgorithm
from valueIteration import ValueIterationAlgorithm
from AdaptiveDynamicProgramming import AdaptiveDynamicProgrammingAlgorithm
from DirectUtilEstimation import DirectUtilEstimationAlgorithm
from TemporalDifference import TemporalDifferenceAlgorithm
import utils

transitionDict = {
    'U': [
        {
            'probability': .8,
            'action': 'U'
        },
        {
            'probability': .1,
            'action': 'R'
        },
        {
            'probability': .1,
            'action': 'L'
        }
    ],
    'R': [
        {
            'probability': .8,
            'action': 'R'
        },
        {
            'probability': .1,
            'action': 'U'
        },
        {
            'probability': .1,
            'action': 'D'
        }
    ],
    'L': [
        {
            'probability': .8,
            'action': 'L'
        },
        {
            'probability': .1,
            'action': 'U'
        },
        {
            'probability': .1,
            'action': 'D'
        }
    ],
    'D': [
        {
            'probability': .8,
            'action': 'D'
        },
        {
            'probability': .1,
            'action': 'R'
        },
        {
            'probability': .1,
            'action': 'L'
        }
    ]
}
config = {
    'gridInfos': [
        {
            'width': 4,
            'height': 3,
            'defaultValue': -.04,
            'obstacles': [(2,2)],
            'terminalCells': [
                {
                    'cell': (4,3),
                    'value': 1
                },
                {
                    'cell': (4,2),
                    'value': -1
                }
            ]
        },
        {
            'width': 10,
            'height': 10,
            'defaultValue': -.04,
            'obstacles': [],
            'terminalCells': [
                {
                    'cell': (5,5),
                    'value': 1
                }
            ]
        },
        {
            'width': 10,
            'height': 10,
            'defaultValue': -.04,
            'obstacles': [(4, 4),(6, 4),(4, 6),(6, 6)],
            'terminalCells': [
                {
                    'cell': (5,5),
                    'value': 1
                }
            ]
        },
        {
            'width': 10,
            'height': 10,
            'defaultValue': -.04,
            'obstacles': [(4, 4),(6, 4),(4, 6),(6, 6)],
            'terminalCells': [
                {
                    'cell': (5,5),
                    'value': 1
                },
                {
                    'cell': (5,7),
                    'value': -1
                },
                {
                    'cell': (4,5),
                    'value': -1
                }
            ]
        }
    ],
    'discountFactor': .9,
    'epochLimit': 1000
}
# Need to get the policy
def GetGridInfo(gridInfos):
    print('Grid options:')
    print('\t1: 4 X 3 world with one obstacle in (2, 2), reward +1 at (4, 3) and -1 at (4, 2)')
    print('\t2: 10 X 10 world with no obstacles and reward +1 at (5, 5)')
    print('\t3: 10 X 10 world with four obstacles at (4, 4) (6, 4) (4, 6) (6, 6) and reward +1 at (5, 5)')
    print('\t4: 10 X 10 world with four obstacles at (4, 4) (6, 4) (4, 6) (6, 6) and reward +1 at (5, 5), reward -1 at (5, 7) and (4, 5)')
    print('\t5: Exit')
    print('')
    done = False
    validOptions = list(range(1,6))
    while not done:
        gridNum = int(input('Please choose your grid:' + os.linesep))
        done = gridNum in validOptions
        if not done:
            print('Invalid grid choice!')
    if gridNum == 5:
        return None
    return gridInfos[gridNum - 1]

def GetAlgorithm():
    print('Algorithm options:')
    print('\t1: Direct Utility Estimation')
    print('\t2: Adaptive Dynamic Programming')
    print('\t3: Temporal Difference')
    done = False
    validOptions = list(range(1,4))
    while not done:
        algoNum = int(input('Please choose your algorithm:' + os.linesep))
        done = algoNum in validOptions
        if not done:
            print('Invalid algorithm choice!')
    return algoNum

def GetPolicy(rewardDict, transitionDict, discountFactor, gridInfo):
    # policyIteration = PolicyIterationAlgorithm(rewardDict, transitionDict, discountFactor, gridInfo)
    # results = policyIteration.Run()
    valueIteration = ValueIterationAlgorithm(rewardDict, transitionDict, discountFactor, gridInfo)
    results = valueIteration.Run()
    return results['policy']

def GetReward(cell, gridInfo):
    terminalCell = [cellObj for cellObj in gridInfo['terminalCells'] if cellObj['cell'] == cell]
    if len(terminalCell) > 0:
        return terminalCell[0]['value']
    elif cell in gridInfo['obstacles']:
        return 'NA'
    return gridInfo['defaultValue']

def GetActualRewardDict(gridInfo):
    rewardDict = {}
    for col in range(gridInfo['width']):
        for row in range(gridInfo['height']):
            cell = (col + 1, row + 1)
            reward = GetReward(cell, gridInfo)
            rewardDict[cell] = reward
    return rewardDict

def GetStartingState(validCells):
    done = False
    state = None
    while not done:
        col = int(input('Please provide the starting column:' + os.linesep))
        row = int(input('Please provide the starting row:' + os.linesep))
        state = (col,row)
        done = state in validCells
        if not done:
            print('Invalid starting state!')
    return state

def RunSimulationFromStart(policy, startingState, gridInfo, validCells):
    done = False
    currState = startingState
    sequence = [str(currState)]
    while not done:
        action = policy[currState]
        if action == 'NA':
            done = True
        else:
            sequence.append(action)
            nextState = utils.GetNextState(currState, action, gridInfo, validCells)
            sequence.append(str(nextState))
            currState = nextState
    return sequence

def RunSimulation(policy, gridInfo):
    gridCells = utils.GetGridCells(gridInfo)
    gridCellsMinusObstacles = utils.GetGridCellsMinusObstacles(gridCells,gridInfo)
    validCells = utils.GetValidGridCells(gridCells, gridInfo)
    # Get starting point from user
    startingState = GetStartingState(validCells)
    # Follow policy until end
    sequence = RunSimulationFromStart(policy, startingState, gridInfo, gridCellsMinusObstacles)
    return sequence

def PrintSequence(sequence):
    print(' --> '.join(sequence))

def PrintPolicy(policy, gridInfo):
    gridTextArr = []
    cellWidth = 10
    for row in range(gridInfo['height']):
        row += 1
        rowTextArr = []
        for col in range(gridInfo['width']):
            col += 1
            cell = (col,row)
            cellText = str(cell) + '=' + policy[cell]
            rowTextArr.append(cellText.center(cellWidth,' '))
        gridTextArr.append('|'.join(rowTextArr))
    rowSeparator = os.linesep + ('-' * ((cellWidth * 10) + 9)) +  os.linesep
    print(rowSeparator.join(reversed(gridTextArr)))
    

def Main(actualTransitionDict, discountFactor, epochLimit, gridInfos):
    while True:
        # Get world from user
        gridInfo = GetGridInfo(gridInfos)
        if gridInfo == None:
            sys.exit()
        # Get algorithm from user
        algorithm = GetAlgorithm()
        actualRewardDict = GetActualRewardDict(gridInfo)
        # Get policy for this world
        policy = GetPolicy(actualRewardDict, actualTransitionDict, discountFactor, gridInfo)
        # PrintPolicy(policy, gridInfo)
        newPolicy = None
        # print('Algorithm starting at ' + time.strftime("%H:%M:%S"))
        if algorithm == 1:
            print('Running DUE algorithm...')
            due = DirectUtilEstimationAlgorithm(policy, epochLimit, gridInfo, actualRewardDict, actualTransitionDict)
            newPolicy = due.Run()
        elif algorithm == 2:
            print('Running ADP algorithm...')
            adp = AdaptiveDynamicProgrammingAlgorithm(policy, epochLimit, discountFactor, gridInfo, actualRewardDict, actualTransitionDict)
            newPolicy = adp.Run()
        elif algorithm == 3:
            print('Running TD algorithm...')
            td = TemporalDifferenceAlgorithm(policy, epochLimit, discountFactor, gridInfo, actualRewardDict, actualTransitionDict)
            newPolicy = td.Run()
        # print('Algorithm ending at ' + time.strftime("%H:%M:%S"))
        sequence = RunSimulation(newPolicy, gridInfo)
        PrintSequence(sequence)

Main(transitionDict, config['discountFactor'], config['epochLimit'], config['gridInfos'])