from KMedoids import KMedoidsAlgorithm
from KMeans import KMeansAlgorithm

Config = {
    'dataPath': './irisData.csv',
    'columns': ['SepalLength','SepalWidth','PetalLength','PetalWidth'],
    'labelColumn': ['Label'],
    'k': 3
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

def GetRowsWithLabels(labels, clusters, centers, dataLabelDict):
    rowsWithLabels = []
    for clusterIndex in range(len(clusters)):
        centerDataIndex = centers[clusterIndex]
        # All of the points in this cluster get this label
        clusterLabel = labels[centerDataIndex][0]
        clusterDataIndices = clusters[clusterIndex]
        rowsWithLabels += GetActualLabels(clusterDataIndices, dataLabelDict, clusterLabel)
    return rowsWithLabels

def GetConfusionMatrix(labels, clusters, centers):
    dataLabelDict = GetLabelDictionary(labels)
    rowsWithLabels = GetRowsWithLabels(labels, clusters, centers, dataLabelDict)
    # [
    #   [labeledAs1Is1, labeledAs1Is2, labeledAs1Is3]
    #   [labeledAs2Is1, labeledAs2Is2, labeledAs2Is3]
    #   [labeledAs3Is1, labeledAs3Is2, labeledAs3Is3]
    # ]
    confusionMatrixWithPredictedAsKey = {}
    for predictedLabel in dataLabelDict:
        row = []
        for actualLabel in dataLabelDict:
            count = len([row for row in rowsWithLabels if row['predictedLabel'] == predictedLabel and row['actualLabel'] == actualLabel ])
            row.append(count)
        confusionMatrixWithPredictedAsKey[predictedLabel] = row
    return confusionMatrixWithPredictedAsKey

def PrintConfusionMatrix(confusionMatrix):
    columnWidth = 20
    topRow = ' ' * columnWidth
    rows = []
    for label in sorted(confusionMatrix):
        topRow += label.ljust(columnWidth)
        row = label.ljust(columnWidth) 
        for count in confusionMatrix[label]:
            row += str(count).ljust(columnWidth)
        rows.append(row)
    print(' ' * columnWidth * (1 + len(confusionMatrix) // 2) + 'Actual Labels')
    print(topRow)
    for stringRow in rows:
        print(stringRow)

def PrintResults(k, results):
    clusters = results['clusters']
    centers = results['centers']
    labels = results['actualLabels']
    confusionMatrix = GetConfusionMatrix(labels, clusters, centers)
    PrintConfusionMatrix(confusionMatrix)

def Main(k, dataPath, columns, labelColumn):
    print('Running with KMedoids...')
    kMedoid = KMedoidsAlgorithm(k, dataPath, columns, labelColumn)
    results = kMedoid.Run()
    PrintResults(k, results)
    print('Running with KMeans...')
    kMeans = KMeansAlgorithm(k, dataPath, columns, labelColumn)
    results = kMeans.Run()
    PrintResults(k, results)

Main(Config['k'], Config['dataPath'], Config['columns'], Config['labelColumn'])
