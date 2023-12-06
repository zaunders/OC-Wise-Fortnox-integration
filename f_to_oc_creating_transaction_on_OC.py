import requests
from dotenv import load_dotenv
import os



def createOCexpense(slug, amount, description):
    load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
    accessToken = os.getenv("oc_access_token")

    # Set the headers with the API key if needed
    headers = {
        "authorization": f"Bearer {accessToken}",
        "Content-Type": "application/json"
    }

    # Define the GraphQL endpoint URL
    graphql_url = f"https://staging.opencollective.com/api/graphql/v2"


    # check that there are sufficient funds in OC
    # if not, return error "insufficient funds"

    # Mutation to create the expense
    mutation = """
    mutation createOCexpense ($account: AccountReferenceInput!, $expense: ExpenseCreateInput!) {
        createExpense(
            expense: $expense
            account: $account
            ) 
        {
        id
        }
    }
    """

    # Create a GraphQL request payload
    payload = {
        "query": mutation,
        "variables": {
            "account": {
                "slug": slug
            },
            "expense": {
                "type": "INVOICE",
                "description": description,
                "items" : {
                    "description": description,
                    "amount": amount
                },
                "payee": {
                    "slug": slug
                },
                "payoutMethod": {
                        "type":"OTHER",
                        "data" : {
                            "content": 'Bank transfer / bankgiro'}
                }
            }
        }
    }
    

    # Requesting to create the expense at the account with the slug 
    try:
        # Send a POST request to the GraphQL endpoint
        response = requests.post(graphql_url, json=payload, headers=headers)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            data = response.json()
            expense_id = data['data']['createExpense']['id']
            #print("The expense was created successfully with id:"+expense_id)
            return expense_id

        else:
            print(f"Failed to create expense. Status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return e





