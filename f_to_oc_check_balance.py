import requests
from dotenv import load_dotenv
import os

def checkBalance(slug):
    load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
    OC_personal_development_token=os.getenv("OC_personal_development_token")

    # Define the GraphQL endpoint URL
    graphql_url = f"https://staging.opencollective.com/api/graphql/v2?personalToken={OC_personal_development_token}"


    query = """
    query checkBalance($slug: String!) {
        project(
            slug: $slug
        ) {
            stats {
                balance {
                    valueInCents
                }
            }
        }
    }   
    """
    # Create a GraphQL request payload
    payload = {
        "query": query,
        "variables": {
            "slug": slug
            }
    }


    # Requesting to create the expense at the account with the slug 
    try:
        # Send a POST request to the GraphQL endpoint
        response = requests.post(graphql_url, json=payload)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            data = response.json()
            valueInCents = data['data']['project']['stats']['balance']['valueInCents']
            print("The project balance is: " + str(valueInCents))
            return valueInCents

        else:
            print(f"Failed to retrieve project balance. Status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return e

