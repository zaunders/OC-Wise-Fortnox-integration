# OC-Wise-Fortnox-integration

## General information
This integration helps organisations that are reviewing transactions and expenses in Open Collective to automatically book them in Fortnox with links to all of the recipts and metadata needed.

It works by pulling completed transactions from Wise, finds all of the relevant information about those transactions from the Open Collective platform. It also pulls in a mapping of Fortnox accounts to projects slugs or tags in open collective so that it knows on what accounts to book the expenses in Fortnox.

For every voucher (verifikat in Swedish) a pdf of expense information is created and uploaded along with a .json file of the same information in case there is a need to read the information back out of Fortnox at some point.

## Deployment
The script runs daily. For it to work, the .env file must be edited manually to set the api keys for Wise, Open Collective and Fortnox. For Open Collective, authorization must be done every 3 months in order renew the access token. For Fortnox, the refresh token can be used so long as the script runs at least once every 30 days. 

