import os
import json
from fastapi import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from db_utils.supa_db import store_user_credentials

SCOPES = ['https://mail.google.com/', 
          'https://www.googleapis.com/auth/gmail.modify',
         'https://www.googleapis.com/auth/gmail.labels',
         'https://www.googleapis.com/auth/gmail.readonly']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")

router = APIRouter()

@router.get('/authorize')
async def authorize_user_creds():

    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES
    )

    flow.redirect_uri = 'http://localhost:1800/gmail/auth/callback'

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    print(authorization_url)

    # include oauth2 state management - store and retrieve/compare with callback
    return {"auth_url": authorization_url}

@router.get('/auth/callback')
async def auth_callback(request: Request):
    
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code:
        raise HTTPException(400, "Authorization code missing.")
    
    # include oauth2 state verification - raise error for invalid

    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        state=state
    )
    flow.redirect_uri = 'http://localhost:1800/gmail/auth/callback'

    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)

    creds = flow.credentials

    service = build('gmail', 'v1', credentials=creds)
    profile = service.users().getProfile(userId='me').execute()
    user_email = profile['emailAddress']

    ## store user creds with email

    print(f"Credentials: {creds}")

    store_user_credentials(user_email, json.loads(creds.to_json()))
    
    request = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/phishing-451316/topics/gmailNotifs',
        'labelFilterBehavior': 'INCLUDE'
    }
    service.users().watch(userId='me',body=request).execute()

    frontend_url = f"http://localhost:3000/success?email={user_email}"

    return RedirectResponse(url=frontend_url)