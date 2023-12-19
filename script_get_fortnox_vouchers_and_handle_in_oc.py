# Getting all verifications from Fortnox and finding relevant ones
import json
from dotenv import load_dotenv
import os
from send_error_message_email import sendErrorEmail
import numpy as np
from f_to_oc_get_vouchers import getVouchers
from fortnox_get_voucher_by_voucher_number import getVoucherByVoucherNumber
from f_to_oc_process_bank_account_voucher import process_bankaccount_voucher
import time
from send_fortnox_to_oc_finished import sendFinishedOC

print("Starting script")
# Load the .env file and get the access token for fortnox
load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
relative_path=os.getenv("relative_path")

access_token = os.getenv('fortnox_access_token')

requests_done = 0
processed_vouchers = np.load(f'{relative_path}processed_vouchers.npy')
vouchers_with_info = []

# declaring empty list to track all expenses and funds created
created_expenses_html=[]

all_vouchers = getVouchers(0)
requests_done += 1
# parse the response and create an array that holds for each voucher the voucher number
all_vouchers_array = []
for voucher in all_vouchers["Vouchers"]:
    all_vouchers_array.append(voucher["VoucherNumber"])


# if there are more than 100 vouchers, get the rest of them
number_of_vouchers = all_vouchers["MetaInformation"]["@TotalResources"]
if number_of_vouchers > 100:
    extra_requests = int(np.ceil(number_of_vouchers/100)-1)
    for i in range(extra_requests):
        offset = (i+1)*100
        vouchers = getVouchers(offset)
        requests_done += 1
        for voucher in vouchers["Vouchers"]:
            all_vouchers_array.append(voucher["VoucherNumber"])
            #vouchers_with_info.append((voucher["VoucherNumber"], voucher["Description"]))

print(all_vouchers_array)
#print(vouchers_with_info)

# go through vouchers and get the ones that have not been processed and belong to bank account 1940
for current_voucher in all_vouchers_array:
    # the fortnox API has a limit of 25 requests per second, so we sleep for 5 seconds after 25 requests to avoid any errors
    if requests_done > 24:
        time.sleep(5)
        requests_done = 0


    needs_further_process = False

    #get the Voucher data if not already processed

    if current_voucher in processed_vouchers:
        print(f"Voucher {current_voucher} already processed")
    else:
        data = getVoucherByVoucherNumber(current_voucher)
        requests_done += 1

        print("Processing voucher:")
        print(current_voucher)


        for row in data["Voucher"]["VoucherRows"]:
            #print(row)
            # Only process the vouchers that are connected to the bank account
            if row["Account"] == 1940:
                needs_further_process = True
                print("bank account row found")


        if needs_further_process == True:
            # Handle voucher by either adding the funds or creating an expense from the voucher
            handled_response = process_bankaccount_voucher(data["Voucher"]["VoucherNumber"])
            requests_done += 1
            if handled_response == "expense created" or handled_response == "fund added":
                # Add the voucher as being processed to the list of processed vouchers so that it will not be done again
                new_expense = "Fortnox voucher: <b>"+str(data["Voucher"]["VoucherNumber"])+"</b>, with the description: <b>"+data["Voucher"]["Description"]+"</b> was successfully processed."
                created_expenses_html.append(new_expense)
                new_voucher = np.array([current_voucher])
                processed_vouchers = np.concatenate((processed_vouchers, new_voucher))
                np.save(f'{relative_path}processed_vouchers.npy', processed_vouchers)
            elif handled_response == "wise":
                # Add the voucher as being processed to the list of processed vouchers so that it will not be done again
                new_voucher = np.array([current_voucher])
                processed_vouchers = np.concatenate((processed_vouchers, new_voucher))
                np.save(f'{relative_path}processed_vouchers.npy', processed_vouchers)

        else:
            # Add the voucher as being processed to the list of processed vouchers so that it will not be done again
            new_voucher = np.array([current_voucher])
            processed_vouchers = np.concatenate((processed_vouchers, new_voucher))
            np.save(f'{relative_path}processed_vouchers.npy', processed_vouchers)
            
# email summary of expenses created
if created_expenses_html != []:
    sendFinishedOC(created_expenses_html)

