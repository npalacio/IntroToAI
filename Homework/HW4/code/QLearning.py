# Q(x,y) needs to be initialized somehow? Or we use a default value whenever it is undefined?
# while not over epoch limit
    # s = random starting state
    # while not done
        # pick action a that maximizes Q(s,a)
        # do action a, get next state s' and its reward r'
        # Q(s,a) = equation with update using Q(s,a) and Q(s',x) (and N(s) for learning rate?)
            # will need to find x that maximizes Q(s',x)
        # s = s'
        # done = s is terminal
    # iterate epoch limit
# End up with a filled out Q(s,a) that can be used to calculate a policy (pick action at state s that maximizes Q)

# while not over epoch limit
    # s = null (prev state)
    # pick random starting state s'
    # while not done
        # pick action a that maximizes Q(s',a)
        # do action a, get next state s'' and its reward r''
        # update Q(s',a) with its previous value + max of Q(s'',x) - Q(s',a)
            # will need to iterate over the actions in s' to get best q value
        # s = s'