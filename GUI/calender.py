import datetime
import os

import google.auth
from google.oauth2 import service_account
import googleapiclient.discovery


# Set up credentials and calendar API client
creds = None
# Set up credentials and calendar API client
def calendar_init():
    creds = service_account.Credentials.from_service_account_file(
        './ece477_key.json',
        scopes=['https://www.googleapis.com/auth/calendar'],
    )
    calendar_api = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    return calendar_api

def set_time():
    todays_time = datetime.datetime.now()
    current_year = todays_time.year
    current_month = todays_time.month
    current_day = todays_time.day
    one_day = datetime.timedelta(days=1)
    tomorrow_date = one_day + todays_time
    tomorrow_day = tomorrow_date.day

    start_date = datetime.datetime(current_year, current_month, current_day, 0, 0, 0).isoformat() + 'Z'  # 'Z' indicates UTC time
    end_date = datetime.datetime(current_year, current_month, tomorrow_day, 0, 0, 0).isoformat() + 'Z'

    return start_date, end_date
# retrieve events in date range
def retrieve_calendar_info(calendar_api, start_date, end_date): 
    events_result = calendar_api.events().list(calendarId='primary', timeMin=start_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    # print event summary and ID for each event
    for event in events:
        print(f"{event['summary']} ({event['id']})")
        print(event['description'])

def main():
    calendar_api = calendar_init()
    start_date, end_date = set_time()
    retrieve_calendar_info(calendar_api, start_date, end_date) 


if __name__ == "__main__":
    # call the main function
    main()    
#add an event
'''
# Create the event for April 26 at 10pm
event = {
    'summary': 'Example Event',
    'location': 'San Francisco',
    'description': 'This is an example event.',
    'start': {
        'dateTime': datetime.datetime(2023, 4, 26, 22, 0, tzinfo=datetime.timezone.utc).isoformat(),
        'timeZone': 'UTC',
    },
    'end': {
        'dateTime': datetime.datetime(2023, 4, 26, 23, 0, tzinfo=datetime.timezone.utc).isoformat(),
        'timeZone': 'UTC',
    },
    'reminders': {
        'useDefault': True,
    },
}
# Insert the event into the calendar
try:
    created_event = calendar_api.events().insert(calendarId='e5e1b4295b88651a4dc4fdfacc526f33547c980842641c4ad3e0fe8cf7099a34@group.calendar.google.com', body=event).execute()
    print(f'Event created: {created_event.get("htmlLink")}')
except HttpError as error:
    print(f'An error occurred: {error}')
'''
