import requests
import json
from dotenv import load_dotenv
import os




# Create a connection between an uploaded file and a specific voucher
def createVoucherFileConnection(URL, FileId, VoucherNumber, VoucherSeries):

    # Load the .env file and get the access token for fortnox
    load_dotenv('./.env')
    access_token = os.getenv('fortnox_access_token')

    # Define the API endpoint URL for creating vouchers
    api_url = "https://api.fortnox.se/3/voucherfileconnections/"

    # Set up the request headers with your API token
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    # Define the voucher data in the format required by the API
    voucher_file_connection = {
        "VoucherFileConnection": {
            "@url": URL,
            "FileId": FileId,
            "VoucherDescription": "",
            "VoucherNumber": VoucherNumber,
            "VoucherSeries": VoucherSeries
        }
    }

    try:
        # Send a POST request to create the voucher
        response = requests.post(api_url, json=voucher_file_connection, headers=headers)
        
        # Check if the request was successful (HTTP status code 200 or 201)
        if response.status_code in {200, 201}:
            # Parse the JSON response
            voucher_connection_response = response.json()

            
            return voucher_connection_response

        else:
            print(f"Failed to connect file to Voucher. Status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return e