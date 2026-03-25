from icalendar import Calendar, Event
from caldav import DAVClient, Calendar as CalDAVCalendar
import requests
import os

def download_ics_file(ics_url, ics_file_path):
    """Download the remote .ics file to a local path."""
    response = requests.get(ics_url)
    response.raise_for_status()  # Raise an error for bad status codes
    with open(ics_file_path, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {ics_url} to {ics_file_path}")

def load_ics_to_baikal(ics_file_path, caldav_url, username, password):
    """Load events from a local .ics file into a Baïkal CalDAV calendar."""
    # Load the .ics file
    with open(ics_file_path, 'r') as f:
        ical_calendar = Calendar.from_ical(f.read())

    # Connect to the Baïkal CalDAV server
    client = DAVClient(
        url=caldav_url,
        username=username,
        password=password
    )

    # Get the calendar object
    try:
        calendar = client.calendar(url=caldav_url)
    except Exception as e:
        raise ValueError(f"Failed to access calendar: {e}")

    # Add each event from the .ics file to the Baïkal calendar
    events = [event for event in ical_calendar.subcomponents if isinstance(event, Event)]

    for event in events:
        try:
            calendar.save_event(event.to_ical().decode('utf-8'))
        except Exception as e:
            print(event)

    print(f"Successfully loaded events from {ics_file_path} to CalDav calendar.")

def main():
    ics_file_path = "downloaded_events.ics"

    # Step 1: Download the remote ICS file
    download_ics_file(os.getenv('ICS_URL'), ics_file_path)

    # Step 2: Load the events into Baïkal
    load_ics_to_baikal(ics_file_path, os.getenv('CALDAV_URL'), os.getenv('USERNAME'), os.getenv('PASSWORD'))

if __name__ == "__main__":
    main()
