# Will need to implement K-Medoids algorithm
class KMedoids:
    def __init__(self, k):
        self.k = k

    def Run(self):
        print('empty run method')
        # Pick k random data members as starting centers
        # For each point, assign it to the cluster with the closest center
        # For each cluster center, for each cluster member,
            # swap the center and the member
            # recalculate the total distances of each cluster member to its center
                # If total cost improved, do the swap, otherwise undo it (how do we do this while inside the loops?)
