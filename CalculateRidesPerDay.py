from google.cloud import storage
import pandas as pd
import os
import io
import csv
import math
import sys

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/bdebe/Documents/GIT/TAMIDS/datacompetition-301e5b3cf3fc.json"
for x in range(0, 3):
    error = ""
    communityNumber = "00000000000" + str(x)
    communityName = "community_08_" + communityNumber
#try:
    client = storage.Client()
    bucket = client.get_bucket('snappy-guard-200200')
    blob = storage.Blob('testing_data/community_08_' + communityNumber + '.csv', bucket)
    #blob = storage.Blob('testing_data/community_' + communityNumber + '.csv', bucket)
    content = blob.download_as_string()

    #Create DataFrame from 'content' pulled from GCloud Storage
    df = pd.read_csv(io.StringIO(content.decode('utf-8')), dtype='unicode')

    #Grab the Trip_Start_Timestamp column only
    dfTimeStamp = df['Trip_Start_Timestamp']

    #Convert the dfTimeStamp dataframe to a list
    datesOfRides = dfTimeStamp.tolist()

    #Convert Timestamp to Year/Month/Date Format
    dailyNumRides = {}

    #Count the number of ride occurrences for each day
    for day in datesOfRides:
        #Convert Timestamp to Year/Month/Date Format
        clippedDay = day[:10]
        splitDay = clippedDay.split('/')
        key = (splitDay[2] + '-' + splitDay[0] + '-' + splitDay[1])
        if key in dailyNumRides:
            dailyNumRides[key] += 1
        else:
            #print (key)
            dailyNumRides[key] = 1

    #Sort the occurrences from low to high for IQR Calculations
    sortedValues = sorted(dailyNumRides.values())

    #Initialize Low/High Values -> Min and Max values kept in set
    lowValue = None
    highValue = None

    #Calcualte IQR (We don't distinguish between even and odd data sets because the midpoint/firstQuartile/thirdQuartile
    #Being 1 spot off is very meaningless in this context
    length = len(sortedValues)
    midPoint = (length - 1)/2
    lowPoint = int(midPoint/2)
    highPoint = int(midPoint * 1.5)
    firstQuartile = sortedValues[lowPoint]
    thirdQuartile = sortedValues[highPoint]
    IQR = thirdQuartile - firstQuartile
    lowValue = firstQuartile - 1.5*IQR
    highValue = thirdQuartile + 1.5*IQR
    #print ("Lowest kept value: " + str(lowValue))
    #print ("Highest kept value: " + str(highValue))
    #print ("Calculated IQR: " + str(IQR))

    #Find all of the outliers
    outlierKeys = []
    #print ("Before: " + str(len(dailyNumRides)))
    before = len(dailyNumRides)
    for entry in dailyNumRides:
        if dailyNumRides[entry] < lowValue or dailyNumRides[entry] > highValue:
            outlierKeys.append(entry)

    #Delete all of the outliers
    for entry in outlierKeys:
        #print ("Deleting: " + str(dailyNumRides[entry]))
        del dailyNumRides[entry]

    #Calculate number of deleted occurrences for the sake of data info
    after = len(dailyNumRides)
    deleted = before - after
    #print ("Total deleted outliers: " + str(deleted))

    #Export to CSV
    #outfile = open('test_ride_occurrences/ride_occurrences_community_' + communityNumber + '.csv','w')
    outfile = open('test_ride_occurrences/ride_occurrences_community_08_' + communityNumber + '.csv', 'w')
    x = 1
    outfile.write('Day,Date,Rides\n' )
    for key, value in sorted(dailyNumRides.items()):
        outfile.write(str(x) + ',' + str(key) + ',' + str(value) + '\n' )
        x+=1
#except:
#    print('Failed with: ' + communityName + '. Recieved error: ' + error)
#    e = sys.exc_info()[0]
#    print("Error: %s" % e)