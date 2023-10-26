import requests
from datetime import datetime
import os
from dotenv import load_dotenv 



def sendErrorEmail(error_message):
    # Load the .env file and get the access token for fortnox
    load_dotenv('./.env')
    access_token = os.getenv('postmark_api_token')

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
        "To": "viktor@darksoil.studio",  # Replace with the recipient email address
        "Subject": "Script running at "+now.strftime("%d/%m/%Y %H:%M:%S")+" has an error",
        "TextBody": error_message
    }

    # Send the POST request
    response = requests.post(api_url, headers=headers, json=payload)

    # Check the response
    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print("Failed to send email:", response.text)

# Test the function
#send_error_email("This is a test error message.")