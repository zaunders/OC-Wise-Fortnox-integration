import requests
from remove_special_characters import remove_special_characters


def getExpensesFromOC(accessToken, offset, startDate):


    # Define the GraphQL endpoint URL
    graphql_url = "https://api.opencollective.com/graphql/v2"


    # Set the headers with the API key if needed
    headers = {
        "authorization": f"Bearer {accessToken}",
        "Content-Type": "application/json"
    }

    # Define your Open Collective collective's slug
    collective_slug = "borderland"

    # prepare list for storing and returning expenses
    OC_expense_list = []

    # Define the GraphQL query to retrieve expenses for the specified account
    query = """
    query GetExpensesByAccount($account: AccountReferenceInput!, $date: DateTime, $offset: Int) {
    expenses(
        account: $account
        includeChildrenExpenses: true
        limit:1000
        offset: $offset
        dateFrom: $date
        ) {
            nodes {
                id
                account {
                    slug
                }
                description
                legacyId
                tags
                type
                amountV2 {
                    value
                    currency
                }
                createdAt
                attachedFiles {
                    url
                    name
                }
                items  {
                    url
                }
                activities {
                    type
                    transaction {
                        merchantId
                    }
                }
            }
        }
    }
    """

    # Create a GraphQL request payload
    payload = {
        "query": query,
        "variables": {
            "account": {
            "slug": collective_slug
            },
        "date": startDate,
        "offset": offset
        }
    }

    # Requesting all expenses from OC and creating an array with one row per expense. 
    try:
        # Send a POST request to the GraphQL endpoint
        response = requests.post(graphql_url, json=payload, headers=headers)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            data = response.json()
            #print(data)
            expenses = data["data"]["expenses"]["nodes"]


            #writing expense information including attached files
            for expense in expenses:
                invoiceFiles = ""
                expenseItems = ""
                expenseTags = ""
                expenseId = expense['id']
                expenseAccountSlug = expense['account']['slug']
                expenseDescription = expense['description']
                clean_expenseDescription = remove_special_characters(expenseDescription)
                expenseLegacyId = expense['legacyId']
                expenseType = expense['type']
                expenseCreatedAt = expense['createdAt']
                expenseCurrency = expense['amountV2']['currency']
                expenseValue = expense['amountV2']['value']
                expenseMerchantId = ""
                expenseActivityTypes = ""
                #{expense['activities']['transaction']['merchantId']}

                if len(expenseDescription) > 198:
                    expenseDescription = expenseDescription[:198]

                if expense['tags']:
                    for tag in expense['tags']:
                        expenseTags += f"{tag}, "
                
                # Check if there are attached files
                if expense['attachedFiles']:
                    for attached_file in expense['attachedFiles']:
                        invoiceFiles += f"{attached_file['url']}; "


                elif expense['items']:
                    for item in expense['items']:
                        expenseItems += f"{item['url']}; "
                
                if expense['activities']:
                    for activity in expense['activities']:
                        activityType = f"{activity['type']}; "
                        expenseActivityTypes += f"{activityType}; "
                        
                        if activity['transaction']:
                            expenseMerchantId = activity['transaction']['merchantId']

                new_OC_expense = {
                    "MerchantId": expenseMerchantId, 
                    "AccountSlug": expenseAccountSlug, 
                    "Description": clean_expenseDescription, 
                    "LegacyId": expenseLegacyId, 
                    "Type": expenseType, 
                    "CreatedAt": expenseCreatedAt, 
                    "Currency": expenseCurrency, 
                    "Value": expenseValue, 
                    "Tags": expenseTags, 
                    "invoiceFiles": invoiceFiles, 
                    "items": expenseItems, 
                    "expenseActivityTypes" : expenseActivityTypes
                }
                OC_expense_list.append(new_OC_expense)
            return OC_expense_list



        else:
            print(f"Failed to retrieve expenses. Status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return e