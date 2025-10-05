from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from db_utils.supa_db import get_user_credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.cloud import pubsub_v1
from config import PROJECT_ID, SUBSCRIPTION_ID
from models.phish_model import predict_email, display_results
import time
import base64
import json

allowed_labels = ['POTENTIAL THREAT']

def callback(message):
    print(f"Message received: {message.data}")
    message.ack()

    try:
        email_address = retrieve_email(message.data)
        creds_dict = get_user_credentials(email_address)
        if not creds_dict:
            raise Exception("No credentials stored for this user: ", email_address)
        
        creds = Credentials.from_authorized_user_info(creds_dict)
        service = build('gmail', 'v1', credentials=creds)
        latest_email = get_latest_email(service)
        if latest_email is not None:
            process_email(latest_email, service)
    except Exception as e:
        print("Email processing Exception: ", e)

def retrieve_email(payload):
    notification_data = json.loads(payload)
    email = notification_data.get('emailAddress')
    return email

def get_latest_email(service):
    latest = service.users().messages().list(userId='me', maxResults=1).execute()
    if not latest:
        raise Exception("No messages in this mailbox")

    message_id = latest['messages'][0]['id']
    message = service.users().messages().get(userId='me', id=message_id).execute()

    print(message.get('labelIds', []))
    labels = message.get('labelIds', [])
    unwanted_labels = ['CATEGORY_SOCIAL', 'CATEGORY_PROMOTIONS', 'SPAM']
    if any(label in labels for label in unwanted_labels):
        print("Returning none")
        return None

    print("Returning the message")
    return message

def process_email(latest_email, service):
    """ Processes email by retrieving, analyzing, and labelling it"""

    email_id = latest_email['id']
    payload = latest_email['payload']
    body = get_email_body(payload)
    if body['plain'] is not None:
        print(body['plain'])
        results = predict_email(body['plain'])
        display_results(results)

    label_manager('SAFE', service, email_id)

def get_email_body(payload):
    """ Retrieves email body """

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

def label_manager(label_name, service, message_id):
    """ Retrieves label_id and labels the message """

    label_id = get_label_id_by_name(label_name, service)
    if label_id == None:
        label_id = create_label(label_name, service)

    label_message(label_id, service, message_id)

def get_label_id_by_name(label_name, service):
    """ Retrieves label_id by label_name """

    labels_dict = service.users().labels().list(userId='me').execute()
    labels_list = labels_dict['labels']
    for label in labels_list:
        if label['name'] == label_name:
            return label['id']
    return None

def create_label(label_name, service):
    """ Creates a label with selected label_name """

    label = service.users().labels().create(
        userId='me',
        body={
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show',
            'name': label_name
        }
    ).execute()
    return label['id']

def label_message(label_id, service, message_id):
    """ Labels the message """
    
    result = service.users().messages().modify(
        userId='me',
        id=message_id,
        body={
            "addLabelIds": [
                label_id
            ]
        }
    ).execute()


if __name__ == "__main__":

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    print("Listening for messages on: ", subscription_path)

    subscriber.subscribe(subscription_path, callback=callback)

    while True:
        time.sleep(30)


"""

Add a label manager function or file
 - Check labelling functionality, try personalization or design
Add further models for urgency, reminders, personal etc.

"""