import requests
#import csv
from dotenv import set_key, load_dotenv
import os
from datetime import datetime
from make_transaction_pdf import make_voucher_pdf
from make_transaction_json import makeJson
from oc_get_expenses import getExpensesFromOC
from get_matching_table import getMatchingTable
from fortnox_create_voucher import createVoucher
from fortnox_upload_file import uploadFile
from fortnox_create_file_connection import createVoucherFileConnection
import numpy as np
from send_error_message_email import sendErrorEmail
from send_transfer_not_found import sendTransferNotFound
from find_voucher_number import findVoucherNumber
from fortnox_get_voucher_by_voucher_number import getVoucherByVoucherNumber
from send_oc_token_expiring import sendOcExpiring
from get_time_since_day import get_time_since_created
import time



##############################################################################################################
#  Setting up the variables for the script                                                    
#                
#  Expenses in OC may be added before the opening of the bookkeeping year but closed after, therefore
#  it is useful to set an OC start date that is well before the bookkeeping year start in order to get all
#  the matching information. There really is no need to limit the end dates as the script will only book
#  transactions that have not been booked before.
##############################################################################################################

# Load the .env file
load_dotenv('./.env')
relative_path=os.getenv("relative_path")


#Check when OC token was created and if it is expiring soon, send an email
age_of_token = get_time_since_created()



print("days since OC token was created: "+str(age_of_token))
if age_of_token == 75:
    sendOcExpiring(age_of_token)
elif age_of_token > 86:
    sendOcExpiring(age_of_token)


 

#set the access tokens
wise_api_token = os.getenv("wise_api_token")
oc_access_token = os.getenv("oc_access_token")
fortnox_access_token = os.getenv("oc_access_token")

# Get the current date amd format to YYYY-MM-DD
current_date = datetime.now()
today_date_formatted = current_date.strftime('%Y-%m-%d')

# between which dates are we getting transactions Wise
wise_start_date=os.getenv("wise_start_date")     
wise_end_date=os.getenv("wise_end_date") 
#wise_end_date=today_date_formatted

# OC expense start and end dates for getting information
oc_start_date=os.getenv("oc_start_date") 
#oc_end_date="2023-10-26"

# setting upp the json objects needed
Wise_completed_transactions = []
Wise_transactions_refunded = []
OC_expense_list = []
unmatched_Wise_transactions = []

# Set up account matching dictionary
fortnox_account_lookup = getMatchingTable()

# Storing a list of booked transfers, this is checked to avoid double booking (recovering a spammed Fortnox account would be a pain)
# the list is also a lookup table for the Fortnox voucher number for each recorded transaction (used for booking refunded transactions)
booked_transfers = np.load(f'{relative_path}booked_transfers.npy')
refunded_transfers_booked = np.load(f'{relative_path}refunded_transfers_booked.npy')




##############################################################################################################
#  Getting transactions from Wise                                                                            #
##############################################################################################################

# Define the API endpoint URL
api_url = f"https://api.transferwise.com/v1/transfers?profile=25518118&limit=100&createdDateStart={wise_start_date}&createdDateEnd={wise_end_date}"

# Set up the request headers with your API token
headers = {
    "Authorization": f"Bearer {wise_api_token}",
}

# get all the rows from Wise (using offset to get 100rows at a time (max per request is 200))
offset = 0
for i in range(1, 20):

    try:
        # Send a GET request to retrieve the list of transfers
        response = requests.get(api_url, headers=headers, params={"offset": offset})

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            transfers = response.json()
            #print(transfers)

                # Iterate through the transfers and write each transfer to the CSV file
            for transfer in transfers:
                transfer_id = transfer["id"]
                status = transfer["status"]
                detailReference = transfer["details"]["reference"]
                created = transfer["created"]
                source_currency = transfer["sourceCurrency"]
                source_value = transfer["sourceValue"]
                customer_transaction_id = transfer["customerTransactionId"]
                targetAccount = transfer["targetAccount"]


                new_Wise_transaction = {
                    "transferId": str(transfer_id), 
                    "status": status, 
                    "created": created, 
                    "value": source_value, 
                    "detailReference": detailReference,
                    "targetAccount": targetAccount
                    }
                if status == "outgoing_payment_sent":
                    Wise_completed_transactions.append(new_Wise_transaction)
                elif status == "funds_refunded":
                    Wise_transactions_refunded.append(new_Wise_transaction)
        

        else:
            print(f"Failed to retrieve transfers. Status code: {response.status_code}")
            sendErrorEmail(response.text)


    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sendErrorEmail(e)
    offset += 100


