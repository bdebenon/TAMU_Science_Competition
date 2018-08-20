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

actualDict = {}
predictedDict = {}
for x in range(10,78):
    if (x < 10):
        communityNumber = "0" + str(x)
    else:
        communityNumber = "" + str(x)

    communityName = "community_" + communityNumber
    file_name = 'results/community_' + communityNumber + '.csv'
    df = pd.read_csv(file_name)

    dates = df['Date'].values
    actual = df['Actual'].values
    prediction = df['Prediction'].values

    x = 0
    for date in dates:
        if date in actualDict:
            actualDict[date] += actual[x]
            predictedDict[date] += prediction[x]
        else:
            actualDict[date] = actual[x]
            predictedDict[date] = prediction[x]
        x += 1

resultsActual = pd.DataFrame(list(actualDict.items()), columns=['Date', 'Actual'])
resultsPredicted = pd.DataFrame(list(predictedDict.items()), columns=['Date', 'Prediction'])

results = resultsActual.copy()
results['Prediction'] = resultsPredicted['Prediction']

file_name = 'OverallResults.csv'
results.to_csv(file_name, encoding='utf-8', index=False)

