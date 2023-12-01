import numpy as np
from dotenv import set_key, load_dotenv
import os

# Load the .env file
load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
relative_path=os.getenv("relative_path")


booked_transfers = np.array([[0,0]])
refunded_transfers_booked = np.array([[0,0]])
unmatched_transfer_ids = np.array([0])
processed_vouchers = np.array([0])
np.save(f'{relative_path}booked_transfers.npy', booked_transfers)
np.save(f'{relative_path}refunded_transfers_booked.npy', refunded_transfers_booked)
np.save(f'{relative_path}unmatched_transfers_handled.npy', unmatched_transfer_ids)
np.save(f'{relative_path}processed_vouchers.npy', processed_vouchers)

