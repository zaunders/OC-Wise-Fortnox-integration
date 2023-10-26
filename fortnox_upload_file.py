import requests
from dotenv import load_dotenv
import os


# Upload a file to fortnox with the supplied file path
def uploadFile(fileURL):

    # Load the .env file and get the access token for fortnox
    load_dotenv('./.env')
    access_token = os.getenv('fortnox_access_token')

    files = {'file': open(fileURL, 'rb')}

    # Define the API endpoint URL for creating vouchers
    api_url = "https://api.fortnox.se/3/inbox/"

    # Set up the request headers with your API token
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    json_data = {"path":"Inbox_v"}

    try:
        # Send a POST request to create the voucher
        response = requests.post(api_url, files=files, headers=headers, json=json_data)

        # Check if the request was successful (HTTP status code 200 or 201)
        if response.status_code in {200, 201}:
            # Parse the JSON response
            file_upload_response = response.json()

            # Display the created voucher information
            #print(file_upload_response)
            return file_upload_response

        else:
            print(f"Failed to create voucher. Status code: {response.status_code}")
            print("Response Content:")
            #print(response.text)
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return e


