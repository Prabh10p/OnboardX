import streamlit as st
from datetime import datetime, timedelta
import json

def render_team_directory(user, services):
    """Team Directory with meeting scheduling"""
    st.title("👥 Team Directory")
    
    # Mock team data - in production, fetch from database
    team_members = [
        {
            "id": "tm1",
            "name": "Sarah Johnson",
            "role": "Engineering Manager",
            "department": "Engineering",
            "email": "sarah.j@company.com",
            "timezone": "PST",
            "bio": "10+ years in software development. Happy to help with technical onboarding!",
            "expertise": ["Python", "System Design", "Team Leadership"],
            "availability": "Mon-Fri 9AM-5PM PST"
        },
        {
            "id": "tm2",
            "name": "Michael Chen",
            "role": "Senior Product Designer",
            "department": "Design",
            "email": "michael.c@company.com",
            "timezone": "EST",
            "bio": "Design thinking enthusiast. Let's chat about product and UX!",
            "expertise": ["Figma", "User Research", "Prototyping"],
            "availability": "Mon-Fri 10AM-6PM EST"
        },
        {
            "id": "tm3",
            "name": "Emma Williams",
            "role": "HR Business Partner",
            "department": "People Ops",
            "email": "emma.w@company.com",
            "timezone": "CST",
            "bio": "Here to support your onboarding journey. Ask me anything about company culture!",
            "expertise": ["Benefits", "Culture", "Career Development"],
            "availability": "Mon-Fri 8AM-4PM CST"
        },
        {
            "id": "tm4",
            "name": "David Park",
            "role": "Sales Director",
            "department": "Sales",
            "email": "david.p@company.com",
            "timezone": "PST",
            "bio": "Love connecting with new team members. Let's talk strategy!",
            "expertise": ["Customer Relations", "B2B Sales", "Negotiation"],
            "availability": "Mon-Fri 9AM-6PM PST"
        }
    ]
    
    # Search and filter
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search team members", placeholder="Search by name, role, or department")
    with col2:
        dept_filter = st.selectbox("Filter by Department", ["All", "Engineering", "Design", "People Ops", "Sales"])
    
    # Filter team members
    filtered_members = team_members
    if search:
        filtered_members = [m for m in filtered_members if search.lower() in m['name'].lower() 
                           or search.lower() in m['role'].lower() 
                           or search.lower() in m['department'].lower()]
    if dept_filter != "All":
        filtered_members = [m for m in filtered_members if m['department'] == dept_filter]
    
    st.markdown("---")
    
    # Display team members
    for member in filtered_members:
        with st.expander(f"**{member['name']}** - {member['role']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Department:** {member['department']}")
                st.markdown(f"**Email:** {member['email']}")
                st.markdown(f"**Timezone:** {member['timezone']}")
                st.markdown(f"**Availability:** {member['availability']}")
                st.markdown(f"**Bio:** {member['bio']}")
                
                st.markdown("**Expertise:**")
                st.markdown(" • " + " • ".join(member['expertise']))
            
            with col2:
                if st.button(f"📅 Schedule Meeting", key=f"schedule_{member['id']}"):
                    st.session_state.scheduling_member = member
                    st.session_state.show_scheduler = True
                    st.rerun()
                
                if st.button(f"✉️ Send Message", key=f"message_{member['id']}"):
                    st.info(f"Message feature coming soon! For now, email {member['email']}")
    
    # Meeting Scheduler Modal
    if st.session_state.get('show_scheduler', False):
        st.markdown("---")
        member = st.session_state.scheduling_member
        
        st.subheader(f"📅 Schedule Meeting with {member['name']}")
        
        with st.form("schedule_meeting"):
            meeting_title = st.text_input("Meeting Title", value=f"1:1 with {member['name']}")
            
            col1, col2 = st.columns(2)
            with col1:
                meeting_date = st.date_input("Date", min_value=datetime.now().date())
            with col2:
                meeting_time = st.time_input("Time")
            
            duration = st.selectbox("Duration", ["15 min", "30 min", "45 min", "60 min"], index=1)
            
            meeting_type = st.radio("Meeting Type", ["Virtual (Zoom)", "In-Person", "Phone Call"])
            
            agenda = st.text_area("Meeting Agenda (Optional)", 
                                 placeholder="What would you like to discuss?")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                submit = st.form_submit_button("📨 Send Meeting Request", use_container_width=True)
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.show_scheduler = False
                    st.rerun()
            
            if submit:
                # Save meeting to user's calendar
                meeting_data = {
                    "id": f"meeting_{datetime.now().timestamp()}",
                    "title": meeting_title,
                    "with": member['name'],
                    "date": meeting_date.isoformat(),
                    "time": meeting_time.isoformat(),
                    "duration": duration,
                    "type": meeting_type,
                    "agenda": agenda,
                    "status": "pending"
                }
                
                # Store in session state (in production, save to database)
                if 'meetings' not in st.session_state:
                    st.session_state.meetings = []
                st.session_state.meetings.append(meeting_data)
                
                # Send email notification
                try:
                    services['email'].send_meeting_request(
                        to_email=member['email'],
                        from_name=user['name'],
                        meeting_data=meeting_data
                    )
                except:
                    pass  # Email service might not be configured
                
                st.success(f"✅ Meeting request sent to {member['name']}!")
                st.balloons()
                st.session_state.show_scheduler = False
                st.rerun()