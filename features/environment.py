import os
import boto3
import botocore

def before_scenario(context, _scenario):
    if os.getenv("ENV") is None:
        context.s3 = boto3.client("s3", endpoint_url="http://localhost:4566")
        context.lambda_client = boto3.client('lambda',
            region_name="us-east-1",
            endpoint_url="http://127.0.0.1:3001/",
            use_ssl=False,
            verify=False,
            config=botocore.client.Config(
                signature_version=botocore.UNSIGNED,
                read_timeout=60,
                retries={'max_attempts': 0},
            )
        )
    else:
        context.s3 = boto3.client("s3")
        context.lambda_client = boto3.client("lambda")