import pandas as pd
import random
import math
tmpConfig = {
    'dataPath': './hw3-crime_data.csv',
    'columns': ['Murder','Assault','UrbanPop','Rape']
}
class KMeans:
    def __init__(self, k, dataPath, columns):
        self.k = k
        self.dataPath = dataPath
        self.columns = columns

    def Run(self):
        # Pick k random centers (not from dataset? centroids?)
        data = LoadData(self.dataPath, self.columns)
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
                clusters = newClusters
        return newClusters

    def GetRandomCenters(self, k, data):
        randomDataIndices = random.sample(range(len(data)), k)
        randomCenters = [data[i] for i in randomDataIndices]
        return randomCenters
        
    def LoadData(self, csvPath, columns):
        # Should return [[],[],[],...] for data
        df = pd.read_csv(csvPath)
        df = df.filter(items=columns)
        return df.values.tolist()

    def GetClusters(self, data, centers):
        # get k lists of data keys
        centerCountArr = range(len(centers))
        clusters = [[] for center in centerCountArr]
        for dataIndex in range(len(data)):
            minDist = float("inf")
            bestClusterIndex = 0
            for centerIndex in centerCountArr:
                # See which center this data point belongs to
                dist = GetDistance(centers[centerIndex],data[dataIndex])
                bestClusterIndex = centerIndex if dist < minDist else bestClusterIndex
            # Assign data point to its closest cluster center
            clusters[bestClusterIndex].append(dataIndex)
        return clusters

    def GetDistance(self, point1, point2):
        featureCount = len(point1)
        euclidianDist = math.sqrt(sum([abs(point1[i] - point2[i]) ** 2 for i in range(featureCount)]))
        return euclidianDist

    def GetUpdatedCenters(self, clusters):
        # For each cluster, find its center
        newCenters = [[] for c in clusters]
        for clusterIndex in range(len(clusters)):
            currCluster = clusters[clusterIndex]
            featureTotals = [0 for x in currCluster[0]]
            rowCount = len(currCluster)
            for clusterDataIndex in range(rowCount):
                dataPoint = currCluster[clusterDataIndex]
                for featureIndex in range(len(dataPoint)):
                    # For each column, add it to the corresponding column total
                    featureTotals[featureIndex] = featureTotals[featureIndex] + dataPoint[featureIndex]
            newCenters[clusterIndex] = [featureTotal / rowCount for featureTotal in featureTotals]
        return newCenters

    def IsDone(self, oldClusters, newClusters):
        # We are done when the clusters are the same
        oldClusters = [set(cluster) for cluster in oldClusters]
        newClusters = [set(cluster) for cluster in newClusters]
        # We assume clusters are in same order
        for i in range(len(oldClusters)):
            areChanges = len(oldClusters[i].difference(newClusters[i])) != 0 or len(newClusters[i].difference(oldClusters[i])) != 0
            if areChanges:
                return False
        return True
