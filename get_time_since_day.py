import datetime
from dotenv import set_key, load_dotenv
import os

def get_time_since_created():
    # Load the .env file
    load_dotenv('./.env')
    token_date=os.getenv("oc_access_token_created")
    datetime_created = datetime.datetime.strptime(token_date, '%Y-%m-%d')
    time_now = datetime.datetime.now()
    days_since_create = abs(time_now-datetime_created).days
    return days_since_create

