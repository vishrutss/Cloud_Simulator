"""
CDN Module

This module simulates a simple Content Delivery Network (CDN) with basic functionalities 
such as uploading files to the origin server, replicating files to edge servers, and 
serving files from the nearest edge server.

Functions:
    upload_to_origin(file_name, content):
        Uploads a file to the origin server and replicates it to all edge servers.
    replicate_to_edges(file_name):
        Replicates a file from the origin server to all edge servers.
    serve_from_nearest_edge(file_name, user_location):
        Serves a file from the nearest edge server based on the user's location.
Constants:
    edge_servers (list): List of edge server names.
    ROOT_CDN_DIR (str): Root directory for the CDN storage.
"""
import os
import shutil

edge_servers = ['edge1', 'edge2', 'edge3']

ROOT_CDN_DIR = "cdn_storage"

if not os.path.exists(ROOT_CDN_DIR):
    os.makedirs(ROOT_CDN_DIR)

def upload_to_origin(file_name, content):
    """
    Uploads a file to the origin server and replicates it to all edge servers.
    Args:
        file_name (str): The name of the file to upload.
        content (str): The content of the file to upload.
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    origin_path = os.path.join(ROOT_CDN_DIR, 'origin')
    if not os.path.exists(origin_path):
        os.makedirs(origin_path)
    file_path = os.path.join(origin_path, file_name)
    with open(file_path, 'wb') as f:
        f.write(content)
    replicate_result = replicate_to_edges(file_name)
    return {"message": f"File {file_name} uploaded to origin. {replicate_result}"}

def delete_from_origin(file_name):
    """
    Deletes a file from the origin server and all edge servers.
    Args:
        file_name (str): The name of the file to delete.
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    origin_path = os.path.join(ROOT_CDN_DIR, 'origin', file_name)
    if os.path.exists(origin_path):
        os.remove(origin_path)
        for server in edge_servers:
            edge_path = os.path.join(ROOT_CDN_DIR, server, file_name)
            if os.path.exists(edge_path):
                os.remove(edge_path)
        return {"message": f"File {file_name} deleted from origin and all edge servers."}
    return {"message": f"File {file_name} not found."}

def replicate_to_edges(file_name):
    """
    Replicates a file from the origin server to all edge servers.
    Args:
        file_name (str): The name of the file to replicate.
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    origin_path = os.path.join(ROOT_CDN_DIR, 'origin', file_name)
    if not os.path.exists(origin_path):
        return {"message": "File does not exist in the origin."}
    for server in edge_servers:
        edge_dir = os.path.join(ROOT_CDN_DIR, server)
        if not os.path.exists(edge_dir):
            os.makedirs(edge_dir)
        edge_path = os.path.join(edge_dir, file_name)
        shutil.copy(origin_path, edge_path)
    return {"message": f"File {file_name} replicated to all edge servers."}

def serve_from_nearest_edge(file_name, user_location):
    """
    Serves a file from the nearest edge server based on the user's location.
    Args:
        file_name (str): The name of the file to serve.
        user_location (int): The location of the user.
    Returns:
        dict: A dictionary containing the content of the file and the server it was served from.
    """
    nearest_server = edge_servers[user_location % len(edge_servers)]
    edge_path = os.path.join(ROOT_CDN_DIR, nearest_server, file_name)
    if os.path.exists(edge_path):
        with open(edge_path, 'r', encoding='utf-8') as f:
            return {"content": f.read(), "server": nearest_server}
    else:
        return {"message": f"File {file_name} not found."}
