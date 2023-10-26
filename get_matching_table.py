import requests
import json


def getMatchingTable ():
    # Define the URL of the JSON file on GitHub
    url = "https://raw.githubusercontent.com/zaunders/OC-Wise-Fortnox-integration/main/fortnox_account_lookup.json"

    try:
        # Fetch the JSON data from the URL
        response = requests.get(url)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the JSON data
            json_data = response.json()

            # Now, you can work with the JSON data as a Python dictionary
            return json_data

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return response.status_code

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return e

