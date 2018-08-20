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
        df = pd.read_csv('ride_occurrences/ride_occurrences_community_' + communityNumber + '.csv')
        window = 20
        df['20_ExpMA'] = pd.stats.moments.ewma(df['Rides'], span = window)
        file_name = 'exponentialMA/20ExpMA_community_' + communityNumber + '.csv'
        df.to_csv(file_name, encoding='utf-8', index=False)

    except:
        print('Failed with: ' + communityName + '. Received error: ' + error)