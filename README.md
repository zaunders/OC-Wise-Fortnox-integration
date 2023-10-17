# OC-Wise-Fortnox-integration

## General information
This integration helps organisations that are reviewing transactions and expenses in Open Collective to automatically book them in Fortnox with links to all of the recipts and metadata needed.

It works by pulling completed transactions from Wise, finds all of the relevant information about those transactions from the Open Collective platform. It also pulls in a mapping of Fortnox accounts to projects slugs or tags in open collective so that it knows on what accounts to book the expenses in Fortnox.

For every voucher (verifikat in Swedish) a pdf of expense information is created and uploaded along with a .json file of the same information in case there is a need to read the information back out of Fortnox at some point.

## Deployment
The script runs daily. For it to work, the .env file must be edited manually to set the api keys for Wise, Open Collective and Fortnox. For Open Collective, authorization must be done every 3 months in order renew the access token. For Fortnox, the refresh token can be used so long as the script runs at least once every 30 days. 

## Fortnox matching
This is a provisional solution as OC is working on enabling collectives to specify the bookkeeping accounts directly on OC and then being able to choose which of the accounts an expense or invoice should be going towards.

For now, the matching table works by iterationg through the list of transactions/expenses and then checking first if the expense is a dream (by checking the slug), then go to the dream account, if not, check the the tags of the expense in order to find which account it should go to. 

## Authentication
### Fortnox
In order to authenticate the scripts and there is no longer a valid access & refresh token, a user that has the appropriate privileges in fortnox needs to click through an authentication and make sure a authentication code gets added to the .env file (either by writing it directly or emailing someone who can put it in)

The following URL will lead to authentication and once authenticated the redirect URL will contain the authcode that needs to be entered into the .env file:
https://apps.fortnox.se/oauth-v1/auth?client_id=b2g2khPkn8Y0&redirect_uri=https://darksoil.studio&scope=companyinformation%20supplier%20supplierinvoice%20bookkeeping%20connectfile&state=somestate123&access_type=offline&response_type=code&account_type=service



### Open Collective
Similar to Fortnox, in open collective the access token needs to be refreshed from time to time. An access token is valid for 90 days at Open collective. In order to retrieve a new authcode a user with adequate access will need to access through the following URL:
https://opencollective.com/oauth/authorize?client_id=e5393aa85430c0b1da1d&response_type=code&redirect_url=https://opencollective.com/borderland/&scope=email,account,expenses,transactions,orders

After authentication, the redirect URL will contain a parameter that is the authcode, this code must be entered into the .env file. Then the authscript will run so that the access token is exchanged for and is automatically updated in the .env file.
