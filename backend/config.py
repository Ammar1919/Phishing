import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
PROJECT_ID = os.getenv('PROJECT_ID')
SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID')