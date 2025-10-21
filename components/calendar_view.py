import streamlit as st
from datetime import datetime, timedelta
import calendar as cal

def render_calendar(user, services):
    """Calendar view with meetings and onboarding events"""
    st.title("📅 My Calendar")
    
    # Calendar controls
    col1, col2, col3 = st.columns([1, 2, 1])
    
    # Initialize current month/year
    if 'calendar_date' not in st.session_state:
        st.session_state.calendar_date = datetime.now()
    
    current_date = st.session_state.calendar_date
    
    with col1:
        if st.button("◀ Previous"):
            if current_date.month == 1:
                st.session_state.calendar_date = current_date.replace(year=current_date.year-1, month=12)
            else:
                st.session_state.calendar_date = current_date.replace(month=current_date.month-1)
            st.rerun()
    
    with col2:
        st.markdown(f"### {current_date.strftime('%B %Y')}")
    
    with col3:
        if st.button("Next ▶"):
            if current_date.month == 12:
                st.session_state.calendar_date = current_date.replace(year=current_date.year+1, month=1)
            else:
                st.session_state.calendar_date = current_date.replace(month=current_date.month+1)
            st.rerun()
    
    # Get all events for the month
    meetings = st.session_state.get('meetings', [])
    onboarding_events = get_onboarding_events(user)
    
    # Display calendar
    st.markdown("---")
    
    # Weekday headers
    cols = st.columns(7)
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    for i, day in enumerate(weekdays):
        cols[i].markdown(f"**{day}**")
    
    # Get calendar data
    month_cal = cal.monthcalendar(current_date.year, current_date.month)
    
    for week in month_cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")
            else:
                date_obj = datetime(current_date.year, current_date.month, day)
                day_events = get_events_for_day(date_obj, meetings, onboarding_events)
                
                # Highlight today
                is_today = date_obj.date() == datetime.now().date()
                
                with cols[i]:
                    if is_today:
                        st.markdown(f"**🔵 {day}**")
                    else:
                        st.write(f"{day}")
                    
                    if day_events:
                        for event in day_events[:2]:  # Show max 2 events
                            emoji = "📅" if event['type'] == 'meeting' else "🎯"
                            st.caption(f"{emoji} {event['title'][:15]}...")
                        if len(day_events) > 2:
                            st.caption(f"+{len(day_events)-2} more")
    
    # Upcoming events list
    st.markdown("---")
    st.subheader("📋 Upcoming Events")
    
    tab1, tab2, tab3 = st.tabs(["All Events", "Meetings", "Onboarding Tasks"])
    
    with tab1:
        all_events = sorted(meetings + onboarding_events, 
                           key=lambda x: datetime.fromisoformat(x['date']))
        display_event_list(all_events)
    
    with tab2:
        display_event_list(sorted(meetings, key=lambda x: datetime.fromisoformat(x['date'])))
    
    with tab3:
        display_event_list(sorted(onboarding_events, key=lambda x: datetime.fromisoformat(x['date'])))
    
    # Quick add event
    st.markdown("---")
    with st.expander("➕ Add Quick Event"):
        with st.form("quick_event"):
            event_title = st.text_input("Event Title")
            col1, col2 = st.columns(2)
            with col1:
                event_date = st.date_input("Date")
            with col2:
                event_time = st.time_input("Time")
            
            if st.form_submit_button("Add Event"):
                event = {
                    "id": f"event_{datetime.now().timestamp()}",
                    "title": event_title,
                    "date": event_date.isoformat(),
                    "time": event_time.isoformat(),
                    "type": "personal",
                    "status": "scheduled"
                }
                if 'meetings' not in st.session_state:
                    st.session_state.meetings = []
                st.session_state.meetings.append(event)
                st.success("Event added!")
                st.rerun()

def get_onboarding_events(user):
    """Generate onboarding milestone events"""
    join_date = datetime.fromisoformat(user.get('join_date_full', datetime.now().isoformat()))
    
    events = [
        {
            "id": "ob1",
            "title": "First Day - Welcome Session",
            "date": join_date.isoformat(),
            "time": "09:00:00",
            "type": "onboarding",
            "status": "completed"
        },
        {
            "id": "ob2",
            "title": "Week 1 Check-in with Manager",
            "date": (join_date + timedelta(days=7)).isoformat(),
            "time": "14:00:00",
            "type": "onboarding",
            "status": "pending"
        },
        {
            "id": "ob3",
            "title": "30-Day Review",
            "date": (join_date + timedelta(days=30)).isoformat(),
            "time": "10:00:00",
            "type": "onboarding",
            "status": "pending"
        },
        {
            "id": "ob4",
            "title": "90-Day Performance Review",
            "date": (join_date + timedelta(days=90)).isoformat(),
            "time": "10:00:00",
            "type": "onboarding",
            "status": "pending"
        }
    ]
    
    return [e for e in events if datetime.fromisoformat(e['date']).date() >= datetime.now().date() - timedelta(days=30)]

def get_events_for_day(date_obj, meetings, onboarding_events):
    """Get all events for a specific day"""
    all_events = meetings + onboarding_events
    return [e for e in all_events if datetime.fromisoformat(e['date']).date() == date_obj.date()]

def display_event_list(events):
    """Display list of events"""
    if not events:
        st.info("No events scheduled")
        return
    
    for event in events[:10]:  # Show up to 10 events
        event_date = datetime.fromisoformat(event['date'])
        event_time = event.get('time', '00:00:00')
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            emoji = "📅" if event['type'] == 'meeting' else "🎯"
            st.markdown(f"{emoji} **{event['title']}**")
            if 'with' in event:
                st.caption(f"with {event['with']}")
        
        with col2:
            st.write(event_date.strftime('%B %d, %Y'))
            st.caption(event_time[:5])
        
        with col3:
            status = event.get('status', 'scheduled')
            if status == 'completed':
                st.success("✅ Done")
            elif status == 'pending':
                st.warning("⏳ Pending")
            else:
                st.info("📌 Scheduled")