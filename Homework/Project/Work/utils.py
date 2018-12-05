import math
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta

from sklearn import metrics

def FilterColumns(df, columns):
    return df.filter(items=columns)

def InitializeNewColumnDict(columnInfoDictArr):
    newColumnDataDict = {}
    for colDict in columnInfoDictArr:
        newColumnDataDict[colDict['name']] = []
    return newColumnDataDict

def AddNewColumnData(row, columnInfoDictArr, newColumnDataDict):
    for colDict in columnInfoDictArr:
        name = colDict['name']
        newValue = ConvertToNumeric(row, name, colDict['valuesToHandle'], colDict['defaultValue'])
        newColumnDataDict[name].append(newValue)

def UpdateDfColumns(df, newColumnDataDict):
    for key in newColumnDataDict:
        df[key] = pd.Series(newColumnDataDict[key])
    return df

def ConvertColumnsToNumeric(df, columnInfoDict):
    newColumnDataDict =  InitializeNewColumnDict(columnInfoDict)
    df.apply(lambda row: AddNewColumnData(row, columnInfoDict, newColumnDataDict),axis=1)
    df = UpdateDfColumns(df, newColumnDataDict)
    return df

def ConvertColumnToNumeric(df, column, valuesToHandle, defaultValue):
    df[column] = df.apply(lambda row: ConvertToNumeric(row, column, valuesToHandle, defaultValue),axis=1)
    return df

def ConvertToNumeric(row, column, valuesToHandle, defaultValue):
    value = row[column]
    if value in valuesToHandle:
        value = defaultValue
    return float(value)

def CalculateWeatherDataYear(row):
    dateTime = GetDateTime(row)
    return dateTime.year

def CalculateWeatherDataMonth(row):
    dateTime = GetDateTime(row)
    return dateTime.month

def CalculateWeatherDataDay(row):
    dateTime = GetDateTime(row)
    return dateTime.day

def CalculateWeatherDataHour(row):
    dateTime = GetDateTime(row)
    return dateTime.hour

def GetDateTime(row):
    year = int(row['Year'])
    month = int(row['Month'])
    day = int(row['Day'])
    time = row['Time']
    minute = time % 100
    hour = int(math.floor(time / 100.0))
    # print(str(hour))
    dateTime = datetime(year, month, day, hour, minute) + timedelta(hours=int(row['TimeZone']))
    return dateTime

def CalculateFlightDataHour(row):
    time = row['CRSDepTime']
    hour = int(math.floor(time / 100.0))
    return hour

def DropDuplicates(df, columns):
    rowCountBefore = df.shape[0]
    df.drop_duplicates(keep='first', subset=columns, inplace=True)
    rowCountAfter = df.shape[0]
    print('Deleted ' + str(rowCountBefore - rowCountAfter) + ' duplicate rows')

def FillInMissingNumericValues(df, columnName, defaultValue):
    rowCountBefore = df.loc[(df[columnName].isnull())].shape[0]
    df[columnName].fillna(defaultValue, inplace=True)
    rowCountAfter = df.loc[(df[columnName].isnull())].shape[0]
    print('Filled in ' + str(rowCountBefore - rowCountAfter) + ' missing values for ' + columnName)

def UpdateComparisonDict(comparisonDict, testingLabelData, predictedLabelData):
    comparisonDict['MeanAbsErr'].append(metrics.mean_absolute_error(testingLabelData, predictedLabelData))
    comparisonDict['MeanSquErr'].append(metrics.mean_squared_error(testingLabelData, predictedLabelData))
    comparisonDict['RootMeanSquErr'].append(np.sqrt(metrics.mean_squared_error(testingLabelData, predictedLabelData)))
    return comparisonDict

weatherData = pd.read_csv('./Weather Data.csv', nrows=100)
colInfoDict = [{
    'name': 'Visibility',
    'valuesToHandle': ['M'],
    'defaultValue': 0
}]
ConvertColumnsToNumeric(weatherData, colInfoDict)