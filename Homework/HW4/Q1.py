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
                    'cell': (3,3),
                    'value': 1
                },
                {
                    'cell': (3,2),
                    'value': -1
                }
            ]
        }
    ],
    'discountFactor': .9,
    'epochLimit': 1000
}
# Need to get the policy
def GetWorld():
    # TODO: Get from user
    return config['gridInfos'][0]

def GetAlgorithm():
    # TODO: Get from user
    return 0

def GetPolicy():
    print('Implement')

def GetReward(cell, gridInfo):
    terminalCell = [cellObj for cellObj in gridInfo['terminalCells'] if cellObj['cell'] == cell]
    if len(terminalCell) > 0:
        return terminalCell['value']
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


def Main():
    # Get world from user
    gridInfo = GetWorld()
    # Get algorithm from user
    algorithm = GetAlgorithm()
    actualRewardDict = GetActualRewardDict(gridInfo)
    # Get policy for this world
    policy = GetPolicy()
    # Calculate utilities from algorithm and world

