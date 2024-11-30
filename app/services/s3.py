#!!! переписать
import os
from typing import List, Any
from functools import wraps
from aioboto3 import Session
import aiofiles
from botocore.exceptions import ClientError
from app.core.config import config

class S3Session():
    
    def __init__(self, settings: Any = config) -> None:
        self.s3=None
        self.bucket_name=settings.aws_bucket_name
        self.service_name=settings.aws_service_name
        self.region_name=settings.aws_region
        self.endpoint_url=settings.aws_endpoint
        self.access_key_id=settings.aws_access_key_id
        self.secret_access_key=settings.aws_secret_access_key
    
    async def create_client(self):
        session = Session()
        self.s3 = await session.client(
            service_name=self.service_name,
            region_name=self.region_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key
        ).__aenter__()
    
    async def bucket_exists(self, bucket_name: str) -> bool:
        """
        Проверка существования бакета.
        args:
            bucket_name: str - имя бакета
        return: bool
        """
        try:
            await self.s3.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
        raise ValueError(f'Ошибка при проверке наличия бакета: {e}') from e
    
    async def upload_file(self, bucket_name: str, file_path: str, file_key: str) -> None:
        """
        Загрузка файл-подобного объекта в S3.
        Файл должен быть открыт в бинарном режиме.
        args:
            bucket_name: str - имя бакета для загрузки файла
            file_path: str - путь к файлу для загрузки
            file_key: str - ключ файла в S3
        return: None
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'Файл {file_path} не найден')
        try:
            async with aiofiles.open(file=file_path, mode='rb') as file:
                await self.s3.upload_fileobj(
                    Fileobj=file,
                    Bucket=bucket_name,
                    Key=file_key,
                )
                return self.get_link_file(bucket_name, file_key)
        except ClientError as e:
            raise ValueError(f'Ошибка при загрузке файла: {e}') from e
        except IOError as e:
            raise ValueError(f'Ошибка при открытии файла: {e}') from e
        except Exception as e:
            raise RuntimeError(f'Ошибка при загрузке файла: {e}') from e
    async def get_link_file(self, bucket_name: str, file_key: str) -> str:
        """
        Получение ссылки на файл в S3.
        args:
            bucket_name: str - имя бакета
            file_key: str - ключ файла в S3
        return: str - ссылка на файл в S3
        """
        # exapmle:https://storage.yandexcloud.net/drivers.data/conf/com-1/2ep/lpm-4/auf32.rar
        try: 
            return f'https://storage.yandexcloud.net/{bucket_name}/{file_key}'
        except ClientError as e:
            raise ValueError(f'Ошибка при получении ссылки на файл: {e}') from e
        except Exception as e:
            raise RuntimeError(f'Ошибка при получении ссылки на файл: {e}') from e
    async def download_file(self, bucket_name: str, file_key: str, file_path: str) -> None:
        """
        Скачивание файл-подобного объекта из S3.
        args:
            bucket_name: str - имя бакета для скачивания файла
            file_key: str - ключ файла в S3
            file_path: str - путь к файлу для скачивания
        return: None
        """
        try:
            async with aiofiles.open(file=file_path, mode='wb') as file:
                await self.s3.download_fileobj(
                    Bucket=bucket_name,
                    Key=file_key,
                    Fileobj=file
                )
        except ClientError as e:
            raise ValueError(f'Ошибка при скачивании файла: {e}') from e
        except IOError as e:
            raise ValueError(f'Ошибка при открытии файла для записи: {e}') from e
        except Exception as e:
            raise RuntimeError(f'Ошибка при скачивании файла: {e}') from e
    
    async def upload_multiple_files(self,
                                     bucket_name: str, 
                                     file_paths: List[str], 
                                     file_keys: List[str]
    ) -> List[str]:
        """
        Загрузка нескольких файлов в S3.
        args:
            bucket_name: str - имя бакета для загрузки файлов
            file_paths: List[str] - список путей к файлам для загрузки
            file_keys: List[str] - список ключей файлов в S3
        return: List[str] - список ключей загруженных файлов
        """
        uploaded_files = []
        for file_path in file_paths:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f'Файл {file_path} не найден')
        try:
            for file_path, file_key in zip(file_paths, file_keys):
                await self.upload_file(bucket_name, file_path, file_key)
                uploaded_files.append(file_key)
            return uploaded_files
        except ClientError as e:
            raise ValueError(f'Ошибка при загрузке файлов: {e}') from e
        except IOError as e:
            raise ValueError(f'Ошибка при открытии файлов: {e}') from e
        except Exception as e:
            raise RuntimeError(f'Ошибка при загрузке файлов: {e}') from e
     
    async def download_multiple_files(self,
                                      bucket_name: str, 
                                      file_keys: List[str], 
                                      file_paths: List[str]
    ) -> List[str]:
        """
        Скачивание нескольких файлов из S3.
        args:
            bucket_name: str - имя бакета для скачивания файлов
            file_keys: List[str] - список ключей файлов в S3
            file_paths: List[str] - список путей к файлам для скачивания
        return: List[str] - список ключей скаченных файлов
        """
        downloaded_files = []
        try:
            for file_key, file_path in zip(file_keys, file_paths):
                await self.download_file(bucket_name, file_key, file_path)
                downloaded_files.append(file_key)
            return downloaded_files
        except ClientError as e:
            raise ValueError(f'Ошибка при скачивании файлов: {e}') from e
        except IOError as e:
            raise ValueError(f'Ошибка при открытии файлов для записи: {e}') from e
        except Exception as e:
            raise RuntimeError(f'Ошибка при скачивании файлов: {e}') from e
    
    async def get_list_files(self, bucket_name: str, prefix: str = '') -> List[str]:
        """
        Получение списка файлов в бакете.
        args:
            bucket_name: str - имя бакета для скачивания файлов
            prefix: str - префикс для фильтрации файлов
        return: List[str] - список ключей файлов в S3
        """
        try:
            response = await self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            files = []
            for obj in response.get('Contents', []):
                files.append(obj['Key'])
            return files
        except ClientError as e:
            raise ValueError(f'Ошибка при получении списка файлов: {e}') from e
        except Exception as e:
            raise RuntimeError(f'Ошибка при получении списка файлов: {e}') from e
 
    async def download_all_files(self, bucket_name: str, folder_path: str, prefix: str) -> None:
        """
        Скачивание всех файлов из бакета.
        args:
            bucket_name: str - имя бакета для скачивания файлов
            folder_path: str - путь к папке для скачивания файлов
            prefix: str - префикс для фильтрации файлов
        return: None
        """
        downloaded_files = []
        try:
            file_keys = await self.get_list_files(bucket_name, prefix)
            file_paths = [os.path.join(folder_path, file_key) for file_key in file_keys]
            downloaded_files = await self.download_multiple_files(bucket_name, file_keys, file_paths)
            return downloaded_files
        except ClientError as e:
            raise ValueError(f'Ошибка при скачивании файлов: {e}') from e
        except IOError as e:
            raise ValueError(f'Ошибка при открытии файлов для записи: {e}') from e
        except Exception as e:
            raise RuntimeError(f'Ошибка при скачивании файлов: {e}') from e

    async def delete_file(self, bucket_name: str,file_key: str) -> bool:
        """
        Удаление файла из бакета. 
        args:
            bucket_name: str - имя бакета для удаления файла
            file_key: str - ключ файла для удаления
        return: None
        """
        try:
            await self.s3.delete_object(
                    Bucket=bucket_name,
                    Key=file_key
                )
            return True
        except ClientError as e:
            raise ValueError(f'Ошибка при удалении файла из бакета: {e}') from e
        except Exception as e:
            raise RuntimeError(f'Ошибка при удалении файла из бакета: {e}') from e

    async def create_bucket(self, 
                             bucket_name: str) -> None:
        """
        Создание бакета в S3.
        args:
        bucket_name: str - имя бакета для создания
        return: None
        """
        try:
            await self.s3.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            raise ValueError(f'Ошибка при создании бакета: {e}') from e
        except Exception as e:
            raise RuntimeError(f'Ошибка при создании бакета: {e}') from e
    
    def s3_client_decorator(self, aws_access_key_id, aws_secret_access_key, region_name, endpoint_url):
        """Декоратор для автоматического создания и закрытия S3Client."""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                async with S3Session(aws_access_key_id, aws_secret_access_key, region_name, endpoint_url) as s3_client:
                    return await func(s3_client, *args, **kwargs)
            return wrapper
        return decorator