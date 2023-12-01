# Getting all verifications from Fortnox and finding relevant ones

from dotenv import load_dotenv
import os
import numpy as np


# Load the .env file and get the access token for fortnox
load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
relative_path=os.getenv("relative_path")
processed_vouchers = np.load(f'{relative_path}processed_vouchers.npy')

print(processed_vouchers)
