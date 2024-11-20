import uuid
import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile
from fastapi import HTTPException
from app.core.config import config


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            service_name=config.AWS_SERVICE_NAME,
            aws_access_key_id=config.AWS_ACCESS_KEY,
            aws_secret_access_key=config.AWS_SECRET_KEY,
            region_name=config.AWS_REGION
        )
        self.bucket = config.AWS_BUCKET_NAME
        self.endpoint = config.AWS_ENDPOINT
        
    async def create_bucket(self, bucket_name: str):
        self.s3_client.create_bucket(Bucket=bucket_name)

    async def get_object(self, bucket_name: str, key: str):
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=key)
            return response['Body'].read()
        except ClientError as e:
            raise HTTPException(status_code=404, detail="File not found")
        
    async def get_list_objects(self, bucket_name: str):
        response = self.s3_client.list_objects(Bucket=bucket_name)
        return response.get('Contents', []) 
    
    async def delete_objects(self, bucket_name: str, keys: list):
        self.s3_client.delete_objects(
            Bucket=bucket_name, 
            Delete={'Objects': [{'Key': key} for key in keys]})
    
    async def upload_file(self, file: UploadFile, folder: str = "") -> str:
        file_content = await file.read()
        return await self.save_file(file_content, file.filename, folder)

    async def save_file(self, file_content: bytes, file_name: str, folder: str) -> str:
        unique_filename = f"{uuid.uuid4()}_{file_name}"
        path = f"{folder}/{unique_filename}" if folder else unique_filename
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=path,
                Body=file_content
            )
            return f"{self.endpoint}/{self.bucket}/{path}"
        
        except ClientError as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error uploading file to S3: {str(e)}"
            )

