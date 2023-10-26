import requests
import json
from dotenv import load_dotenv
import os
from send_error_message_email import sendErrorEmail
import numpy as np


# getting the booked voucher for transferId
def findVoucherNumber(transferId):
    # Getting the booked transfers array
    booked_transfers = np.load('booked_transfers.npy')
    #print(booked_transfers)
    just_ids = booked_transfers[:, 0]
    # Find the index where the first value matches
    index = np.where(just_ids == transferId)
    
    # If a match is found, return the corresponding second value
    if index[0].size > 0:
        return booked_transfers[index[0][0], 1]
    else:
        return None


"""
# Test
value_to_match = "506920466"
result = findVoucherNumber(value_to_match)
if result is not None:
    print(f"For the value {value_to_match}, the corresponding second value is {result}.")
else:
    print(f"No match found for the value {value_to_match}.")

"""