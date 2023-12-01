import requests
from dotenv import load_dotenv
import os


def addFunds(amount, collective_slug, description):
    load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
    OC_personal_development_token=os.getenv("OC_personal_development_token")
    
    # Define the GraphQL endpoint URL
    graphql_url = f"https://staging.opencollective.com/api/graphql/v2?personalToken={OC_personal_development_token}"


    mutation = """
    mutation addFunds($account: AccountReferenceInput!, $amount: AmountInput!, $description: String!) {
        addFunds (
            fromAccount: $account
            account: $account
            amount: $amount
            description: $description
        ) {
            id
        }
    }   
    """
    # Create a GraphQL request payload
    payload = {
        "query": mutation,
        "variables": {
            "account": {
                "slug": collective_slug
            },
            "amount": {
                "valueInCents": amount
            },
            "description": description
        }
    }



    # Requesting to create the expense at the account with the slug 
    try:
        # Send a POST request to the GraphQL endpoint
        response = requests.post(graphql_url, json=payload)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            data = response.json()
            #funded_id = data['data']['processExpense']['id']
            print("Successfully added funds to collective with slug: " + collective_slug)
            return data

        else:
            print(f"Failed to approve expense. Status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return e


#testing
#test = addFunds(10000, "granslandet", "pengar från stripe (medlemmar)")
