import csv
import math

class KMedoidsAlgorithm:
    def __init__(self, k, dataPath, columns, labelColumn):
        self.k = k
        self.dataPath = dataPath
        self.columns = columns
        self.labelColumn = labelColumn

    def Run(self):
        data = self.LoadData(self.dataPath, self.columns, True)
        # Pick k random data members as starting centers
        centers = self.GetInitialCenters(self.k, data)
        # For each point, assign it to the cluster with the closest center
        clusters = self.GetClusters(data, centers)
        totalDistance = self.GetTotalDistance(data, centers, clusters)
        done = False
        while not done:
            # New centers should be within each cluster, the data point that minimizes total distance
            newCenters = self.GetNewCenters(data, clusters)
            newClusters = self.GetClusters(data, newCenters)
            newTotalDistance = self.GetTotalDistance(data, newCenters, newClusters)
            # print('Cluster 1 = ' + str(len(newClusters[0])))
            # print('Cluster 2 = ' + str(len(newClusters[1])))
            # print('Cluster 3 = ' + str(len(newClusters[2])))
            # print()
            if self.IsDone(totalDistance, newTotalDistance):
                done = True
            else:
                clusters = newClusters
                totalDistance = newTotalDistance
        actualLabels = self.LoadData(self.dataPath, self.labelColumn, False)
        return {
            'clusters': newClusters,
            'centers': newCenters,
            'actualLabels': actualLabels
        }

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

    def GetInitialCenters(self, k, data):
        # Find the k data points with the smallest total distance ratios to the other data points
        dataRange = range(len(data))
        distanceRatios = [0 for x in dataRange]
        D = self.GetD(data)
        distanceRatios = self.GetDistanceRatios(data, D)
        sortedDistanceRatios = sorted(distanceRatios, key=lambda k: k['distanceRatio'])
        return [dataPoint['index'] for dataPoint in sortedDistanceRatios[:k]]

    def GetD(self, data):
        D = 0
        for currDataIndex in range(len(data) - 1):
            for nextDataIndex in range(currDataIndex + 1, len(data)):
                D += self.GetEuclidianDistance(data[currDataIndex], data[nextDataIndex])
        return D

        
    def GetDistanceRatios(self, data, D):
        dataRange = range(len(data))
        distanceRatios = [{'index': 0, 'distanceRatio': 0} for x in dataRange]
        for dataPointIndex in dataRange:
            dataPoint = data[dataPointIndex]
            distanceRatio = sum([self.GetEuclidianDistance(dataPoint, otherDataPoint) / D for otherDataPoint in data])
            distanceRatios[dataPointIndex] = {'index': dataPointIndex, 'distanceRatio': distanceRatio}
        return distanceRatios

    def GetEuclidianDistance(self, point1, point2):
        featureCount = len(point1)
        euclidianDist = math.sqrt(sum([abs(point1[i] - point2[i]) ** 2 for i in range(featureCount)]))
        return euclidianDist

    def GetClusters(self, data, centers):
        # get k lists of data keys
        centerCountArr = range(len(centers))
        clusters = [[] for center in centerCountArr]
        for dataIndex in range(len(data)):
            minDist = float("inf")
            bestClusterIndex = 0
            for centerIndex in centerCountArr:
                # See which center this data point belongs to
                dist = self.GetEuclidianDistance(data[centers[centerIndex]],data[dataIndex])
                if dist < minDist:
                    bestClusterIndex = centerIndex
                    minDist = dist
            # Assign data point to its closest cluster center
            clusters[bestClusterIndex].append(dataIndex)
        return clusters

    def GetTotalDistance(self, data, centers, clusters):
        # This is sum of all cluster objects to their cluster centers
        totalDistance = 0
        for clusterIndex in range(len(clusters)):
            cluster = clusters[clusterIndex]
            clusterCenter = data[centers[clusterIndex]]
            for clusterMemberDataIndex in cluster:
                clusterMember = data[clusterMemberDataIndex]
                totalDistance += self.GetEuclidianDistance(clusterCenter, clusterMember)
        return totalDistance

    def GetNewCenters(self, data, clusters):
        # For each cluster, pick a new data member to be the center
        newCenters = [0 for x in range(len(clusters))]
        for clusterIndex in range(len(clusters)):
            clusterMemberDataIndices = clusters[clusterIndex]
            minDist = float('inf')
            bestCenterIndex = 0
            for memberDataIndex in clusterMemberDataIndices:
                # See what the total distance would be if this were the cluster center
                dist = self.GetClusterDistance(data, memberDataIndex, clusterMemberDataIndices)
                if dist < minDist:
                    # We have a new best cluster center
                    bestCenterIndex = memberDataIndex
            newCenters[clusterIndex] = bestCenterIndex
        return newCenters

    def GetClusterDistance(self, data, centerDataIndex, clusterMemberDataIndices):
        clusterDistance = 0
        center = data[centerDataIndex]
        for memberDataIndex in clusterMemberDataIndices:
            member = data[memberDataIndex]
            clusterDistance += self.GetEuclidianDistance(center, member)
        return clusterDistance

    def IsDone(self, previousDist, newDist):
        return previousDist == newDist
