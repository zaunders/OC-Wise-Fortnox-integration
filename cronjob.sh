#!/bin/bash

# refresh the fortnox token
python3 /home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/fortnox_exchange_refresh_token.py

echo "starting wise transactions script.."
# run the integrationscript
python3 /home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/script_get_wise_transactions_book_and_match.py
echo "script taking wise transactions and booking them in fortnox finished!"

echo "starting fortnox reading script.."
# run the script that takes the fortnox transactions and matches them with the wise transactions
python3 /home/viktor/Documents/OC-coding/OC-Wise-Fortnox-integration/script_get_fortnox_vouchers_and_handle_in_oc.py

echo "script reading bookings from fortnox and creating OC expenses finished!"
