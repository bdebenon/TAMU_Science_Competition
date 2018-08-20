from google.cloud import storage
import pandas as pd
import numpy as np
import os
import io
import csv
import math


for x in range(1,10):
    communityNumber = "0" + str(x)
    communityName = "community_" + communityNumber
    error = ""
    try:
        df = pd.read_csv('exponentialMA/20ExpMA_community_' + communityNumber + '.csv')
        fits = df.copy()
        days = df['Day'].tolist()
        rides = df['20_ExpMA'].tolist()
        #print (str(len(days)) + ':' + str(len(rides)))
        #print (days[-10:])
        #print (rides[-10:])
        secondCoeff = np.polyfit(days, rides, 2)
        fourthCoeff = np.polyfit(days, rides, 4)

        predictedAverages = []

        for x in range(len(days) + 1, len(days) + 1 + 365 + 1):
            second = secondCoeff[2] + secondCoeff[1] * pow(x, 1) + secondCoeff[0] * pow(x, 2)
            fourth = fourthCoeff[4] + fourthCoeff[3] * pow(x, 1) + fourthCoeff[2] * pow(x, 2) + \
                     fourthCoeff[1] * pow(x, 3) + fourthCoeff[0] * pow(x, 4)
            average = (second + fourth) / 2
            # print (str(average) + ':' + str(rides[x - 1]))
            predictedAverages.append(average)

        df2 = pd.read_csv('test_ride_occurrences/ride_occurrences_community_' + communityNumber + '.csv')
        predictedDf = pd.DataFrame()
        predictedDf['Date'] = df2['Date']
        predictedDf['Predicted_Poly'] = predictedAverages[:predictedDf['Date'].count()]

        file_name = 'predicted20ExpMAAverage/20ExpMA_polynomial_community_' + communityNumber + '.csv'
        predictedDf.to_csv(file_name, encoding='utf-8', index=False)

    except:
        print('Failed with: ' + communityName + '. Received error: ' + error)