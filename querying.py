# Imports the Google Cloud client library
from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/bdebe/Documents/GIT/TAMIDS/datacompetition-71e5d3ebc025.json"

for x in range(10,78):
    currentCom = str(x)
    tableName = 'community_' + str(currentCom)

    try:
        client = bigquery.Client()
        dataset_ref = client.dataset('taxidataTest')
        table_ref = dataset_ref.table(tableName)
        client = bigquery.Client()
        query = """
            SELECT *
            FROM taxidataTest.2017
            WHERE Pickup_Community_Area = @currentCom
            """
        query_params = [
            bigquery.ScalarQueryParameter('currentCom', 'STRING', currentCom)
        ]
        job_config = bigquery.QueryJobConfig()
        job_config.query_parameters = query_params
        job_config.allow_large_results = True
        job_config.destination = table_ref
        job_config.write_disposition = 'WRITE_TRUNCATE'
        job = client.query(query, job_config=job_config)
        job.result()
    except:
        print("Issue with: " + currentCom + "--" + tableName)

    print ("COMPLETE: " + currentCom)