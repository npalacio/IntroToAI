from KMeans import KMeansAlgorithm

Config = {
    'dataPath': './hw3-crime_data.csv',
    'columns': ['Murder','Assault','UrbanPop','Rape'],
    'kValues': [2,3,4,5,6]
}

def PrintResults(k, results):
    print('K = ' + str(k) + ', distortion = ' + str(int(results['distortion'])) + ', iterations = ' + str(results['iterations']))

def Main(kVals, dataPath, columns):
    for k in kVals:
        kMeans = KMeansAlgorithm(k, dataPath, columns)
        results = kMeans.Run()
        PrintResults(k, results)

Main(Config['kValues'], Config['dataPath'], Config['columns'])