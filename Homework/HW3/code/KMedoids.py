# Will need to implement K-Medoids algorithm
class KMedoids:
    def __init__(self, k):
        self.k = k
        self.dataPath = dataPath
        self.columns = columns

    def Run(self):
        print('empty run method')
        data = self.LoadData(self.dataPath, self.columns)
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
            if self.IsDone(totalDistance, newTotalDistance):
                done = True
            else:
                clusters = newClusters

    def LoadData(self, csvPath, columns):
        # Should return [[],[],[],...] for data
        df = pd.read_csv(csvPath)
        df = df.filter(items=columns)
        return df.values.tolist()

    def GetInitialCenters(self, k, data):
        # Find the k data points with the smallest total distance ratios to the other data points
        dataRange = range(len(data))
        distanceRatios = [0 for x in dataRange]
        D = self.GetD(data)
        distanceRatios = self.GetDistanceRatios(data)
        distanceRatios.sort()
        return distanceRatios[:k]

    def GetD(self, data):
        
    def GetDistanceRatios(self, data, D):
        dataRange = range(len(data))
        distanceRatios = [0 for x in dataRange]
        for dataPointIndex in dataRange:
            dataPoint = data[dataPointIndex]
            distanceRatio = sum([self.GetEuclidianDistance(dataPoint, otherDataPoint) / D for otherDataPoint in data])
            distanceRatios[dataPointIndex] = distanceRatio
        return distanceRatios

    def GetEuclidianDistance(self, point1, point2):
        featureCount = len(point1)
        euclidianDist = math.sqrt(sum([abs(point1[i] - point2[i]) ** 2 for i in range(featureCount)]))
        return euclidianDist

    def GetClusters(self, data, centers):
    def GetTotalDistance(self, data, centers, clusters):
    def GetNewCenters(self, data, centers, clusters):
    def IsDone(self, previousDist, newDist):
