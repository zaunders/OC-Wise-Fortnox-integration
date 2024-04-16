import requests
import os
from dotenv import set_key, load_dotenv


def wise_get_fee_for_transaction(Uuid):

    # Load the .env file
    load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
    relative_path=os.getenv("relative_path")


    #set the access tokens
    wise_api_token = os.getenv("wise_api_token")

    #gränslandet profile
    profile_id = 25518118

    # Set up the request headers with your API token
    headers = {"Authorization": f"Bearer {wise_api_token}"}

    # get qoute for a specific transaction
    api_url_quote = f"https://api.transferwise.com//v3/profiles/{profile_id}/quotes/{Uuid}"
    response_quote = requests.get(api_url_quote, headers=headers)
    response_json = response_quote.json()
    
    fee_options = response_json['paymentOptions']
    for option in fee_options:
        if option['payOut'] == 'BANK_TRANSFER' and option['payIn'] == 'BALANCE':
            fee = option['fee']['total']

    return fee

testfee = wise_get_fee_for_transaction('3c0dfaa8-6594-4f21-9c6a-2f328e66d9e4')
print(testfee)