from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from supa_db import get_user_credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.cloud import pubsub_v1
from config import PROJECT_ID, SUBSCRIPTION_ID
from phish_model import predict_email, display_results
import time
import base64
import json

def callback(message):
    print(f"Message received: {message.data}")
    email_address = retrieve_email(message.data)
    payload = get_latest_email_payload(email_address)
    body = get_email_body(payload)
    if body['plain'] is not None:
        print(body['plain'])
        results = predict_email(body['plain'])
        display_results(results)
    message.ack()

def retrieve_email(payload):
    notification_data = json.loads(payload)
    email = notification_data.get('emailAddress')
    return email

## Function to get email from db, construct creds, service, and retrieve latest email

def get_latest_email_payload(email_address):
    creds_dict = get_user_credentials(email_address)
    if not creds_dict:
        raise Exception("No credentials stored for this user: ", email_address)
    
    creds = Credentials.from_authorized_user_info(creds_dict)
    service = build('gmail', 'v1', credentials=creds)

    latest = service.users().messages().list(userId='me', maxResults=1).execute()
    message_id = latest['messages'][0]['id']
    message = service.users().messages().get(userId='me', id=message_id).execute()

    if not latest:
        raise Exception("No messages in this mailbox")

    return message['payload']

def get_email_body(payload):
    body = {'body': None, 'plain': None, 'html': None}
    if 'body' in payload and 'data' in payload['body']:
        print("Using body")
        data = payload['body']['data']
        decoded_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
        body['body'] = decoded_data.decode('UTF-8')
    elif 'parts' in payload:
        print("Using parts")
        for part in payload['parts']:
            if part['mimeType'] == 'text/html':
                data = part['body']['data']
                decoded_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                body['html'] = decoded_data.decode('UTF-8')
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                decoded_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                body['plain'] = decoded_data.decode('UTF-8')
    return body

def labeller(results):
    if results['all_probabilities']['legitimate_email'] < 0.6:
        ### label the email as phishing - create custom label
        pass
    
if __name__ == "__main__":

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    print("Listening for messages on: ", subscription_path)

    subscriber.subscribe(subscription_path, callback=callback)

    while True:
        time.sleep(30)

## add a label manager - risky email for < 50% confidence 
## add further models for urgency or reminders 