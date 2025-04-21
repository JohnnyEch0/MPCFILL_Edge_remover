import os
import io
import sys
from pathlib import Path
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

"""
Manage Google Drive API interactions
"""
# Constants
SERVICE_ACC_FILENAME = "mpcfill-to-pdf-tool-0aafb35b956a.json"  # Update this to your actual credential file name
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def find_or_create_google_drive_service():
    """Create and return a Google Drive API service"""
    print("Getting Google Drive API credentials...")
    
    # Find the service account file in the same directory as the script
    script_dir = Path(os.path.abspath(__file__)).parent
    credential_path = script_dir / SERVICE_ACC_FILENAME
    
    if not credential_path.exists():
        print(f"ERROR: Service account file not found at {credential_path}")
        print("Please make sure your service account key file is in the correct location.")
        return None
    
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            str(credential_path), scopes=SCOPES
        )
        service = build("drive", "v3", credentials=creds, static_discovery=False, cache_discovery=False)
        print("Successfully created Google Drive service!")
        return service
    except Exception as e:
        print(f"Error creating Google Drive service: {e}")
        return None
    
def get_google_drive_file_name(service, drive_id):
    """
    Retrieve the name for the Google Drive file identified by `drive_id`.
    """
    if not drive_id:
        return None
    
    try:
        response = service.files().get(fileId=drive_id).execute()
        return response.get("name")
    except HttpError as error:
        print(f"Error retrieving file metadata: {error}")
        # Check if it's a permissions issue
        if error.resp.status == 404:
            print(f"File not found or no permission: {drive_id}")
        return None

def download_google_drive_file(service, drive_id, file_path):
    """
    Download the Google Drive file identified by `drive_id` to the specified `file_path`.
    Returns whether the request was successful or not.
    """
    print(f"Downloading Google Drive image {drive_id}...")
    
    try:
        request = service.files().get_media(fileId=drive_id)
        file_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download: {int(status.progress() * 100)}%")
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(file_buffer.getvalue())
        
        print(f"File saved to {file_path}")
        return True
        
    except HttpError as error:
        print(f"Error downloading file: {error}")
        print(f"Response status: {error.resp.status}")
        print(f"Response reason: {error.resp.reason}")
        return False
    
