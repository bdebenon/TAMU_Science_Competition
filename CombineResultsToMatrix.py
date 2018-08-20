from google.cloud import storage
import pandas as pd
import numpy as np
import os
import io
import csv
import math


for x in range(1,6):
    communityNumber = "0" + str(x)
    communityName = "community_" + communityNumber
    error = ""
    try:
        dfA = pd.read_csv('exponentialMA/20ExpMA_community_' + communityNumber + '.csv')
        dfB = pd.read_csv('polynomialAverage/polynomial_community_' + communityNumber + '.csv')
        #dfC = pd.read_csv('ride_revenues/ride_revenues_community_' + communityNumber + '.csv')

        df = dfA.copy()
        df['Poly_Average'] = dfB['Poly_Average']
        #df['Revenue'] = dfC['Revenue']

        file_name = 'matrix/polynomial_community_' + communityNumber + '.csv'
        df.to_csv(file_name, encoding='utf-8', index=False)
    except:
        print('Failed with: ' + communityName + '. Received error: ' + error)
