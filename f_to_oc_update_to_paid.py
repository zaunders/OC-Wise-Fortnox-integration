import requests
from dotenv import load_dotenv
import os


def payExpense(expense_id):
    load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
    accessToken = os.getenv("oc_access_token")
    OC_personal_development_token = os.getenv("OC_personal_development_token")

    # Set the headers with the API key if needed
    headers = {
        "authorization": f"Bearer {accessToken}",
        "Content-Type": "application/json"
    }
    
    # Define the GraphQL endpoint URL
    graphql_url = f"https://staging.opencollective.com/api/graphql/v2?personalToken={OC_personal_development_token}"


    ###################################################################################################################################
    # Mutation to pay the expense
    mutation = """
    mutation payExpense($expense: ExpenseReferenceInput!){
        processExpense(
            expense: $expense
            action: PAY
            message: "expense paid"
        ) {
            id
        }
    }
    """
    # Create a GraphQL request payload
    payload = {
        "query": mutation,
        "variables": {
            "expense": {
                "id": expense_id
            }
        }
    }

    # Requesting to create the expense at the account with the slug 
    try:
        # Send a POST request to the GraphQL endpoint
        response = requests.post(graphql_url, json=payload)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            data = response.json()
            expense_id = data['data']['processExpense']['id']
            #print("Successfully payed expense with id: " + expense_id)
            return expense_id

        else:
            print(f"Failed to pay expense. Status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return e


