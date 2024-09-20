"""
Storage Module

This module provides functions to manage storage buckets and files in a
simulated cloud environment.

Functions:
- create_bucket(bucket_name): Creates a new bucket with the specified name
if it does not already exist.
- upload_file(bucket_name, file_name, file_content): Uploads a file with the
specified name and content to the specified bucket.
- delete_file(bucket_name, file_name): Deletes a file with the specified name
from the specified bucket.
- delete_bucket(bucket_name): Deletes a bucket with the specified name if it
exists and is empty.

Global Variables:
- ROOT_STORAGE_DIR: The root directory where all storage buckets are located.
If it does not exist, it is created at module initialization.
"""
import os

ROOT_STORAGE_DIR = "storage"

if not os.path.exists(ROOT_STORAGE_DIR):
    os.makedirs(ROOT_STORAGE_DIR)

def create_bucket(bucket_name):
    """
    Creates a new bucket with the specified name if it does not already exist.
    Args:
        bucket_name (str): The name of the bucket to create.
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    bucket_path = os.path.join(ROOT_STORAGE_DIR, bucket_name)
    if not os.path.exists(bucket_path):
        os.makedirs(bucket_path)
        return {"message": f"Bucket {bucket_name} created!"}
    return {"message": f"Bucket {bucket_name} already exists!"}

def upload_file(bucket_name, file_name, file_content):
    """
    Uploads a file with the specified name and content to the specified bucket.
    Args:
        bucket_name (str): The name of the bucket to upload the file to.
        file_name (str): The name of the file to upload.
        file_content (str): The content of the file to upload.
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    bucket_path = os.path.join(ROOT_STORAGE_DIR, bucket_name)
    if not os.path.exists(bucket_path):
        return {"error": f"Bucket {bucket_name} does not exist!"}
    file_path = os.path.join(bucket_path, file_name)
    with open(file_path, 'wb') as f:
        f.write(file_content)
    return {"message": f"File {file_name} uploaded to {bucket_name}!"}

def delete_file(bucket_name, file_name):
    """
    Deletes a file with the specified name from the specified bucket.
    Args:
        bucket_name (str): The name of the bucket to delete the file from.
        file_name (str): The name of the file to delete.
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    file_path = os.path.join(ROOT_STORAGE_DIR, bucket_name, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"File {file_name} deleted from {bucket_name}!"}
    return {"message": f"File {file_name} does not exist in {bucket_name}!"}

def delete_bucket(bucket_name):
    """
    Deletes a bucket with the specified name if it exists and is empty.
    Args:
        bucket_name (str): The name of the bucket to delete.
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    bucket_path = os.path.join(ROOT_STORAGE_DIR, bucket_name)
    if os.path.exists(bucket_path):
        if os.listdir(bucket_path):
            return {"message": f"Bucket {bucket_name} is not empty and cannot be deleted!"}
        os.rmdir(bucket_path)
        return {"message": f"Bucket {bucket_name} deleted!"}
    return {"message": f"Bucket {bucket_name} does not exist!"}
