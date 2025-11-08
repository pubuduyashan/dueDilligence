#!/usr/bin/env python3
"""
Google Drive Upload Helper
Uploads scraped CSV files to Google Drive folder
"""

import os
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


class DriveUploader:
    """Upload files to Google Drive"""

    def __init__(self, folder_id):
        """
        Initialize Drive Uploader

        Args:
            folder_id (str): Google Drive folder ID where files will be uploaded
        """
        self.folder_id = folder_id
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with Google Drive API"""
        creds = None

        # The file token.pickle stores the user's access and refresh tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    logger.error("credentials.json not found!")
                    logger.info("\nTo use this script, you need to:")
                    logger.info("1. Go to https://console.cloud.google.com/")
                    logger.info("2. Create a new project or select existing one")
                    logger.info("3. Enable Google Drive API")
                    logger.info("4. Create OAuth 2.0 credentials (Desktop app)")
                    logger.info("5. Download credentials as 'credentials.json'")
                    logger.info("6. Place credentials.json in this directory\n")
                    raise FileNotFoundError("credentials.json is required")

                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)
        logger.info("Successfully authenticated with Google Drive")

    def upload_file(self, file_path, folder_id=None):
        """
        Upload a file to Google Drive

        Args:
            file_path (str): Path to the file to upload
            folder_id (str): Folder ID to upload to (optional, uses default if not provided)

        Returns:
            dict: File metadata from Google Drive
        """
        if folder_id is None:
            folder_id = self.folder_id

        file_name = os.path.basename(file_path)

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        media = MediaFileUpload(file_path, resumable=True)

        try:
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()

            logger.info(f"Uploaded: {file_name} (ID: {file.get('id')})")
            return file

        except Exception as e:
            logger.error(f"Failed to upload {file_name}: {e}")
            return None

    def upload_directory(self, directory_path, folder_id=None):
        """
        Upload all CSV files from a directory to Google Drive

        Args:
            directory_path (str): Path to directory containing files
            folder_id (str): Folder ID to upload to (optional)

        Returns:
            tuple: (success_count, fail_count)
        """
        if folder_id is None:
            folder_id = self.folder_id

        if not os.path.exists(directory_path):
            logger.error(f"Directory not found: {directory_path}")
            return 0, 0

        # Get all CSV files
        csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

        if not csv_files:
            logger.warning(f"No CSV files found in {directory_path}")
            return 0, 0

        logger.info(f"Found {len(csv_files)} CSV files to upload")

        success_count = 0
        fail_count = 0

        for csv_file in csv_files:
            file_path = os.path.join(directory_path, csv_file)
            result = self.upload_file(file_path, folder_id)

            if result:
                success_count += 1
            else:
                fail_count += 1

        logger.info(f"Upload complete - Success: {success_count}, Failed: {fail_count}")
        return success_count, fail_count


def main():
    """Main execution function"""

    # Your Google Drive folder ID from the URL
    # https://drive.google.com/drive/folders/1GtUUeBd3Q46FEhlMg87BaBscvqDHC8IE?usp=sharing
    FOLDER_ID = '1GtUUeBd3Q46FEhlMg87BaBscvqDHC8IE'

    # Directory containing scraped CSV files
    SCRAPED_DATA_DIR = 'scraped_data'

    print("\n" + "="*60)
    print("Google Drive Upload Tool")
    print("="*60)
    print(f"Target folder: {FOLDER_ID}")
    print(f"Source directory: {SCRAPED_DATA_DIR}")
    print("="*60 + "\n")

    try:
        uploader = DriveUploader(folder_id=FOLDER_ID)
        success, failed = uploader.upload_directory(SCRAPED_DATA_DIR)

        print("\n" + "="*60)
        print("UPLOAD SUMMARY")
        print("="*60)
        print(f"Successfully uploaded: {success} files")
        print(f"Failed to upload: {failed} files")
        print("="*60 + "\n")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nPlease follow the setup instructions above to configure Google Drive API access.\n")
    except Exception as e:
        print(f"\nUnexpected error: {e}\n")


if __name__ == '__main__':
    main()
