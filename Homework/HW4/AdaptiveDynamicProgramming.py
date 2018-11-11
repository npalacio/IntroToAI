class AdaptiveDynamicProgramming:
    def __init__(self, policy, epochLimit):
        self.policy = policy
        self.epochLimit = epochLimit

    def Run():
        print('Implement')
        epochLimit = self.epochLimit
        iterationCount = 0
        while iterationCount < epochLimit:
            # What is an epoch here?

        # Figure out transition and reward functions
            # Keep track of how many times you did an action in a state as well as the resulting state each time
                # This is transition model
            # Every time you visit a state, record its reward = reward function
        # Using transition model, reward function and policy, calculate the utilities of each state
        # You keep on iterating over a number of epochs