import os
import tempfile
from typing import Any, Dict

import boto3

if os.getenv("ENV") is None:
    s3 = boto3.client("s3", endpoint_url="http://docker.for.mac.localhost:4566")
else:
    boto3.client("s3")

def handler(event: Dict[str, Any], _context) -> str:
    """Uploads a friendly saultation to s3"""
    recipient = event["recipient"]
    with tempfile.TemporaryFile() as f:
        f.write(bytes(f"Hello, {recipient}!", "utf-8"))
        f.seek(0)
        s3.upload_fileobj(f, "testbucket", f"{recipient}.txt")
    return "hello"
