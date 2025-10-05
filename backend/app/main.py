from fastapi import FastAPI, Request
from googleapiclient.discovery import build
import json
from gmail.gmail_auth import router as gmail_router
#from message_handler import router as notification_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gmail_router, prefix="/gmail")
#app.include_router(notification_router)

@app.post("/gmail-webhook")
async def gmail_webhook(request: Request):
    """ Receive Gmail notifications for new emails """

async def analyze_new_email(user_email, message_id):
    """ Analyze and flag new emails """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=1800, reload=True)
# OAUTHLIB_INSECURE_TRANSPORT=1 uvicorn app.main:app --host 127.0.0.1 --port 1800 --reload