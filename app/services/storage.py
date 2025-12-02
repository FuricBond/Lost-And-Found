"""
Local file storage service for image uploads.
Stores files in the local filesystem.
"""

import os
import uuid
import shutil
from typing import BinaryIO
from pathlib import Path

from app.config import settings


class StorageService:
    """
    Service for uploading and retrieving files from local storage.
    
    Files are organized as:
    {upload_dir}/items/{item_id}/images/{image_id}/{suffix}.{extension}
    """
    
    def __init__(self):
        """Initialize local storage with configured directory."""
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_file_path(
        self,
        item_id: str,
        image_id: str,
        suffix: str,
        extension: str = "jpg"
    ) -> Path:
        """
        Generate a file path for an image.
        
        Format: {upload_dir}/items/{item_id}/images/{image_id}/{suffix}.{extension}
        """
        path = self.upload_dir / "items" / str(item_id) / "images" / str(image_id)
        path.mkdir(parents=True, exist_ok=True)
        return path / f"{suffix}.{extension}"
    
    def _get_relative_path(
        self,
        item_id: str,
        image_id: str,
        suffix: str,
        extension: str = "jpg"
    ) -> str:
        """
        Generate a relative path key for an image (for database storage).
        """
        return f"items/{item_id}/images/{image_id}/{suffix}.{extension}"
    
    async def upload_image(
        self,
        file_data: BinaryIO,
        item_id: str,
        image_id: str,
        content_type: str,
        suffix: str = "original"
    ) -> str:
        """
        Upload an image to local storage.
        
        Args:
            file_data: File-like object containing image data
            item_id: Parent item UUID
            image_id: Image UUID
            content_type: MIME type of the image
            suffix: Key suffix (original, processed, thumbnail)
        
        Returns:
            Relative path key of the uploaded file
        """
        # Determine file extension from content type
        extension_map = {
            'image/jpeg': 'jpg',
            'image/png': 'png',
            'image/webp': 'webp',
        }
        extension = extension_map.get(content_type, 'jpg')
        
        # Get file path
        file_path = self._get_file_path(item_id, image_id, suffix, extension)
        relative_path = self._get_relative_path(item_id, image_id, suffix, extension)
        
        # Write file
        try:
            with open(file_path, 'wb') as f:
                # Read from file_data and write
                content = file_data.read()
                f.write(content)
            return relative_path
        except Exception as e:
            raise StorageError(f"Failed to upload image: {e}")
    
    async def upload_bytes(
        self,
        data: bytes,
        item_id: str,
        image_id: str,
        content_type: str,
        suffix: str = "processed"
    ) -> str:
        """
        Upload image bytes to local storage.
        
        Args:
            data: Raw image bytes
            item_id: Parent item UUID
            image_id: Image UUID
            content_type: MIME type
            suffix: Key suffix
        
        Returns:
            Relative path key of the uploaded file
        """
        extension_map = {
            'image/jpeg': 'jpg',
            'image/png': 'png',
            'image/webp': 'webp',
        }
        extension = extension_map.get(content_type, 'jpg')
        
        file_path = self._get_file_path(item_id, image_id, suffix, extension)
        relative_path = self._get_relative_path(item_id, image_id, suffix, extension)
        
        try:
            with open(file_path, 'wb') as f:
                f.write(data)
            return relative_path
        except Exception as e:
            raise StorageError(f"Failed to upload image: {e}")
    
    async def download_image(self, relative_path: str) -> bytes:
        """
        Download an image from local storage.
        
        Args:
            relative_path: Relative path key of the image
        
        Returns:
            Image data as bytes
        """
        file_path = self.upload_dir / relative_path
        
        if not file_path.exists():
            raise StorageError(f"Image not found: {relative_path}")
        
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except Exception as e:
            raise StorageError(f"Failed to download image: {e}")
    
    async def delete_image(self, relative_path: str) -> bool:
        """
        Delete an image from local storage.
        
        Args:
            relative_path: Relative path key of the image
        
        Returns:
            True if deleted successfully
        """
        file_path = self.upload_dir / relative_path
        
        try:
            if file_path.exists():
                file_path.unlink()
            return True
        except Exception as e:
            raise StorageError(f"Failed to delete image: {e}")
    
    async def delete_item_images(self, item_id: uuid.UUID) -> int:
        """
        Delete all images for an item.
        
        Args:
            item_id: Item UUID
        
        Returns:
            Number of deleted files
        """
        item_dir = self.upload_dir / "items" / str(item_id)
        
        if not item_dir.exists():
            return 0
        
        try:
            # Count files before deletion
            count = sum(1 for _ in item_dir.rglob('*') if _.is_file())
            # Remove entire directory tree
            shutil.rmtree(item_dir)
            return count
        except Exception as e:
            raise StorageError(f"Failed to delete item images: {e}")
    
    def get_file_url(self, relative_path: str) -> str:
        """
        Get the file URL/path for serving.
        
        Args:
            relative_path: Relative path key of the file
        
        Returns:
            URL path for serving the file
        """
        return f"/files/{relative_path}"
    
    def get_absolute_path(self, relative_path: str) -> Path:
        """
        Get the absolute file path.
        
        Args:
            relative_path: Relative path key
        
        Returns:
            Absolute Path object
        """
        return self.upload_dir / relative_path


class StorageError(Exception):
    """Custom exception for storage operations."""
    pass


# Singleton instance
storage_service = StorageService()
