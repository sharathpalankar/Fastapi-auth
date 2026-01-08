import boto3

s3=boto3.client('s3')
bucket_name = "myfirstawsbucket-sharu"

# print(s3.list_buckets())