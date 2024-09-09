import requests
from datetime import datetime
import os
from dotenv import load_dotenv 

def sendFinished(html_list):
    # Load the .env file and get the access token for fortnox
    load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
    access_token = os.getenv('postmark_api_token')
    summary_email_recipient= os.getenv('summary_email_recipient')

    # Define the URL of the Postmark API endpoint for sending emails
    api_url = "https://api.postmarkapp.com/email"

    # Define your headers, including your API token for authentication
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Postmark-Server-Token": access_token  # token managed by viktor@darksoil.studio
    }
    now = datetime.now()
    
    # Create the payload for the email
    html=""
    for item in html_list:
        html=html+item+"<br>"

    payload = {
        "From": "viktor@darksoil.studio",  # Replace with your sender email address
        "To": summary_email_recipient,  # Replace with the recipient email address
        "Subject": "[OC-to-F-Script] running at "+now.strftime("%d/%m/%Y %H:%M:%S")+" ran successfully!",
        "HtmlBody": "The integration script found the following wise transactions and created respective vouchers in Fortnox:<br><br>"+html+"<br><br>Have a good day!"

    }

    # Send the POST request
    response = requests.post(api_url, headers=headers, json=payload)

    # Check the response
    if response.status_code == 200:
        print("Summary email sent successfully!")
    else:
        print("Failed to send email:", response.text)

