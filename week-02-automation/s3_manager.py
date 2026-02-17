#!/usr/bin/env python3
"""
S3 Bucket Manager
Create buckets, upload/download files, manage S3 storage
Author: Juno-50 | Day 8 - AWS Learning Journey
"""

import boto3
import os
from datetime import datetime

class S3Manager:
    """S3 Bucket Manager class - Handles all S3 operations."""
    
    def __init__(self, region='us-east-1'):
        """Initialize S3 client."""
        self.s3 = boto3.client('s3', region_name=region)
        self.region = region
        print(f"✅ Connected to S3 in region: {region}")
    
    def create_bucket(self, bucket_name):
        """Create S3 bucket."""
        try:
            # Check if bucket already exists
            try:
                self.s3.head_bucket(Bucket=bucket_name)
                print(f"⚠️  Bucket '{bucket_name}' already exists")
                return False
            except:
                pass
            
            # Create bucket
            if self.region == 'us-east-1':
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                self.s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.region}
                )
            
            print(f"✅ Bucket '{bucket_name}' created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating bucket: {e}")
            return False
    
    def upload_file(self, file_path, bucket_name, object_name=None):
        """Upload file to S3 bucket."""
        if object_name is None:
            object_name = os.path.basename(file_path)
        
        try:
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                return False
            
            self.s3.upload_file(file_path, bucket_name, object_name)
            file_size = os.path.getsize(file_path)
            print(f"✅ Uploaded '{file_path}' to '{bucket_name}/{object_name}' ({file_size} bytes)")
            return True
        except Exception as e:
            print(f"❌ Error uploading file: {e}")
            return False
    
    def list_objects(self, bucket_name):
        """List all objects in bucket."""
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            
            if 'Contents' not in response:
                print(f"Bucket '{bucket_name}' is empty")
                return
            
            print(f"\nObjects in '{bucket_name}':")
            print(f"{'Name':<40} {'Size (bytes)':<15} {'Last Modified'}")
            print("-" * 80)
            
            for obj in response['Contents']:
                print(f"{obj['Key']:<40} {obj['Size']:<15} {obj['LastModified']}")
            
            print(f"\nTotal objects: {len(response['Contents'])}")
        except Exception as e:
            print(f"❌ Error listing objects: {e}")
    
    def download_file(self, bucket_name, object_name, file_path):
        """Download file from S3."""
        try:
            self.s3.download_file(bucket_name, object_name, file_path)
            print(f"✅ Downloaded '{bucket_name}/{object_name}' to '{file_path}'")
            return True
        except Exception as e:
            print(f"❌ Error downloading file: {e}")
            return False
    
    def delete_bucket(self, bucket_name, confirm=True):
        """Delete S3 bucket (must be empty)."""
        if confirm:
            response = input(f"⚠️  Delete bucket '{bucket_name}'? (yes/no): ")
            if response.lower() != 'yes':
                print("Deletion cancelled")
                return False
        
        try:
            # First, delete all objects in bucket
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                print(f"Deleting {len(response['Contents'])} object(s)...")
                for obj in response['Contents']:
                    self.s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                    print(f"  Deleted: {obj['Key']}")
            
            # Now delete the bucket
            self.s3.delete_bucket(Bucket=bucket_name)
            print(f"✅ Bucket '{bucket_name}' deleted successfully")
            return True
        except Exception as e:
            print(f"❌ Error deleting bucket: {e}")
            return False

def main():
    """Main function - demonstrates S3Manager usage."""
    print("=" * 80)
    print("S3 Bucket Manager")
    print("=" * 80)
    
    s3_manager = S3Manager()
    
