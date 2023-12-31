import requests
from dotenv import set_key, load_dotenv
import os
import datetime


# Load the .env file and get the authcode

load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
relative_path=os.getenv("relative_path")

authcode = os.getenv('fortnox_authcode')
credentials = os.getenv('fortnox_credentials')


# Fortnox OAuth token URL
token_url = "https://apps.fortnox.se/oauth-v1/token"


# Authorization header with Basic Authentication
auth_header = {
    "Authorization": f"Basic {credentials}"
}

# Request body as a dictionary
data = {
    "grant_type": "authorization_code",
    "code": authcode,
    "redirect_uri": "https://darksoil.studio"
}


# Send a POST request to the token URL
response = requests.post(token_url, headers=auth_header, data=data)


# Check if the request was successful (status code 200)
if response.status_code == 200:
    full_response = response.json()
    access_token = full_response.get("access_token")
    refresh_token = full_response.get("refresh_token")
    
else:
    # If the request was not successful, print an error message
    print(f"Error: {response.status_code} - {response.text}")

time_now = datetime.datetime.now()
formatted_date = time_now.strftime("%Y-%m-%d-%H-%M")
set_key(f'{relative_path}.env', 'fortnox_access_token', access_token)
set_key(f'{relative_path}.env', 'fortnox_refresh_token', refresh_token)
set_key(f'{relative_path}.env', 'fortnox_token_last_update', formatted_date)
print("Access token and refresh token updated in .env file")
