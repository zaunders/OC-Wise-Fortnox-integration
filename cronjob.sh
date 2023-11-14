#!/bin/bash

# refresh the fortnox token
python3 /home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/fortnox_exchange_refresh_token.py

echo "starting script.."
# run the integrationscript
python3 /home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/script_get_wise_transactions_book_and_match.py

echo "script finished!"