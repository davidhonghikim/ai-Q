# AI-Q Knowledge Library System - Storage Service
# TOKEN COUNT: ~1,000 tokens
"""
Storage service for AI-Q Knowledge Library System.
Handles MinIO object storage initialization and operations.
"""

import asyncio
import logging
import os
from typing import Any, BinaryIO, Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path

from minio import Minio  # type: ignore
from minio.error import S3Error  # type: ignore
from src.config.settings import get_settings

# Configure logging
logger = logging.getLogger(__name__)

class StorageService:
    """Storage service for managing MinIO operations."""
    
    def __init__(self):
        self.settings = get_settings()
        self.client: Optional[Minio] = None  # type: ignore
        self.buckets = {}
    
    async def initialize(self) -> None:
        """Initialize MinIO connection and create buckets."""
        try:
            logger.info("Initializing storage service...")
            
            # Create MinIO client
            self.client = Minio(
                endpoint=f"{self.settings.object_storage.minio.host}:{self.settings.object_storage.minio.api_port}",
                access_key=self.settings.object_storage.minio.root_user,
                secret_key=self.settings.object_storage.minio.root_password,
                secure=False,  # Set to True for HTTPS
                region="us-east-1"
            )
            
            # Test connection
            await self._test_connection()
            
            # Create buckets
            await self._create_buckets()
            
            logger.info("Storage service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize storage service: {e}")
            raise
    
    async def _test_connection(self) -> None:
        """Test MinIO connection."""
        try:
            # List buckets to test connection
            buckets = self.client.list_buckets()
            logger.info("MinIO connection test successful")
        except Exception as e:
            logger.error(f"MinIO connection test failed: {e}")
            raise
    
    async def _create_buckets(self) -> None:
        """Create MinIO buckets if they don't exist."""
        buckets = [
            "aiq-documents",
            "aiq-images", 
            "aiq-videos",
            "aiq-audio",
            "aiq-backups",
            "aiq-temp"
        ]
        
        for bucket_name in buckets:
            await self._create_bucket(bucket_name)
    
    async def _create_bucket(self, bucket_name: str) -> None:
        """Create a specific MinIO bucket."""
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                logger.info(f"Created bucket: {bucket_name}")
            else:
                logger.info(f"Bucket already exists: {bucket_name}")
            
            # Store bucket reference
            self.buckets[bucket_name] = bucket_name
            
        except Exception as e:
            logger.error(f"Failed to create bucket {bucket_name}: {e}")
            raise
    
    async def upload_file(self, bucket_name: str, object_name: str, file_path: str, 
                         content_type: Optional[str] = None) -> bool:
        """Upload a file to MinIO."""
        try:
            if not self.client.bucket_exists(bucket_name):
                raise Exception(f"Bucket {bucket_name} does not exist")
            
            # Determine content type if not provided
            if not content_type:
                content_type = self._get_content_type(file_path)
            
            # Upload file
            self.client.fput_object(
                bucket_name,
                object_name,
                file_path,
                content_type=content_type
            )
            
            logger.debug(f"Uploaded file: {object_name} to bucket: {bucket_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload file {object_name}: {e}")
            return False
    
    async def upload_data(self, bucket_name: str, object_name: str, data: bytes, 
                         content_type: Optional[str] = None) -> bool:
        """Upload data bytes to MinIO."""
        try:
            if not self.client.bucket_exists(bucket_name):
                raise Exception(f"Bucket {bucket_name} does not exist")
            
            # Upload data
            self.client.put_object(
                bucket_name,
                object_name,
                data,
                length=len(data),
                content_type=content_type or "application/octet-stream"
            )
            
            logger.debug(f"Uploaded data: {object_name} to bucket: {bucket_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload data {object_name}: {e}")
            return False
    
    async def download_file(self, bucket_name: str, object_name: str, 
                           file_path: str) -> bool:
        """Download a file from MinIO."""
        try:
            if not self.client.bucket_exists(bucket_name):
                raise Exception(f"Bucket {bucket_name} does not exist")
            
            # Download file
            self.client.fget_object(bucket_name, object_name, file_path)
            
            logger.debug(f"Downloaded file: {object_name} from bucket: {bucket_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to download file {object_name}: {e}")
            return False
    
    async def get_file_data(self, bucket_name: str, object_name: str) -> Optional[bytes]:
        """Get file data as bytes from MinIO."""
        try:
            if not self.client.bucket_exists(bucket_name):
                raise Exception(f"Bucket {bucket_name} does not exist")
            
            # Get object data
            response = self.client.get_object(bucket_name, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            
            logger.debug(f"Retrieved data: {object_name} from bucket: {bucket_name}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to get file data {object_name}: {e}")
            return None
    
    async def delete_file(self, bucket_name: str, object_name: str) -> bool:
        """Delete a file from MinIO."""
        try:
            if not self.client.bucket_exists(bucket_name):
                raise Exception(f"Bucket {bucket_name} does not exist")
            
            # Delete object
            self.client.remove_object(bucket_name, object_name)
            
            logger.debug(f"Deleted file: {object_name} from bucket: {bucket_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete file {object_name}: {e}")
            return False
    
    async def list_files(self, bucket_name: str, prefix: Optional[str] = None) -> List[Dict[str, Any]]:
        """List files in a bucket."""
        try:
            if not self.client.bucket_exists(bucket_name):
                raise Exception(f"Bucket {bucket_name} does not exist")
            
            # List objects
            objects = self.client.list_objects(bucket_name, prefix=prefix, recursive=True)
            
            files = []
            for obj in objects:
                files.append({
                    "name": obj.object_name,
                    "size": obj.size,
                    "last_modified": obj.last_modified,
                    "etag": obj.etag
                })
            
            logger.debug(f"Listed {len(files)} files in bucket: {bucket_name}")
            return files
            
        except Exception as e:
            logger.error(f"Failed to list files in bucket {bucket_name}: {e}")
            return []
    
    async def get_file_info(self, bucket_name: str, object_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a file."""
        try:
            if not self.client.bucket_exists(bucket_name):
                raise Exception(f"Bucket {bucket_name} does not exist")
            
            # Get object info
            stat = self.client.stat_object(bucket_name, object_name)
            
            return {
                "name": object_name,
                "size": stat.size,
                "last_modified": stat.last_modified,
                "etag": stat.etag,
                "content_type": stat.content_type
            }
            
        except Exception as e:
            logger.error(f"Failed to get file info {object_name}: {e}")
            return None
    
    async def generate_presigned_url(self, bucket_name: str, object_name: str, 
                                   method: str = "GET", expires: int = 3600) -> Optional[str]:
        """Generate a presigned URL for file access."""
        try:
            if not self.client.bucket_exists(bucket_name):
                raise Exception(f"Bucket {bucket_name} does not exist")
            
            # Generate presigned URL
            url = self.client.presigned_url(
                method,
                bucket_name,
                object_name,
                expires=timedelta(seconds=expires)
            )
            
            logger.debug(f"Generated presigned URL for: {object_name}")
            return url
            
        except Exception as e:
            logger.error(f"Failed to generate presigned URL for {object_name}: {e}")
            return None
    
    def _get_content_type(self, file_path: str) -> str:
        """Get content type based on file extension."""
        ext = Path(file_path).suffix.lower()
        content_types = {
            ".txt": "text/plain",
            ".pdf": "application/pdf",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".mp4": "video/mp4",
            ".mp3": "audio/mpeg",
            ".json": "application/json",
            ".xml": "application/xml",
            ".csv": "text/csv"
        }
        return content_types.get(ext, "application/octet-stream")
    
    async def close(self) -> None:
        """Close MinIO connection."""
        try:
            # MinIO client doesn't have a close method, but we can clean up
            logger.info("Storage connections closed")
        except Exception as e:
            logger.error(f"Error closing storage connections: {e}")

# Global storage service instance
_storage_service: Optional[StorageService] = None

async def init_storage() -> None:
    """Initialize the storage service."""
    global _storage_service
    
    try:
        _storage_service = StorageService()
        await _storage_service.initialize()
        logger.info("Storage initialization completed")
    except Exception as e:
        logger.error(f"Storage initialization failed: {e}")
        raise

async def get_storage_service() -> StorageService:
    """Get the storage service instance."""
    if not _storage_service:
        raise RuntimeError("Storage service not initialized")
    return _storage_service

async def close_storage() -> None:
    """Close storage connections."""
    global _storage_service
    if _storage_service:
        await _storage_service.close()
        _storage_service = None 