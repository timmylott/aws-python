import boto3
import datetime


def get_all_s3_object_versions(s3, **base_kwargs):
    versionidmarker = None
    keymarker = None
    while True:
        list_kwargs = dict(MaxKeys=1000, **base_kwargs)
        if versionidmarker:
            list_kwargs['VersionIdMarker'] = versionidmarker
            list_kwargs['KeyMarker'] = keymarker
        response = s3.list_object_versions(**list_kwargs)
        yield from response.get('Versions', [])  # change this to DeleteMarkers if you want that
        if not response.get('IsTruncated'):  # At the end of the list
            break
        versionidmarker = response.get('NextVersionIdMarker')
        keymarker = response.get('NextKeyMarker')


s3_client = boto3.client('s3')
bucket = ''
prefix = ''

for version in get_all_s3_object_versions(s3_client, Bucket=bucket,
                                          Prefix=prefix):
    # this is looking for specific file version based on a date
    if datetime.datetime.strptime('2024-11-05 +0000', '%Y-%m-%d %z') <= version['LastModified'] <= datetime.datetime.strptime('2024-11-06 +0000', '%Y-%m-%d %z'):
        if '_temporary' not in version['Key']:
            print(version['Key'])
            filename = version['Key'].split('/')[-1]
            s3_client.download_file(bucket, version['Key'],
                                    f'./{filename}', ExtraArgs={"VersionId": version['VersionId']})
