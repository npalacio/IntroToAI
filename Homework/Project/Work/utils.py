import math
from datetime import datetime
from datetime import timedelta

def FilterColumns(df, columns):
    return df.filter(items=columns)

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
    df.drop_duplicates(keep='first' subset=columns, inplace=True)
    rowCountAfter = df.shape[0]
    print('Deleted ' + str(rowCountBefore - rowCountAfter) + ' duplicate rows')
# def CalculateWeatherDataHour(row):
#     year = str(row['Year'])
#     month = '%02d' % int(row['Month'])
#     day = '%02d' % int(row['Day'])
#     time = row['Time']
#     minutes = '%02d' % (time % 100)
#     hour = '%02d' % str(int(math.ceil(time / 100.0)))
#     # dateTime = datetime.strptime('2013 04 03 20 46 UTC', '%Y %m %d %H %M %Z')
#     dateTimeString = year + ' ' + month + ' ' + day + ' ' + 
#     dateTime = datetime.strptime('2013 04 03 20 46 UTC', '%Y %m %d %H %M %Z')
#     return hour