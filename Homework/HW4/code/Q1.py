from policyIteration import PolicyIterationAlgorithm
from AdaptiveDynamicProgramming import AdaptiveDynamicProgrammingAlgorithm

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
def GetGridInfo():
    # TODO: Get from user
    return config['gridInfos'][0]

def GetAlgorithm():
    # TODO: Get from user
    return 0

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

def GetStartingState():
    input('Please provide the starting state in the form of (column,row)')

def RunSimulation(policy):
    # Get starting point from user
    startingState = GetStartingState()
    # Follow policy until end

def Main(actualTransitionDict, discountFactor, epochLimit):
    # Get world from user
    gridInfo = GetGridInfo()
    # Get algorithm from user
    algorithm = GetAlgorithm()
    actualRewardDict = GetActualRewardDict(gridInfo)
    # Get policy for this world
    policy = GetPolicy(actualRewardDict, actualTransitionDict, discountFactor, gridInfo)
    newPolicy = None
    if algorithm == 0:
        adp = AdaptiveDynamicProgrammingAlgorithm(policy, epochLimit, discountFactor, gridInfo, actualRewardDict, actualTransitionDict)
        newPolicy = adp.Run()
    RunSimulation(newPolicy)

Main(transitionDict, config['discountFactor'], config['epochLimit'])