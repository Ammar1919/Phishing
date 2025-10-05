from supabase import create_client, Client
import os
import json
from dotenv import load_dotenv
from db_utils.cryptography import encrypt, decrypt
import base64

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

def store_user_credentials(email, creds):
    
    creds_bytes = json.dumps(creds).encode()
    
    encrypted_creds = base64.b64encode(encrypt(creds_bytes)).decode()

    result = supabase.table('user_credentials').select('email').eq('email', email).execute()

    if result.data:
        result = supabase.table('user_credentials').update({'email': email, 'encrypted_credentials': encrypted_creds}).eq('email', email).execute()
    
    else:    
        result = supabase.table('user_credentials').insert({
            'email': email,
            'encrypted_credentials': encrypted_creds
        }).execute()


def get_user_credentials(email):

    result = supabase.table('user_credentials').select('encrypted_credentials').eq('email', email).execute()

    if not result.data:
        return None
    
    encrypted_creds = result.data[0]['encrypted_credentials']
    creds = json.loads(decrypt(base64.b64decode(encrypted_creds)).decode())

    return creds

