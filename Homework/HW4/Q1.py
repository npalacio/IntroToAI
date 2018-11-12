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
            'width': 3,
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
    'discountFactor': .9
}
# Need to get the policy
def GetWorld():
    print('Implement')
def GetAlgorithm():
    print('Implement')
def GetPolicy():
    print('Implement')
def Main():
    # Get world from user
    world = GetWorld()
    # Get algorithm from user
    algorithm = GetAlgorithm()
    # Get policy for this world
    policy = GetPolicy()
    # Calculate utilities from algorithm and world

