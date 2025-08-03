import boto3

from botocore.exceptions import ClientError
from typing import Optional

from backend.src.auth.config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def upload_file_to_s3(file_obj, filename: str, content_type: str):
    try:
        s3_client.upload_fileobj(
            file_obj,
            S3_BUCKET,
            filename,
            ExtraArgs={"ContentType": content_type}
        )
        return filename
    except ClientError as e:
        print("Upload Error:", e)
        return None

def generate_presigned_url(filename: str, expires_in: int = 3600) -> Optional[str]:
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": S3_BUCKET,
                "Key": filename,
            },
            ExpireIn=expires_in
        )
        return url
    except ClientError as e:
        print("Presigned URL Error:", e)
        return None