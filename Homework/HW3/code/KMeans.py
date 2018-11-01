import csv
import random
import math

class KMeansAlgorithm:
    def __init__(self, k, dataPath, columns, labelColumn = []):
        self.k = k
        self.dataPath = dataPath
        self.columns = columns
        self.labelColumn = labelColumn

    def Run(self):
        # Pick k random centers (not from dataset? centroids?)
        data = self.LoadData(self.dataPath, self.columns, True)
        centers = self.GetRandomCenters(self.k, data)

        # For each point, assign it to the cluster with the closest center
        clusters = self.GetClusters(data, centers)
        newClusters = []
        done = False
        iterationCount = 0
        while not done:
            # For each cluster, calculate a new centroid (center of that cluster)
            newCenters = self.GetUpdatedCenters(data, clusters)
            # For each point, assign it again to the cluster with the closest center
            newClusters = self.GetClusters(data, newCenters)
            # Stop when no cluster memberships change
            if self.IsDone(clusters, newClusters):
                done = True
            else:
                clusters = newClusters
            iterationCount += 1
        # Need to calculate final distortion
        distortion = self.GetDistortion(data, newCenters, newClusters)
        actualLabels = self.LoadData(self.dataPath, self.labelColumn, False)
        return {
            'clusters': newClusters,
            'centers': newCenters,
            'distortion': distortion,
            'iterations': iterationCount,
            'actualLabels': actualLabels
        }

    def GetDistortion(self, data, centers, clusters):
        distortion = 0
        for clusterIndex in range(len(clusters)):
            center = centers[clusterIndex]
            cluster = clusters[clusterIndex]
            for dataIndex in range(len(cluster)):
                dataPoint = data[cluster[dataIndex]]
                distortion += abs(self.GetDistance(dataPoint, center) ** 2)
        return distortion

    def GetRandomCenters(self, k, data):
        randomDataIndices = random.sample(range(len(data)), k)
        randomCenters = [data[i] for i in randomDataIndices]
        return randomCenters
        
    def LoadData(self, csvPath, columnIndices, isNumeric):
        # Should return [[],[],[],...] for data
        with open(csvPath, 'r') as f:
            reader = csv.reader(f)
            your_list = list(reader)[1:]
        filteredList = []
        for row in your_list:
            newRow = []
            for index in columnIndices:
                if isNumeric:
                    newRow.append(float(row[index]))
                else:
                    newRow.append(row[index])
            filteredList.append(newRow)
        return filteredList

    def GetClusters(self, data, centers):
        # get k lists of data keys
        centerCountArr = range(len(centers))
        clusters = [[] for center in centerCountArr]
        for dataIndex in range(len(data)):
            minDist = float("inf")
            bestClusterIndex = 0
            for centerIndex in centerCountArr:
                # See which center this data point belongs to
                dist = self.GetDistance(centers[centerIndex],data[dataIndex])
                if dist < minDist:
                    bestClusterIndex = centerIndex
                    minDist = dist
            # Assign data point to its closest cluster center
            clusters[bestClusterIndex].append(dataIndex)
        return clusters

    def GetDistance(self, point1, point2):
        featureCount = len(point1)
        euclidianDist = math.sqrt(sum([abs(point1[i] - point2[i]) ** 2 for i in range(featureCount)]))
        return euclidianDist

    def GetUpdatedCenters(self, data, clusters):
        # For each cluster, find its center
        newCenters = [[] for c in clusters]
        for clusterIndex in range(len(clusters)):
            currCluster = clusters[clusterIndex]
            featureTotals = [0 for x in range(len(data[currCluster[0]]))]
            rowCount = len(currCluster)
            for clusterDataIndex in range(rowCount):
                dataPoint = data[currCluster[clusterDataIndex]]
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
