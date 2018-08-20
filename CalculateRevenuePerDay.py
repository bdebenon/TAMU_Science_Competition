from google.cloud import storage
import pandas as pd
import os
import io
import csv
import math
import sys

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/bdebe/Documents/GIT/TAMIDS/datacompetition-301e5b3cf3fc.json"
for x in range(1,10):
    error = ""
    communityNumber = "0" + str(x)
    communityName = "community_" + communityNumber
    try:
        client = storage.Client()
        bucket = client.get_bucket('snappy-guard-200200')
        blob = storage.Blob('training_data/community_' + communityNumber + '.csv', bucket)
        #blob = storage.Blob('testing_data/community_' + communityNumber + '.csv', bucket)
        content = blob.download_as_string()

        #Create DataFrame from 'content' pulled from GCloud Storage
        df = pd.read_csv(io.StringIO(content.decode('utf-8')), dtype='unicode')

        #Grab the appropriate columns only
        dfRevenueInfo = df[['Trip_Start_Timestamp','Trip_Total','Payment_Type']]

        #Convert the dfTimeStamp dataframe to a list
        datesOfRides = dfRevenueInfo['Trip_Start_Timestamp'].tolist()
        trip_total = dfRevenueInfo['Trip_Total'].tolist()
        payment_type = dfRevenueInfo['Payment_Type'].tolist()

        #Convert Timestamp to Year/Month/Date Format
        dailyRevenue = {}

        #Count the amount of revenue for each day
        x = 0
        for day in datesOfRides:
            #Convert Timestamp to Year/Month/Date Format
            clippedDay = day[:10]
            splitDay = clippedDay.split('/')
            key = (splitDay[2] + '-' + splitDay[0] + '-' + splitDay[1])

            #This compensates for the errors in the data where the total_payment got shifted to teh payment_type column
            if (pd.isnull(payment_type[x])):
                revenue = trip_total[x]
            else:
                if payment_type[x].isdigit():
                    revenue = payment_type[x]
                else:
                    revenue = trip_total[x]

            #Convert the string revenue into float revenue (numeric format)
            if(pd.isnull(revenue)):
                floatRevenue = 0.0
            else:
                floatRevenue = float(revenue[1:])

            #Add revenue to associated day
            if key in dailyRevenue:
                dailyRevenue[key] += floatRevenue
            else:
                dailyRevenue[key] = floatRevenue
            x += 1

        #Sort the occurrences from low to high for IQR Calculations
        sortedValues = sorted(dailyRevenue.values())

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
        #lowValue = firstQuartile - 1.5*IQR
        lowValue = 0.50 #Remove all invalid 0 entries
        highValue = thirdQuartile + 1.5*IQR
        #print ("Lowest kept value: " + str(lowValue))
        #print ("Highest kept value: " + str(highValue))
        #print ("Calculated IQR: " + str(IQR))

        #Find all of the outliers
        outlierKeys = []
        #print ("Before: " + str(len(dailyRevenue)))
        before = len(dailyRevenue)
        for entry in dailyRevenue:
            if dailyRevenue[entry] < lowValue or dailyRevenue[entry] > highValue:
                outlierKeys.append(entry)

        #Delete all of the outliers
        for entry in outlierKeys:
            #print ("Deleting: " + str(dailyRevenue[entry]))
            del dailyRevenue[entry]

        #Calculate number of deleted occurrences for the sake of data info
        after = len(dailyRevenue)
        deleted = before - after
        #print ("Total deleted outliers: " + str(deleted))

        #Export to CSV
        outfile = open('ride_revenues/ride_revenues_community_' + communityNumber + '.csv','w')
        x = 1
        outfile.write('Day,Date,Revenue\n' )
        for key, value in sorted(dailyRevenue.items()):
            outfile.write(str(x) + ',' + str(key) + ',' + str(value) + '\n' )
            x+=1
        print ("Success: " + communityName)
    except:
        print('Failed with: ' + communityName + '. Recieved error: ' + error)
        #e = sys.exc_info()[0]
        #print("Error: %s" % e)