# Counting the number of completed transactions
count = len(Wise_completed_transactions)
print ("rows in wise completed:")
print(count)




# Getting all the rows relevant from OC (use offset to get more then 1000 rows from OC)
OC_expense_list = getExpensesFromOC(oc_access_token, 0, oc_start_date)
OC_expenses_2 = getExpensesFromOC(oc_access_token, 1000, oc_start_date)
full_expenses = OC_expense_list + OC_expenses_2

count = len(OC_expense_list)
print ("All rows from OC:")
print (len(full_expenses))  


##############################################################################################################
#  Joining the transactions from Wise and OC                                                                 #
##############################################################################################################

# get list of unmached transfers that have already been processed
processed = np.load(f'{relative_path}unmatched_transfers_handled.npy')


def join_transactions(Wise_completed_transactions, full_expenses, key_wise, key_oc):
    """
    wise_transactions: List of transactions from Wise.
    oc_expenses: List of expenses from OC.
    key_wise: The key in the wise_transactions items to join on.
    key_oc: The key in the oc_expenses items to join on.
    
    Returns a list of dictionaries containing all keys and values 
    from wise_transactions and oc_expenses for each matched pair.
    """
    joined_list = []

    for wise in Wise_completed_transactions:
        transaction_matched = False
        for oc in full_expenses:
            if str(wise[key_wise]) == str(oc[key_oc]):
                # Joining the transactions by adding keys and values from both dictionaries
                joined_transaction = {**wise, **oc}
                joined_list.append(joined_transaction)
                # Break the inner loop after a match is found, assuming unique keys in oc_expenses
                transaction_matched = True
                break 
        if not transaction_matched:
            # when the balance is topped-up in Wise, the recieved transaction shows up in the list with the target account: 223368720
            if wise["targetAccount"] != 223368720:
                unmatched_Wise_transactions.append(wise)
                if not wise["transferId"] in processed:
                    sendTransferNotFound(wise["transferId"])
                    # Add the transferId to the list of handled unmached items so that email is not sent next time it is encountered
                    trasfer_emailed = np.array([wise["transferId"]])
                    unmatched_transfers_handled = np.concatenate((processed, trasfer_emailed))
                    np.save(f'{relative_path}unmatched_transfers_handled.npy', unmatched_transfers_handled)



    return joined_list

# Joining the wise and oc information for each Wise-transaction
transactions_with_oc_info = join_transactions(Wise_completed_transactions, full_expenses, 'transferId', 'MerchantId')
count = len(transactions_with_oc_info)
print ("rows in joined list:")
print (count)



##############################################################################################################
# Go through the joined transactions, create pdf and push the transactions into Fortnox at the right account #
##############################################################################################################

# Getting the list of just transferIds that have been booked
booked_transaction_ids = booked_transfers[:, 0]

# Setting a variable that keeps track of requests, fortnox has a cap of 25 requests per 5 seconds, the loop makes 5 requests so it should wait after every 5 loops in order to never break the script due to doing to many requests
requests_made_to_fortnox = 0

