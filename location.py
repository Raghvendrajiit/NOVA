from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    creds = None

    # Load credentials if available
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Refresh or re-authenticate if necessary
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())  # Try to refresh token
            except Exception as e:
                print("Token refresh failed. Deleting token and reauthenticating...")
                os.remove('token.pickle')
                creds = None  # Force re-authentication
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save new credentials
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_upcoming_events():
    creds = authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)

    events_result = service.events().list(
        calendarId='primary',
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        return "No upcoming events found."
    
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        location = event.get('location', 'No location')
        attendees = ', '.join([attendee['email'] for attendee in event.get('attendees', [])]) if 'attendees' in event else 'No attendees'
        description = event.get('description', 'No description')
        
        print(f"Event: {event['summary']}")
        print(f"Start: {start}")
        print(f"Location: {location}")
        print(f"Attendees: {attendees}")
        print(f"Description: {description}")
        print("=" * 40)
def create_event_with_reminder():
    creds = authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': 'Sample Event',
        'location': 'Online',
        'description': 'This is a test event.',
        'start': {
            'dateTime': '2025-01-30T10:00:00-07:00',  # Start time in ISO 8601 format
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2025-01-30T11:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},  # Popup reminder 10 minutes before
            ],
        },
    }

    event = service.events().insert(
        calendarId='primary',
        body=event
    ).execute()

    print(f"Event created: {event.get('htmlLink')}")
from datetime import datetime, timedelta

def get_events_for_today():
    creds = authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)

    today = datetime.utcnow().isoformat() + 'Z'  # Current time in UTC
    events_result = service.events().list(
        calendarId='primary',
        timeMin=today,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        return "No events for today."
    
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{event['summary']} - {start}")



create_event_with_reminder()