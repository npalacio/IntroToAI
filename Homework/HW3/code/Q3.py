from KMedoids import KMedoidsAlgorithm

Config = {
    'dataPath': './irisData.csv',
    'columns': ['SepalLength','SepalWidth','PetalLength','PetalWidth'],
    'labelColumn': ['Label'],
    'kValues': [3]
}

def GetLabelDictionary(labels):
    distinctLabels = list(set([label for l in labels for label in l]))
    dataLabelDict = {}
    for label in distinctLabels:
        labelRows = []
        # Get list of all actual rows for this label
        for dataIndex in range(len(labels)):
            if labels[dataIndex][0] == label:
                labelRows.append(dataIndex)
        dataLabelDict[label] = labelRows
    return dataLabelDict

def GetActualLabels(clusterDataIndices, dataLabelDict, clusterLabel):
    rowsWithLabels = []
    for memberDataIndex in clusterDataIndices:
        for label in dataLabelDict:
            if memberDataIndex in dataLabelDict[label]:
                rowsWithLabels.append({
                    'dataIndex': memberDataIndex,
                    'predictedLabel': clusterLabel,
                    'actualLabel': label
                })
    return rowsWithLabels

def GetConfusionMatrix(labels, clusters, centers):
    dataLabelDict = GetLabelDictionary(labels)
    # Get list of all rows we predicted as this label
    for clusterIndex in range(len(clusters)):
        centerDataIndex = centers[clusterIndex]
        # All of the points in this cluster get this label
        clusterLabel = labels[centerDataIndex][0]
        clusterDataIndices = clusters[clusterIndex]
        rowsWithLabels = GetActualLabels(clusterDataIndices, dataLabelDict, clusterLabel)

def PrintResults(k, results):
    clusters = results['clusters']
    centers = results['centers']
    labels = results['actualLabels']
    confusionMatrix = GetConfusionMatrix(labels, clusters, centers)

def Main(kVals, dataPath, columns, labelColumn):
    for k in kVals:
        kMedoid = KMedoidsAlgorithm(k, dataPath, columns, labelColumn)
        results = kMedoid.Run()
        PrintResults(k, results)

Main(Config['kValues'], Config['dataPath'], Config['columns'], Config['labelColumn'])