for item in transactions_with_oc_info:
    # Wait 5 seconds after at least 25 requests
    if requests_made_to_fortnox > 24:
        time.sleep(5)
        requests_made_to_fortnox = 0

    if not item.get("transferId") in booked_transaction_ids:

        # Create a pdf for each transaction
        pdf_path = make_voucher_pdf(item.get("transferId"), item.get("created"), item.get("value"), item.get("AccountSlug"), item.get("Description"), item.get("LegacyId"), item.get("Tags"), item.get("invoiceFiles"), item.get("items"))
        
        # Create a .json file for each transaction
        json_path = makeJson(item.get("transferId"), item.get("created"), item.get("value"), item.get("AccountSlug"), item.get("Description"), item.get("LegacyId"), item.get("Tags"), item.get("invoiceFiles"), item.get("items"))
    
        ## the account 6994 is set as "uncategorized costs" which would be moved later in the bookkeeping, it is for unmatched expenses
        booking_account = 6994
        found_booking_account = False

        # Find the right booking account in Fortnox, if unfound, the uncategorized account code remains
        for account_codes in fortnox_account_lookup:
            if item.get("AccountSlug") == account_codes.get("name"):
                booking_account = account_codes.get("account")
                found_booking_account = True
                break
            elif item.get("tags") != None:
                if account_codes.get("name").lower() in item.get("tags").lower():
                    booking_account = account_codes.get("account")
                    found_booking_account = True
                    break
        

        
        # booking the transaction into fortnox (Wise transactionId is the transferId)
        bookedVoucher = createVoucher(item.get("created")[:10], item.get("Description"), item.get("transferId"), item.get("value"), booking_account, 1941)
        
        # Add the booked transfer to the list of booked transfers as long as it returned a valid object
        if bookedVoucher["Voucher"]["Comments"] != None:
            # Create a new array with the new transfer
            newTransfer = np.array([[bookedVoucher["Voucher"]["Comments"], bookedVoucher["Voucher"]["VoucherNumber"]]])

            # Concatenate existing array and save, this will do a new file write for every record, my be resource intensive but will not lose data if script crashes
            booked_transfers = np.concatenate((booked_transfers, newTransfer))
            np.save(f'{relative_path}booked_transfers.npy', booked_transfers)


        # uploading the pdf file
        uploaded_pdf = uploadFile(pdf_path)
        uploaded_url = uploaded_pdf["File"]["@url"]
        uploaded_file_id = uploaded_pdf["File"]["Id"]
        #print("uploaded pdf resonse:")
        #print(uploaded_url)

        # Uploading .json
        uploaded_json = uploadFile(json_path)
        uploaded_json_url = uploaded_json["File"]["@url"]
        uploaded_json_file_id = uploaded_json["File"]["Id"]
        #print("uploaded json resonse:")
        #print(uploaded_json_url)

        # Connect files to voucher
        pdf_file_connection = createVoucherFileConnection(uploaded_url, uploaded_file_id, bookedVoucher["Voucher"]["VoucherNumber"], bookedVoucher["Voucher"]["VoucherSeries"])
        json_file_connection = createVoucherFileConnection(uploaded_json_url, uploaded_json_file_id, bookedVoucher["Voucher"]["VoucherNumber"], bookedVoucher["Voucher"]["VoucherSeries"])

        
        print (f"booked voucher: {bookedVoucher['Voucher']['VoucherNumber']} with connected file: {pdf_file_connection['VoucherFileConnection']['@url']}")
    
    
#  Setting current date as the last time that the script has been run successfully                       
set_key('.env', 'last_completed_run_date', today_date_formatted)



##############################################################################################################
#  Checking for refunded transactions and booking them into Fortnox                                         #
##############################################################################################################
# Getting the list of just transferIds that have been handled as refunded transfers
refunded_ids = refunded_transfers_booked[:, 0]



# Go through the list of refunded transfers, if they have been booked before and have not been handled as refunds yet, book the reverse of the original voucher in Fortnox
for item in Wise_transactions_refunded:
    # Make sure the refunded transfer has been booked in Fortnox in the first place
    if item.get("transferId") in booked_transaction_ids:
        # Check if the refund has already been handled
        if not item.get("transferId") in refunded_ids:
            # get the voucher information of the original transfer
            voucher_number = findVoucherNumber(item.get("transferId"))
            voucher_to_reverse = getVoucherByVoucherNumber(voucher_number)
            # create a reverse voucher with reference to the original voucher and book it into Fortnox
            reverse_description = f"Refunded bounced payment booked in voucher: A{reverse_voucher['Voucher']['VoucherNumber']}"
            reverse_comment = f"Refunded transferId: {reverse_voucher['Voucher']['Comments']}"
            debit_account = reverse_voucher['Voucher']['VoucherRows'][0]['Account']
            debit_amount = reverse_voucher['Voucher']['VoucherRows'][0]['Debit']
            credit_account = reverse_voucher['Voucher']['VoucherRows'][1]['Account']
            
            # Putting the credit account before the debit account in order to reverse the booked voucher
            reverse_voucher = createVoucher(item.get("created")[:10], reverse_description, reverse_comment, debit_amount, credit_account, debit_account)
            print("reverse booked")
            print(reverse_voucher)

             # Add the booked transfer to the list of refunded transfers as long as it returned a valid object
            if reverse_voucher["Voucher"]["Comments"] != None:
                # Create a new array with the new transfer
                newTransfer = np.array([[reverse_voucher["Voucher"]["Comments"], reverse_voucher["Voucher"]["VoucherNumber"]]])

                # Concatenate existing array and save, this will do a new file write for every record, my be resource intensive but will not lose data if script crashes
                refunded_transfers_booked = np.concatenate((refunded_transfers_booked, newTransfer))
                np.save(f'{relative_path}refunded_transfers_booked.npy', refunded_transfers_booked)



