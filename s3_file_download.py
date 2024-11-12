import boto3

def get_all_s3_objects(s3, **base_kwargs):
    continuation_token = None
    while True:
        list_kwargs = dict(MaxKeys=1000, **base_kwargs)
        if continuation_token:
            list_kwargs['ContinuationToken'] = continuation_token
        response = s3.list_objects_v2(**list_kwargs)
        yield from response.get('Contents', [])
        if not response.get('IsTruncated'):  # At the end of the list
            break
        continuation_token = response.get('NextContinuationToken')

s3_client = boto3.client('s3')

s3_bucket = ''
s3_becket_prefix = ''

for file in get_all_s3_objects(s3_client, Bucket=s3_bucket, Prefix=s3_becket_prefix):
    filename = file['Key'].split('/')[-1]

    # if you want to check the specific file name or file extension
    #if '' in file['Key']:
    #if filename.endswith(''):
    print(filename)
    s3_client.download_file(s3_bucket, file['Key'], f'./{filename}')
