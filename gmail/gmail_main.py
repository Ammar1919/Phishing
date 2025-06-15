import os.path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from gmail_auth import get_creds

def gmail_service():
    creds = get_creds()
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds) # Gmail API
    
        ## All function calls and logic

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
