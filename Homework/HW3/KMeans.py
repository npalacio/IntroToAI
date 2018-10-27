import pandas as pd
import random
# Will need to implement K-Means algorithm
# Will need to take in the dataset, K
class KMeans:
    def __init__(self, k):
        self.k = k
        self.dataPath = './hw3-crime_data.csv'

    def Run(self):
        # Pick k random centers (not from dataset? centroids?)
        data = LoadData(self.dataPath)
        centers = GetRandomCenters(self.k, data)

        # For each point, assign it to the cluster with the closest center
        clusters = GetClusters(data, centers)
        newClusters = []
        done = False
        while not done:
            # For each cluster, calculate a new centroid (center of that cluster)
            newCenters = GetUpdatedCenters(clusters)
            # For each point, assign it again to the cluster with the closest center
            newClusters = GetClusters(newCenters)
            # Stop when no cluster memberships change
            if IsDone(clusters, newClusters):
                done = True
            else:
                # Test
                clusters = newClusters
        return newClusters

    def GetRandomCenters(self, k, data):
        randomDataIndices = random.sample(range(len(data)), k)
        randomCenters = [data[i] for i in randomDataIndices]
        return randomCenters
        
    def LoadData(self, csvPath):
        # Should return [[],[],[],...] for data
        df = pd.read_csv(csvPath)
        df = df.filter(items=['Murder','Assault','UrbanPop','Rape'])
        return df.values.tolist()

    def GetClusters(self, data, centers):
        # get k lists of data keys
        for dataIndex in range(len(data)):
            for centerIndex in range(len(centers)):
                # See which center this data point belongs to

    def GetUpdatedCenters(self, clusters):
        print('Implement updating cluster centroids')

    def IsDone(self, oldClusters, newClusters):
        print('Implement is done')
