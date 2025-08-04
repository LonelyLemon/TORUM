from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from typing import Optional

from backend.src.auth.config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET

async def upload_file_to_s3(file_obj, s3_key: str, content_type: str) -> Optional[str]:
    session = get_session()
    async with session.create_client(
        's3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    ) as client:
        try:
            await client.head_bucket(Bucket=S3_BUCKET)
            await client.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=file_obj,
                ContentType=content_type
            )
            return s3_key
        except ClientError as e:
            print("Upload error: ", {e})
            return None

async def generate_presigned_url(filename: str, expires_in: int = 3600) -> Optional[str]:
    session = get_session()
    async with session.create_client(
        's3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    ) as client:
        try:
            url = await client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': S3_BUCKET,
                    'Key': filename,
                },
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            print("Generate presigned URL error: ", {e})
            return None