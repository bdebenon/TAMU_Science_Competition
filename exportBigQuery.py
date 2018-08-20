from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/bdebe/Documents/GIT/TAMIDS/datacompetition-71e5d3ebc025.json"

client = bigquery.Client()
bucket_name = 'snappy-guard-200200'

for x in range(10,78):
    try:
        currentCom = str(x)
        tableName = 'community_' + str(currentCom)
        destinationName = 'testing_data/' + tableName + '.csv'
        destination_uri = 'gs://{}/{}'.format(bucket_name, destinationName)
        dataset_ref = client.dataset('taxidataTest')
        table_ref = dataset_ref.table(tableName)
        extract_job = client.extract_table(
            table_ref, destination_uri)  # API request
        extract_job.result()
        print("COMPLETE: " + currentCom)
    except:
        print("Issue with: " + currentCom + "--" + tableName)