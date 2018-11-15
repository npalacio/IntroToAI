import os
import sys
from policyIteration import PolicyIterationAlgorithm
from AdaptiveDynamicProgramming import AdaptiveDynamicProgrammingAlgorithm
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
        }
    ],
    'discountFactor': .9,
    'epochLimit': 1000
}
# Need to get the policy
def GetGridInfo(gridInfos):
    print('Grid options:' + os.linesep)
    print('\t1: 4 X 3 world with one obstacle in (2, 2), reward +1 at (4, 3) and -1 at (4, 2)' + os.linesep)
    print('\t2: 10 X 10 world with no obstacles and reward +1 at (5, 5)' + os.linesep)
    print('\t3: 10 X 10 world with four obstacles at (4, 4) (6, 4) (4, 6) (6, 6) and reward +1 at (5, 5)' + os.linesep)
    print('\t4: 10 X 10 world with four obstacles at (4, 4) (6, 4) (4, 6) (6, 6) and reward +1 at (5, 5), reward -1 at (5, 7) and (4, 5)' + os.linesep)
    print('')
    done = False
    validOptions = list(range(1,4))
    while not done:
        gridNum = int(input('Please choose your grid:' + os.linesep))
        done = gridNum in validOptions
        if not done:
            print('Invalid grid choice!')
    return gridInfos[gridNum]

def GetAlgorithm():
    print('Algorithm options:' + os.linesep)
    print('\t1: Direct Utility Estimation' + os.linesep)
    print('\t2: Adaptive Dynamic Programming' + os.linesep)
    print('\t3: Temporal Difference' + os.linesep)
    done = False
    validOptions = list(range(1,3))
    while not done:
        algoNum = int(input('Please choose your algorithm:' + os.linesep))
        done = algoNum in validOptions
        if not done:
            print('Invalid algorithm choice!')
    return algoNum

def GetPolicy(rewardDict, transitionDict, discountFactor, gridInfo):
    policyIteration = PolicyIterationAlgorithm(rewardDict, transitionDict, discountFactor, gridInfo)
    results = policyIteration.Run()
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

def Main(actualTransitionDict, discountFactor, epochLimit):
    while True:
        # Get world from user
        gridInfo = GetGridInfo()
        if gridInfo == None:
            sys.exit()
        # Get algorithm from user
        algorithm = GetAlgorithm()
        actualRewardDict = GetActualRewardDict(gridInfo)
        # Get policy for this world
        policy = GetPolicy(actualRewardDict, actualTransitionDict, discountFactor, gridInfo)
        newPolicy = None
        if algorithm == 2:
            adp = AdaptiveDynamicProgrammingAlgorithm(policy, epochLimit, discountFactor, gridInfo, actualRewardDict, actualTransitionDict)
            newPolicy = adp.Run()
        sequence = RunSimulation(newPolicy, gridInfo)
        PrintSequence(sequence)

Main(transitionDict, config['discountFactor'], config['epochLimit'])