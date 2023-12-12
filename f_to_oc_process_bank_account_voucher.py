# Getting all verifications from Fortnox and finding relevant ones
import json
from dotenv import load_dotenv
import os
from send_error_message_email import sendErrorEmail
import numpy as np
from fortnox_get_voucher_by_voucher_number import getVoucherByVoucherNumber
import time
from f_to_oc_addFunds import addFunds
from f_to_oc_create_and_process_expense import createAndProcessExpense
from get_matching_tables import getMatchingTables




# seperating this out to a seperate file and function because of the custom logic needs
def process_bankaccount_voucher(voucher_number):
    # Load the .env file and get the access token for fortnox
    load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
    relative_path=os.getenv("relative_path")

    OC_slug_lookup = getMatchingTables("OC_slug_lookup")

    voucher = getVoucherByVoucherNumber(voucher_number)
    #print(voucher)

    expenses_added = []
    collective_slug_for_funds = "granslandet"
    expense_project_slug_found = False
    expense_project_slug = ""
    voucher_processed = False

    # Check to see that description is found in lookup table
    for line in OC_slug_lookup:
        if line.get("word").lower() in voucher["Voucher"]["Description"].lower():
            expense_project_slug = line.get("slug")
            expense_project_slug_found = True
    

    for row in voucher["Voucher"]["VoucherRows"]:
            if row["Debit"] != 0:
                # Check that the row was not removed (an edit in the fortnox voucher creates a "removed" row)
                if row["Removed"] == False:
                    # Check if the debit is on the bank account side, that means money coming in and should be added to funds for gränslandet
                    if row["Account"] == 1940:
                        fund_addition_data = addFunds(int(100*row["Debit"]), collective_slug_for_funds, voucher["Voucher"]["Description"]+" (from voucher "+str(voucher_number)+")")
                        voucher_processed = True
                        print(str(row["Debit"])+" SEK added with description:")
                        print(voucher["Voucher"]["Description"])
                    else:
                        # Do not treat transfers from bank account to wise as expense for OC
                        if row["Account"] != 1941:
                            # check if the account is in the range of 2800-2899 (org liebilities)
                            if 2800 <= row["Account"] < 2900:
                                expense_project_slug = "granslandet"
                                expense_project_slug_found = True
                            
                            # Check that the expense project slug has been found
                            if expense_project_slug_found:
                                expense_added = createAndProcessExpense(expense_project_slug, int(100*row["Debit"]), voucher["Voucher"]["Description"]+" (from voucher "+str(voucher_number)+")")
                                # length of an id from open collective is 35 characters, if 35 we can assume success
                                if len(expense_added) == 35:
                                    voucher_processed = True
                                    print("expense added with description:")
                                    print(voucher["Voucher"]["Description"])
                                elif expense_added == "Insufficient funds":
                                    print("Insufficient funds for expense "+voucher["Voucher"]["Description"])
                                    sendErrorEmail("Insufficient funds for processing "+voucher["Voucher"]["Description"])
                            else:
                                print("Expense project slug not found for voucher "+str(voucher_number))
                                sendErrorEmail("Expense project slug not found for voucher "+str(voucher_number))

    return voucher_processed

#testing function, voucher 30 (expense) and 26 funds
#test = process_bankaccount_voucher(46)
#print(test)