"""
##############################################################################################################
# Printing all collections to CSVs for debugging
##############################################################################################################

#Specify the file path where you want to save the data as a CSV file
csv_file_path = "test_OC_rows.csv"
#print(OC_expense_list)

#Open the CSV file in write mode
with open(csv_file_path, mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=",")
    # Write the header row to the CSV file
    csv_writer.writerow(["MerchantId", "AccountSlug", "Description", "LegacyId", "Type", "CreatedAt", "Currency", "Value", "Tags", "invoiceFiles", "items", "expenseActivityTypes"])

for item in full_expenses:
    # Open the CSV file in append mode
    with open(csv_file_path, mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        # Write the transfer data to the CSV file
        csv_writer.writerow([item.get("MerchantId"), item.get("AccountSlug"), item.get("Description"), item.get("LegacyId"), item.get("Type"), item.get("CreatedAt"), item.get("Currency"), item.get("Value"), item.get("Tags"), item.get("invoiceFiles"), item.get("items"), item.get("expenseActivityTypes")])



#Specify the file path where you want to save the data as a CSV file
csv_file_path = "test_Combined.csv"

#Open the CSV file in write mode
with open(csv_file_path, mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=",")
    # Write the header row to the CSV file
    csv_writer.writerow(["TransferId", "Status", "created", "value", "merchantId", "AccountSlug", "Description", "LegacyId", "Type", "CreatedAt", "Currency", "Value", "Tags", "invoiceFiles", "Items"])

for item in transactions_with_oc_info:
    # Open the CSV file in append mode
    with open(csv_file_path, mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        # Write the transfer data to the CSV file
        csv_writer.writerow([item.get("transferId"), item.get("status"), item.get("created"), item.get("value"), item.get("MerchantId"), item.get("AccountSlug"), item.get("Description"), item.get("LegacyId"), item.get("Type"), item.get("CreatedAt"), item.get("Currency"), item.get("Value"), item.get("Tags"), item.get("invoiceFiles"), item.get("items")])



# Writing completed transactions to a File
csv_file_path = "test_wise_completed.csv"
#Open the CSV file in write mode
with open(csv_file_path, mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=",")
    # Write the header row to the CSV file
    csv_writer.writerow(["transferId", "status", "created", "value"])

for item in Wise_completed_transactions:
    # Open the CSV file in append mode
    with open(csv_file_path, mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        # Write the transfer data to the CSV file
        csv_writer.writerow([item.get("transferId"), item.get("status"), item.get("created"), item.get("value")])


# Writing refunded transactions to a File
csv_file_path = "test_wise_refunded.csv"
#Open the CSV file in write mode
with open(csv_file_path, mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=",")
    # Write the header row to the CSV file
    csv_writer.writerow(["transferId", "status", "created", "value"])

for item in Wise_transactions_refunded:
    # Open the CSV file in append mode
    with open(csv_file_path, mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        # Write the transfer data to the CSV file
        csv_writer.writerow([item.get("transferId"), item.get("status"), item.get("created"), item.get("value")])



# Writing unmatched transactions to a File
csv_file_path = "test_wise_unmatched.csv"
#Open the CSV file in write mode
with open(csv_file_path, mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=",")
    # Write the header row to the CSV file
    csv_writer.writerow(["transferId", "status", "created", "value", "detailReference", "targetAccount"])

for item in unmatched_Wise_transactions:
    # Open the CSV file in append mode
    with open(csv_file_path, mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        # Write the transfer data to the CSV file
        csv_writer.writerow([item.get("transferId"), item.get("status"), item.get("created"), item.get("value"), item.get("detailReference"), item.get("targetAccount")])


"""