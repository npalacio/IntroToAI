class DirectUtilEstimation:
    def __init__(self, policy):
        self.policy = policy

    def Run():
        print('Implement')
        # Iterate over number of epochs? 1 epoch = start at a state and follow policy until terminal state
        # How do we pick which states to start at?
        # Pick random state as the starting state
            # Follow the policy from starting state until terminal state, keep track of reward
            # Store final reward for this starting state (keep running average for each starting state)
        # Return the utilities as the average for each state