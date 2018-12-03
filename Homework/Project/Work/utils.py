import math
from datetime import datetime

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

def CalculateWeatherDataHour(row):
    year = str(row['Year'])
    month = '%02d' % int(row['Month'])
    day = '%02d' % int(row['Day'])
    time = row['Time']
    minutes = '%02d' % (time % 100)
    hour = '%02d' % str(int(math.ceil(time / 100.0)))
    # dateTime = datetime.strptime('2013 04 03 20 46 UTC', '%Y %m %d %H %M %Z')
    dateTimeString = year + ' ' + month + ' ' + day + ' ' + 
    dateTime = datetime.strptime('2013 04 03 20 46 UTC', '%Y %m %d %H %M %Z')
    return hour
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