"""
This utility extracts Google Drive ids of the dataset and saves them to file:

2019-09-19_to_172.31.21.94.pcap 1ml5YyJytCiQKNus1Wt0hIGfTt-HnpxqW
2019-09-20_to_172.31.21.94.pcap 1ei7QuuqNkTwTDp5b_sN0C5C2Y6J8X92x

How configure credentials - https://developers.google.com/drive/api/v3/quickstart/python

How to download:

#!/bin/bash
mkdir pcaps
while read -r filename google_drive_id; do
  echo "Downloading $filename $google_drive_id ..."
  wget 'https://drive.google.com/uc?export=download&id='$google_drive_id -O pcaps/$filename
done <utils/dataset_google_drive_ids
"""
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path

def get_google_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def save_ids(filename, files):
    with open(filename, 'w') as f:
        for filename, id in files:
            f.write(f'{filename} {id}\n')

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
creds = get_google_credentials()

drive_service = build('drive', 'v3', credentials=creds)
page_token = None
files = []
while True:
    response = drive_service.files().list(q="name contains 'pcap' and trashed = false",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
    for file in response.get('files', []):
        files.append((file.get('name'), file.get('id')))
    page_token = response.get('nextPageToken', None)
    if page_token is None:
        break

files.sort(key=lambda v: v[0])  # sort by filename

save_ids('dataset_google_drive_ids', filter(lambda fname: 'ICMP' not in fname, files))
save_ids('icmp_dataset_google_drive_ids', filter(lambda fname: 'ICMP' in fname, files))