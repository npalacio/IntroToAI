from valueIteration import ValueIterationAlgorithm
config = {
    'gridInfo': {
        'width': 3,
        'height': 3,
        'defaultValue': -1,
        'rCell': (1,3),
        'rewardCells': {
            'cells': [(3,3)],
            'value': 10
        }
    },
    'discountFactor': .1
}

def GetTransitionDict():
    # {'U': [{'probability': .8, 'action': 'U'},{'probability': .1, 'action': 'L'}]}
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
    return transitionDict

def GetReward(cell, r, gridInfo):
    if cell == gridInfo['rCell']:
        return r
    elif cell in gridInfo['rewardCells']['cells']:
        return gridInfo['rewardCells']['value']
    return gridInfo['defaultValue']

def GetRewardDict(r, gridInfo):
    rewardDict = {}
    for col in range(gridInfo['width']):
        for row in range(gridInfo['height']):
            cell = (col + 1, row + 1)
            reward = GetReward(cell, r, gridInfo)
            rewardDict[cell] = reward
    return rewardDict

def GetAlgorithm():
    # TODO: flip back
    # algorithm = int(input('Enter 1 for Value Iteration, 2 for Policy Iteration, 3 to Exit: '))
    # return algorithm
    return 1

def GetR():
    # TODO: flip back
    # r = int(input('Enter r: '))
    # return r
    return -3

def Main(gridInfo, discountFactor):
    r = GetR()
    algorithm = GetAlgorithm()
    rewardDict = GetRewardDict(r, gridInfo)
    transitionDict = GetTransitionDict()
        # {(1,1): -.04}
    if algorithm == 1:
        valueIteration = ValueIterationAlgorithm(rewardDict, transitionDict, discountFactor, gridInfo)
        valueIteration.Run()

Main(config['gridInfo'], config['discountFactor'])