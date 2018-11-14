# Initialize dicts for state --> # of times visited
# Initialize utility dict just as blank dict
# while not over epoch limit
    # s = random starting state
    # while not done
        # N(s)++
        # If you have not been to s before, initialize its utility
            # Utility = its reward
        # s' = simulate move while at s using input policy
            # We use transition model which means we randomly stray from path
        # U(s) = equation with update using U(s') and N(s)
            # if U(s') is undefined, initialize it to reward of s'
        # s = s'
        # done = s is terminal
    # iterate epoch limit
# End up with a filled out U(s)


# Initialize dicts for state --> # of times visited
# Initialize utility dict just as blank dict
# while not over epoch limit
    # s = null
    # s' = random starting state
    # while not done
        # done = s' is a terminal state
        # N(s')++
        # If you have not been to s' before, initialize its utility
            # Utility = its reward
        # If your previous state (s) is not null
            # U(s) = equation with update using U(s') and N(s)
        # s = s'
        # s' = simulate move while at s' using input policy