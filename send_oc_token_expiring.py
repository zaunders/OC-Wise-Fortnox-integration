import requests
from datetime import datetime
import os
from dotenv import load_dotenv 

def sendOcExpiring(daysLeft):
    # Load the .env file and get the access token for fortnox
    load_dotenv('./.env')
    access_token = os.getenv('postmark_api_token')
    oc_token_email= os.getenv('oc_token_email')

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
        "To": oc_token_email,  # Replace with the recipient email address
        "Subject": "Script running at "+now.strftime("%d/%m/%Y %H:%M:%S")+" found OC token expiring in "+str(daysLeft)+" days!",
        "HtmlBody": "The Open Collective access token used to automate bookkeeping is expiring in "+str(daysLeft)+" days. Please create a new authcode in the .env file.<br><br>In order to do so, please follow this link:<a href='https://opencollective.com/oauth/authorize?client_id=e5393aa85430c0b1da1d&response_type=code&redirect_url=https://opencollective.com/borderland/&scope=email,account,expenses,transactions,orders'> https://opencollective.com/oauth/authorize?client_id=e5393aa85430c0b1da1d&response_type=code&redirect_url=https://opencollective.com/borderland/&scope=email,account,expenses,transactions,orders</a><br><br>After authenticating there, email or message the authcode to the person responsible for putting it into the enviroment running the scripts and updating the token.<br><br>Thanks!"

    }

    # Send the POST request
    response = requests.post(api_url, headers=headers, json=payload)

    # Check the response
    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print("Failed to send email:", response.text)

# Test the function
#sendOcExpiring(5)