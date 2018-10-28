from KMedoids import KMedoidsAlgorithm

Config = {
    'dataPath': './irisData.csv',
    'columns': ['SepalLength','SepalWidth','PetalLength','PetalWidth'],
    'labelColumn': ['Label'],
    'kValues': [3]
}

def Main(kVals, dataPath, columns, labelColumn):
    for k in kVals:
        kMeans = KMeansAlgorithm(k, dataPath, columns)
        results = kMeans.Run()
        PrintResults(k, results)

Main(Config['kValues'], Config['dataPath'], Config['columns'], Config['labelColumn'])
