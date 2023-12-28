# Getting all verifications from Fortnox and finding relevant ones
import requests
import json
from dotenv import load_dotenv
import os
from send_error_message_email import sendErrorEmail
import numpy as np



# get voucher by Voucher number
def getVouchers(offset):
    # Load the .env file and get the access token for fortnox
    load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
    access_token = os.getenv('fortnox_access_token')

    # Define the API endpoint URL for creating vouchers
    api_url = f"https://api.fortnox.se/3/vouchers/"

    # Set up the request headers with your API token
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    params = {"offset":offset}

    try:
        # Send a POST request to create the voucher
        response = requests.get(api_url, headers=headers, params=params, headers=headers)

        # Check if the request was successful (HTTP status code 200 or 201)
        if response.status_code in {200, 201}:
            # Parse the JSON response
            vouchers = response.json()

            # Display the created voucher information
            #print(f"{voucher_response}")
            
            return vouchers

        else:
            print(f"Failed to get vouchers. Status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            sendErrorEmail(response.text)
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sendErrorEmail(e)
        return e
