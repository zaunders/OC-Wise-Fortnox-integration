import requests
from datetime import datetime
import os
from dotenv import load_dotenv 

def sendTransferNotFound(transferId):
    # Load the .env file and get the access token for fortnox
    load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
    access_token = os.getenv('postmark_api_token')
    error_email_recipient= os.getenv('error_email_recipient')

    # Define the URL of the Postmark API endpoint for sending emails
    api_url = "https://api.postmarkapp.com/email"

    # Define your headers, including your API token for authentication
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Postmark-Server-Token": "495cc6b1-7397-4c06-a821-6f42aa8d6560"  # token managed by viktor@darksoil.studio
    }
    now = datetime.now()
    # Create the payload for the email
    payload = {
        "From": "viktor@darksoil.studio",  # Replace with your sender email address
        "To": error_email_recipient,  # Replace with the recipient email address
        "Subject": "Script running at "+now.strftime("%d/%m/%Y %H:%M:%S")+" has found a transferId ("+transferId+") that is not in OC",
        "TextBody": "The transferId that was not found in OC was: "+transferId
    }

    # Send the POST request
    response = requests.post(api_url, headers=headers, json=payload)

    # Check the response
    if response.status_code == 200:
        print("Transfer not found email sent successfully!")
    else:
        print("Failed to send email:", response.text)

# Test the function
#send_error_email("This is a test error message.")