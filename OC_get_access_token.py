import requests
from dotenv import set_key, load_dotenv
import os


# Load the .env file and get the authcode
load_dotenv('./.env')
authcode = os.getenv('oc_authcode')
client_id = os.getenv('oc_client_id')
client_secret = os.getenv('oc_client_secret')


#code = "a62b678d5d290f973c22c4936fa0deed9990e76447642d7efd531ff952f15e66"

# Open Collective OAuth token URL
token_url = "https://opencollective.com/oauth/token"



# Request body as a dictionary
data = {
    "grant_type": "authorization_code",
    "client_id": client_id,
    "client_secret": client_secret,
    "code": f"{authcode}",
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
else:
    # If the request was not successful, print an error message
    print(f"Error: {response.status_code} - {response.text}")
