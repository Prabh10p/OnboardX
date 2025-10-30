"""
Calendar Integration Utilities
Supports Google Calendar, Outlook, and iCal formats
"""

from datetime import datetime, timedelta
from icalendar import Calendar, Event as iCalEvent
import pytz

class CalendarIntegration:
    """Handle calendar integrations and event creation"""
    
    def __init__(self):
        self.timezone = pytz.timezone('America/New_York')
    
    def create_ical_event(self, meeting_data):
        """
        Create an iCal event that can be downloaded
        Compatible with Google Calendar, Outlook, Apple Calendar
        """
        cal = Calendar()
        cal.add('prodid', '-//OnboardX Meeting//onboardx.com//')
        cal.add('version', '2.0')
        
        event = iCalEvent()
        
        # Parse meeting data
        meeting_date = datetime.fromisoformat(meeting_data['date'])
        meeting_time = datetime.fromisoformat(meeting_data['time']).time()
        start_dt = datetime.combine(meeting_date, meeting_time)
        start_dt = self.timezone.localize(start_dt)
        
        # Calculate duration
        duration_minutes = int(meeting_data['duration'].split()[0])
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        
        # Add event details
        event.add('summary', meeting_data['title'])
        event.add('dtstart', start_dt)
        event.add('dtend', end_dt)
        event.add('dtstamp', datetime.now(self.timezone))
        
        # Add description
        description = f"Meeting Type: {meeting_data['type']}\n"
        if meeting_data.get('agenda'):
            description += f"\nAgenda:\n{meeting_data['agenda']}"
        event.add('description', description)
        
        # Add attendees
        if meeting_data.get('attendees'):
            for attendee in meeting_data['attendees']:
                event.add('attendee', f'MAILTO:{attendee}')
        
        # Add location for in-person meetings
        if meeting_data['type'] == 'In-Person':
            event.add('location', meeting_data.get('location', 'Office'))
        elif meeting_data['type'] == 'Virtual (Zoom)':
            event.add('location', meeting_data.get('zoom_link', 'Zoom link will be shared'))
        
        # Add reminder (15 minutes before)
        event.add('trigger', timedelta(minutes=-15))
        
        cal.add_component(event)
        
        return cal.to_ical()
    
    def generate_google_calendar_link(self, meeting_data):
        """Generate a Google Calendar 'Add to Calendar' link"""
        meeting_date = datetime.fromisoformat(meeting_data['date'])
        meeting_time = datetime.fromisoformat(meeting_data['time']).time()
        start_dt = datetime.combine(meeting_date, meeting_time)
        
        duration_minutes = int(meeting_data['duration'].split()[0])
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        
        # Format for Google Calendar
        start_str = start_dt.strftime('%Y%m%dT%H%M%S')
        end_str = end_dt.strftime('%Y%m%dT%H%M%S')
        
        title = meeting_data['title'].replace(' ', '+')
        description = meeting_data.get('agenda', '').replace('\n', '%0A').replace(' ', '+')
        location = meeting_data.get('location', '').replace(' ', '+')
        
        # Build Google Calendar URL
        base_url = "https://calendar.google.com/calendar/render?action=TEMPLATE"
        url = f"{base_url}&text={title}&dates={start_str}/{end_str}"
        url += f"&details={description}&location={location}"
        
        return url
    
    def generate_outlook_calendar_link(self, meeting_data):
        """Generate an Outlook 'Add to Calendar' link"""
        meeting_date = datetime.fromisoformat(meeting_data['date'])
        meeting_time = datetime.fromisoformat(meeting_data['time']).time()
        start_dt = datetime.combine(meeting_date, meeting_time)
        
        duration_minutes = int(meeting_data['duration'].split()[0])
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        
        # Format for Outlook
        start_str = start_dt.strftime('%Y-%m-%dT%H:%M:%S')
        end_str = end_dt.strftime('%Y-%m-%dT%H:%M:%S')
        
        title = meeting_data['title']
        description = meeting_data.get('agenda', '')
        location = meeting_data.get('location', '')
        
        # Build Outlook URL
        base_url = "https://outlook.live.com/calendar/0/deeplink/compose"
        url = f"{base_url}?subject={title}&startdt={start_str}&enddt={end_str}"
        url += f"&body={description}&location={location}"
        
        return url
    
    def get_meeting_summary_email(self, meeting_data, recipient_name):
        """Generate email summary for meeting invitation"""
        meeting_date = datetime.fromisoformat(meeting_data['date'])
        meeting_time = datetime.fromisoformat(meeting_data['time']).time()
        
        email_body = f"""
Hi {recipient_name},

You have a new meeting request:

📅 Meeting: {meeting_data['title']}
🕒 Date & Time: {meeting_date.strftime('%A, %B %d, %Y')} at {meeting_time.strftime('%I:%M %p')}
⏱️ Duration: {meeting_data['duration']}
📍 Type: {meeting_data['type']}

"""
        
        if meeting_data.get('agenda'):
            email_body += f"\n📋 Agenda:\n{meeting_data['agenda']}\n"
        
        email_body += """
Please accept or decline this meeting request.

Best regards,
OnboardX Team
"""
        
        return email_body
    
    def sync_with_google_calendar(self, user_credentials, meeting_data):
        """
        Sync meeting with Google Calendar API
        Requires OAuth2 credentials
        """
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            
            # Build service
            service = build('calendar', 'v3', credentials=user_credentials)
            
            meeting_date = datetime.fromisoformat(meeting_data['date'])
            meeting_time = datetime.fromisoformat(meeting_data['time']).time()
            start_dt = datetime.combine(meeting_date, meeting_time)
            
            duration_minutes = int(meeting_data['duration'].split()[0])
            end_dt = start_dt + timedelta(minutes=duration_minutes)
            
            event = {
                'summary': meeting_data['title'],
                'description': meeting_data.get('agenda', ''),
                'start': {
                    'dateTime': start_dt.isoformat(),
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'dateTime': end_dt.isoformat(),
                    'timeZone': 'America/New_York',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 15},
                        {'method': 'email', 'minutes': 60},
                    ],
                },
            }
            
            if meeting_data.get('attendees'):
                event['attendees'] = [{'email': email} for email in meeting_data['attendees']]
            
            event = service.events().insert(calendarId='primary', body=event).execute()
            
            return {
                'success': True,
                'event_id': event.get('id'),
                'link': event.get('htmlLink')}