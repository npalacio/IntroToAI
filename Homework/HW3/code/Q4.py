from valueIteration import ValueIterationAlgorithm
from policyIteration import PolicyIterationAlgorithm
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
    'discountFactor': .9
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
    algorithm = int(input('Enter 1 for Value Iteration, 2 for Policy Iteration, anything else to Exit: '))
    return algorithm

def GetR():
    r = int(input('Enter r: '))
    return r

def PrintPolicy(policy):
    print('Policy table calculated:')
    for state in sorted(policy):
        print(str(state) + ': ' + str(policy['state']))

def PrintUtilities(utils):
    print('Utilities:')
    for state in sorted(utils):
        print(str(state) + ': ' + str(round(utils['state'], 2)))

def PrintResults(results):
    PrintPolicy(results['policy'])
    PrintUtilities(results['expectedRewardDict'])

def Main(gridInfo, discountFactor):
    done = False
    while not done:
        r = GetR()
        algorithm = GetAlgorithm()
        rewardDict = GetRewardDict(r, gridInfo)
        transitionDict = GetTransitionDict()
        if algorithm == 1:
            valueIteration = ValueIterationAlgorithm(rewardDict, transitionDict, discountFactor, gridInfo)
            results = valueIteration.Run()
            PrintResults(results)
        elif algorithm == 2:
            policyIteration = PolicyIterationAlgorithm(rewardDict, transitionDict, discountFactor, gridInfo)
            results = policyIteration.Run()
            PrintResults(results)
        else:
            done = True

Main(config['gridInfo'], config['discountFactor'])