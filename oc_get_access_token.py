import requests
from dotenv import set_key, load_dotenv
import os
import sys
import re
import datetime
from urllib.parse import urlparse, parse_qs

def extract_code(arg):
    """Accept a full URL with ?code=... or a raw 64-char hex string."""
    if arg.startswith("http"):
        params = parse_qs(urlparse(arg).query)
        codes = params.get("code")
        if not codes:
            print("Error: no 'code' parameter found in URL")
            sys.exit(1)
        return codes[0]
    elif re.fullmatch(r"[0-9a-fA-F]{64}", arg):
        return arg
    else:
        print("Error: argument must be a URL containing 'code=...' or a 64-character hex string")
        sys.exit(1)

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <url-with-code | 64-char-hex-code>")
    sys.exit(1)

new_authcode = extract_code(sys.argv[1])
set_key('.env', 'oc_authcode', new_authcode)
print(f"Updated oc_authcode in .env")

# Load the .env file and get the authcode
load_dotenv('./.env', override=True)
authcode = os.getenv('oc_authcode')
client_id = os.getenv('oc_client_id')
client_secret = os.getenv('oc_client_secret')

# Open Collective OAuth token URL
token_url = "https://opencollective.com/oauth/token"



# Request body as a dictionary
data = {
    "grant_type": "authorization_code",
    "client_id": client_id,
    "client_secret": client_secret,
    "code": authcode,
    "redirect_uri": "https://opencollective.com/borderland/"
}

# Send a POST request to the token URL
response = requests.post(token_url, data=data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    full_response = response.json()
    access_token = full_response.get("access_token")
    #print(f"Access Token: {access_token}")
    #print(f"{full_response}")
    set_key('.env', 'oc_access_token', access_token)
    time_now = datetime.datetime.now()
    formatted_date = time_now.strftime("%Y-%m-%d")
    set_key('.env', 'oc_access_token_created', formatted_date)
    print(f"Access token updated in .env (created {formatted_date})")


else:
    # If the request was not successful, print an error message
    print(f"Error: {response.status_code} - {response.text}")
