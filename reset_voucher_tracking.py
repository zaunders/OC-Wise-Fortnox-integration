import numpy as np
from dotenv import set_key, load_dotenv
import os

# Load the .env file
load_dotenv("/home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/.env")
relative_path=os.getenv("relative_path")



processed_vouchers = np.array([0])

np.save(f'{relative_path}processed_vouchers.npy', processed_vouchers)

