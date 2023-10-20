# OC-Wise-Fortnox-integration

## General information
This integration helps organisations that are reviewing transactions and expenses in Open Collective to automatically book them in Fortnox with links to all of the recipts and metadata needed.

It works by pulling completed transactions from Wise, finds all of the relevant information about those transactions from the Open Collective platform. It also pulls in a mapping of Fortnox accounts to projects slugs or tags in open collective so that it knows on what accounts to book the expenses in Fortnox.

For every voucher (verifikat in Swedish) a pdf of expense information is created and uploaded along with a .json file of the same information in case there is a need to read the information back out of Fortnox at some point.

## Deployment
The script runs daily. For it to work, the .env file must be edited manually to set the api keys for Wise, Open Collective and Fortnox. For Open Collective, authorization must be done every 3 months in order renew the access token. For Fortnox, the refresh token can be used so long as the script runs at least once every 30 days. 

## Financial year
When creating a voucher, what financial year it is put into is determained by the booking date of the voucher, **fortnox will select the bookkeeping year that corresponds to the voucher booking date**.

File uploads are not connected to a specific year at all and will all just go into a folder (currently inbox_v which stands for vouchers).

A tricky and not so great thing is that voucher file connections, the entry that connects an uploaded file and a voucher, take as input voucher number and series. However they DO NOT take year as a parameter and after checking with fortnox support it seems that the only way to choose which year the POST to https://api.fortnox.se/3/voucherfileconnections/ is going to use is by setting the default active year in the book keeping interface. 

IF SOMEONE CHANGES THIS DEFAULT TO ANOTHER YEAR THERE WILL BE NO CONNECTIONS BETWEEN FILES AND VOUCHERS

This setting is found by loggin into fortnox, clicking calendar symbol with currently viewed year after it:
![calendar icon](https://raw.githubusercontent.com/zaunders/OC-Wise-Fortnox-integration/main/images/fortnox_calendar_year.png "click calendar")


Then going to the edit section (Skapa nytt / redigera / radera år):
![year picker](https://raw.githubusercontent.com/zaunders/OC-Wise-Fortnox-integration/main/images/year_settings.png "pick year")


Then clicking on the year that you want to set as default:
![select year](https://raw.githubusercontent.com/zaunders/OC-Wise-Fortnox-integration/main/images/yes_to_default.png "select default")

Then choosing YES for "Öppna detta räkenskapsår vid inlogg"




## Fortnox matching
This is a provisional solution as OC is working on enabling collectives to specify the bookkeeping accounts directly on OC and then being able to choose which of the accounts an expense or invoice should be going towards.

For now, the matching table works by iterationg through the list of transactions/expenses and then checking first if the expense is a dream (by checking the slug), then go to the dream account, if not, check the the tags of the expense in order to find which account it should go to. 

## Authentication

### Fortnox
In order to authenticate the scripts and there is no longer a valid access & refresh token, a user that has the appropriate privileges in fortnox needs to click through an authentication and make sure a authentication code gets added to the .env file (either by writing it directly or emailing someone who can put it in)

The following URL will lead to authentication and once authenticated the redirect URL will contain the authcode that needs to be entered into the .env file:
https://apps.fortnox.se/oauth-v1/auth?client_id=b2g2khPkn8Y0&redirect_uri=https://darksoil.studio&scope=companyinformation%20inbox%20bookkeeping%20connectfile&state=somestate123&access_type=offline&response_type=code&account_type=service

Once an access token has been recived, there is also a refresh token recieved and while the access token only lasts for 1 hour at fortnox, the refresh token lasts for 31 days. So at any time within those 31 days the refresh token can be exchange for a new access token, which also provides a new refresh token so the process is repeated every time the script is run. **Therefore this script should only have to authenticate agains Fortnox once and then be continually refreshed on an ongoing basis.**

### Open Collective
Similar to Fortnox, in open collective the access token also becomes invalid over time. **An access token is valid for 90 days at Open collective**. After that a new authcode needs to be retrieved and put into the .env file. In order to do so, a user with adequate access will need to access through the following URL:
https://opencollective.com/oauth/authorize?client_id=e5393aa85430c0b1da1d&response_type=code&redirect_url=https://opencollective.com/borderland/&scope=email,account,expenses,transactions,orders

After authentication, the redirect URL will contain a parameter called **authcode**, this code must be entered into the .env file. Then the authentication script can then be run run so that the access token is recived and is automatically updated in the .env file.

### Wise
Wise uses a permanent API token so it does not have to be authenticated manually.
