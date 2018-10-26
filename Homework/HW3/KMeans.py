# Will need to implement K-Means algorithm
# Will need to take in the dataset, K
class KMeans:
    def __init__(self, k):
        self.k = k

    def Run(self):
        print('empty run method')
        # Pick k random centers (not from dataset?)
        # For each point, assign it to the cluster with the closest center
        # Now we have initial clusters
        # For each cluster, calculate a new centroid (center of that cluster)
        # For each point, assign it again to the cluster with the closest center
        