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

# Load the .env file and get the access token for fortnox
load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
relative_path=os.getenv("relative_path")

# seperating this out to a seperate file and function because of the custom logic needs
def process_bankaccount_voucher(voucher_number):

    voucher = getVoucherByVoucherNumber(voucher_number)
    #print(voucher)
    debit_rows_info = []
    expenses_added = []
    collective_slug_for_funds = "granslandet"
    expense_project_slug = "infrastructure-2023"

    for row in voucher["Voucher"]["VoucherRows"]:
            if row["Debit"] != 0:
                if row["Removed"] == False:
                    #debit_rows_info.append((row["Account"], row["Debit"], row["Description"]))
                    if row["Account"] == 1940:
                        fund_addition_data = addFunds(int(100*row["Debit"]), collective_slug_for_funds, row["Description"]+"from voucher "+str(voucher_number))
                        print("fund added with description:")
                        print(row["Description"])
                    else:
                        expense_added = createAndProcessExpense(expense_project_slug, int(100*row["Debit"]), row["Description"]+"from voucher "+str(voucher_number))
                        print("expense added with description:")
                        print(row["Description"])
            
    
    return "expenses_processed"

#testing function, voucher 30 (expense) and 26 funds
#test = process_bankaccount_voucher(46)
#print(test)