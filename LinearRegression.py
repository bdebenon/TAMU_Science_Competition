from google.cloud import storage
import pandas as pd
import numpy as np
import os
import io
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

for x in range(1,6):
    communityNumber = "0" + str(x)
    communityName = "community_" + communityNumber
    error = ""
    #try:
    file_name = 'matrix/polynomial_community_' + communityNumber + '.csv'
    df = pd.read_csv(file_name)
    #xdf = df[['20_ExpMA', 'Poly_Average']]
    xdf = df[['20_ExpMA', 'Poly_Average', 'Revenue']]

    file_name = 'ride_occurrences/ride_occurrences_community_' + communityNumber + '.csv'
    df2 = pd.read_csv(file_name)
    ydf = df2['Rides']

    file_name = 'test_ride_occurrences/ride_occurrences_community_' + communityNumber + '.csv'
    df3 = pd.read_csv(file_name)
    xLength = df3['Rides'].count()

    file_name = 'predictedPolynomialAverage/polynomial_community_' + communityNumber + '.csv'
    df4 = pd.read_csv(file_name)

    file_name = 'predicted20ExpMAAverage/20ExpMA_polynomial_community_' + communityNumber + '.csv'
    df5 = pd.read_csv(file_name)

    file_name = 'predictedRevenue/revenue_polynomial_community_' + communityNumber + '.csv'
    df6 = pd.read_csv(file_name)

    X = pd.DataFrame()
    X['EXP_Predicted_Poly'] = df5['Predicted_Poly']
    X['Predicted_Poly'] = df4['Predicted_Poly']
    X['Revenue_Predicted_Poly'] = df6['Revenue_Predicted_Poly']

    lm = LinearRegression()
    print (xdf.head(5))
    print (xdf.tail(5))
    lm.fit(xdf.values, ydf.values)
    dfResults = pd.DataFrame()
    dfResults['Date'] = df3['Date']
    dfResults['Actual'] = df3['Rides']
    dfResults['Prediction'] = lm.predict(X)
    #print (dfResults.head(10))
    #print (dfResults.tail(10))

    file_name = 'results/revenueRuns/community_' + communityNumber + '.csv'
    dfResults.to_csv(file_name, encoding='utf-8', index=False)
    #except:
    #    print('Failed with: ' + communityName + '. Received error: ' + error)
