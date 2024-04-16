import requests
import json
from dotenv import load_dotenv
import os


# Load the .env file and get the access token for fortnox


# 
def createVoucher(creation_date, description, transferId, value, debit_account, credit_account, transferFee):
    load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")    
    access_token = os.getenv('fortnox_access_token')

    # Define the API endpoint URL for creating vouchers
    api_url = "https://api.fortnox.se/3/vouchers"

    # Set up the request headers with your API token
    headers = {
        "Authorization": f"Bearer {access_token}",

    }

    # Define the voucher data in the format required by the API
    voucher_data = {
        "Voucher": {
            "VoucherSeries": "A",  # Replace with your voucher series
            "TransactionDate": creation_date,
            "Description": description,
            "Comments": transferId, # Wise transaction id
            "VoucherRows": [
                {
                    "Account": debit_account,  # Replace with the account number
                    "Debit": value,  # Replace with the debit amount
                    "Credit": 0.00
                },
                {
                    "Account": credit_account,  # Wise account
                    "Debit": 0.00,
                    "Credit": value+transferFee  # Replace with the credit amount
                },
                {
                    "Account": 6570,  # Transaction fees account
                    "Debit": transferFee,
                    "Credit": 0.00,  
                }
            ]
        }

    }

    try:
        # Send a POST request to create the voucher
        response = requests.post(api_url, json=voucher_data, headers=headers)

        
        # Check if the request was successful (HTTP status code 200 or 201)
        if response.status_code in {200, 201}:
            # Parse the JSON response
            voucher_response = response.json()

            # Display the created voucher information
            #print(f"{voucher_response}")
            
            return voucher_response

        else:
            print(f"Failed to create voucher. Status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return e
    


#test
#voucher = createVoucher("2023-08-01", "test", "test", 100, 6230, 1941)
#print(voucher)