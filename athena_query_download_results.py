import boto3
import time

athena_output_s3_bucket = ''

athena = boto3.client("athena")

sql_script = ''
database_name = ''

response = athena.start_query_execution(
    QueryString=sql_script,
    QueryExecutionContext={"Database": database_name},
    ResultConfiguration={
        "OutputLocation": f"s3://{athena_output_s3_bucket}/",
        "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},
    },
)

# Get the query execution ID
query_execution_id = response['QueryExecutionId']

# Wait for the query to complete
while True:
    query_status = athena.get_query_execution(QueryExecutionId=query_execution_id)[
        'QueryExecution']['Status']
    if query_status['State'] == 'SUCCEEDED':
        break
    else:
        if query_status['State'] not in ('QUEUED', 'RUNNING'):
            raise Exception(f"Query execution failed. Status: {query_status['State']} with error: {query_status['StateChangeReason']}")
    time.sleep(0.001)

#download the results
s3_client = boto3.client(
        "s3"
    )
print(f'{response["QueryExecutionId"]}.csv')
s3_client.download_file(athena_output_s3_bucket, f'{response["QueryExecutionId"]}.csv', f'./{response["QueryExecutionId"]}.csv')
