from KMedoids import KMedoidsAlgorithm

Config = {
    'dataPath': './irisData.csv',
    'columns': ['SepalLength','SepalWidth','PetalLength','PetalWidth'],
    'labelColumn': ['Label'],
    'kValues': [3]
}

def PrintResults(k, results):
    clusters = results['clusters']
    centers = results['centers']
    labels = results['actualLabels']
    distinctLabels = list(set([label for l in labels for label in l]))
    dataLabelDict = {}
    for label in distinctLabels:
        labelRows = []
        # Get list of all actual rows for this label
        for dataIndex in range(len(labels)):
            if labels[dataIndex] == label:
                labelRows.append(dataIndex)
        dataLabelDict[label] = labelRows
    # Get list of all rows we predicted as this label
    for clusterIndex in range(len(clusters)):
        centerDataIndex = centers[clusterIndex]
        centerLabel = labels[centerDataIndex]
        cluster = clusters[clusterIndex]

def Main(kVals, dataPath, columns, labelColumn):
    for k in kVals:
        kMedoid = KMedoidsAlgorithm(k, dataPath, columns, labelColumn)
        results = kMedoid.Run()
        PrintResults(k, results)

Main(Config['kValues'], Config['dataPath'], Config['columns'], Config['labelColumn'])
