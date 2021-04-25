import os
from dotenv import find_dotenv, load_dotenv
from twilio.rest import Client

# Config params
load_dotenv(find_dotenv())

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token  = os.getenv("TWILIO_AUTH_TOKEN")
toNumber = os.getenv("TWILIO_TO_NUMBER")
fromNumber = os.getenv("TWILIO_FROM_NUMBER")

# Set client
client = Client(account_sid, auth_token)

# New message
message = client.messages.create(
    to=  toNumber, 
    from_= fromNumber,
    body="Hello from Python!")

print(message.sid)