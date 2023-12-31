import requests
import json
from dotenv import load_dotenv
import os
from send_error_message_email import sendErrorEmail


# get voucher by Voucher number
def getVoucherByVoucherNumber(VoucherNumber):
    # Load the .env file and get the access token for fortnox
    load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
    relative_path=os.getenv("relative_path")
    access_token = os.getenv('fortnox_access_token')

    #always using voucher series A
    VoucherSeries = "A"

    # Define the API endpoint URL for creating vouchers
    api_url = f"https://api.fortnox.se/3/vouchers/{VoucherSeries}/{VoucherNumber}"

    # Set up the request headers with your API token
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

  

    try:
        # Send a POST request to create the voucher
        response = requests.get(api_url, headers=headers)

        # Check if the request was successful (HTTP status code 200 or 201)
        if response.status_code in {200, 201}:
            # Parse the JSON response
            voucher = response.json()

            # Display the created voucher information
            #print(f"{voucher_response}")
            
            return voucher

        else:
            print(f"Failed to get voucher. Status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            sendErrorEmail(response.text)
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sendErrorEmail(e)
        return e
    
#testing
#test = getVoucherByVoucherNumber(1)
#print (test)


"""
{'MetaInformation': 
    {'@TotalResources': 1, '@TotalPages': 1, '@CurrentPage': 1}, 
    'Vouchers': 
        [{'@url': 'https://api.fortnox.se/3/vouchers/A/1?financialyear=2', 'Comments': None, 'Description': 'ny', 'ReferenceNumber': '', 'ReferenceType': 'MANUAL', 'TransactionDate': '2022-07-13', 'VoucherNumber': 1, 'VoucherSeries': 'A', 'Year': 2, 'ApprovalState': 0}]}

        """