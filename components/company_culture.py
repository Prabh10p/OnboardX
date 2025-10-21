import streamlit as st

def render_company_culture(user, services):
    """Company culture, values, and social activities"""
    st.title("🌟 Company Culture & Community")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Our Values", "🎉 Events & Activities", "🏆 Recognition", "💡 Resources"])
    
    with tab1:
        render_company_values()
    
    with tab2:
        render_events_activities()
    
    with tab3:
        render_recognition(user)
    
    with tab4:
        render_culture_resources()

def render_company_values():
    """Display company values and mission"""
    st.header("Our Core Values")
    
    values = [
        {
            "icon": "🤝",
            "title": "Collaboration Over Competition",
            "description": "We believe in the power of teamwork. Success is shared, and we lift each other up.",
            "behaviors": [
                "Share knowledge openly",
                "Ask for help when needed",
                "Celebrate team wins",
                "Cross-functional partnerships"
            ]
        },
        {
            "icon": "🚀",
            "title": "Innovation & Bold Ideas",
            "description": "We encourage creative thinking and aren't afraid to challenge the status quo.",
            "behaviors": [
                "Experiment and learn from failures",
                "Question assumptions",
                "Prototype quickly",
                "Think long-term"
            ]
        },
        {
            "icon": "💪",
            "title": "Ownership & Accountability",
            "description": "We take responsibility for our work and follow through on commitments.",
            "behaviors": [
                "Deliver on promises",
                "Be proactive",
                "Learn from mistakes",
                "Drive projects forward"
            ]
        },
        {
            "icon": "🌱",
            "title": "Continuous Growth",
            "description": "We're committed to personal and professional development for everyone.",
            "behaviors": [
                "Seek feedback actively",
                "Mentor others",
                "Learn new skills",
                "Embrace challenges"
            ]
        },
        {
            "icon": "❤️",
            "title": "Customer Obsession",
            "description": "Our customers are at the heart of everything we do.",
            "behaviors": [
                "Listen deeply",
                "Solve real problems",
                "Go the extra mile",
                "Think from their perspective"
            ]
        }
    ]
    
    for value in values:
        with st.expander(f"{value['icon']} {value['title']}", expanded=True):
            st.write(value['description'])
            st.markdown("**How we live this value:**")
            for behavior in value['behaviors']:
                st.markdown(f"• {behavior}")

def render_events_activities():
    """Display upcoming events and social activities"""
    st.header("Upcoming Events & Activities")
    
    # Upcoming events
    events = [
        {
            "title": "🍕 Team Lunch - Engineering",
            "date": "Friday, Oct 25",
            "time": "12:00 PM - 1:00 PM",
            "location": "Conference Room B",
            "description": "Monthly team lunch to connect and celebrate wins!",
            "spots": "10 spots left"
        },
        {
            "title": "🎓 Learning Hour: Python Best Practices",
            "date": "Next Monday",
            "time": "3:00 PM - 4:00 PM",
            "location": "Virtual (Zoom)",
            "description": "Weekly learning session hosted by Sarah Johnson",
            "spots": "Open to all"
        },
        {
            "title": "🏃 Company 5K Fun Run",
            "date": "Nov 2",
            "time": "9:00 AM",
            "location": "City Park",
            "description": "Annual charity run. All fitness levels welcome!",
            "spots": "Register now"
        },
        {
            "title": "🎮 Game Night",
            "date": "Nov 8",
            "time": "6:00 PM - 9:00 PM",
            "location": "Office Game Room",
            "description": "Board games, video games, snacks, and fun!",
            "spots": "15 spots left"
        }
    ]
    
    for event in events:
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {event['title']}")
                st.write(f"📅 {event['date']} • ⏰ {event['time']}")
                st.write(f"📍 {event['location']}")
                st.write(event['description'])
            
            with col2:
                st.info(event['spots'])
                if st.button("RSVP", key=f"rsvp_{event['title']}"):
                    st.success("✅ You're registered!")
            
            st.markdown("---")
    
    # Interest groups
    st.subheader("🌈 Interest Groups & Clubs")
    
    col1, col2, col3 = st.columns(3)
    
    groups = [
        {"name": "📚 Book Club", "members": 23},
        {"name": "🎸 Music Jam", "members": 15},
        {"name": "🧘 Wellness Warriors", "members": 31},
        {"name": "🎨 Creative Arts", "members": 18},
        {"name": "🌍 Sustainability Team", "members": 27},
        {"name": "⚽ Sports League", "members": 42}
    ]
    
    for i, group in enumerate(groups):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"**{group['name']}**")
            st.caption(f"{group['members']} members")
            if st.button("Join", key=f"join_{i}"):
                st.success(f"Joined {group['name']}!")

def render_recognition(user):
    """Employee recognition and kudos"""
    st.header("🏆 Recognition Wall")
    
    st.markdown("""
    Celebrate your colleagues! Send kudos to recognize great work, helpfulness, or just being awesome.
    """)
    
    # Send kudos form
    with st.expander("✨ Send Kudos"):
        with st.form("send_kudos"):
            recipient = st.text_input("To (Name or Email)")
            kudos_type = st.selectbox("Recognition Type", 
                                     ["Great Work 💪", "Team Player 🤝", "Innovation 💡", 
                                      "Helpful 🙏", "Leadership 🌟", "Other 🎉"])
            message = st.text_area("Your Message", 
                                  placeholder="What do you want to recognize?")
            
            if st.form_submit_button("🚀 Send Kudos"):
                if recipient and message:
                    st.success(f"✅ Kudos sent to {recipient}!")
                    st.balloons()
                else:
                    st.error("Please fill in all fields")
    
    st.markdown("---")
    
    # Recent kudos
    st.subheader("Recent Kudos 🎉")
    
    kudos_list = [
        {
            "from": "Michael Chen",
            "to": "Emma Williams",
            "type": "Helpful 🙏",
            "message": "Emma went above and beyond helping me navigate the benefits system. So grateful!",
            "time": "2 hours ago",
            "likes": 15
        },
        {
            "from": "Sarah Johnson",
            "to": "New Team",
            "type": "Team Player 🤝",
            "message": "Shoutout to everyone who helped make this week's product launch a success. Amazing teamwork!",
            "time": "Yesterday",
            "likes": 28
        },
        {
            "from": "David Park",
            "to": "Michael Chen",
            "type": "Innovation 💡",
            "message": "Michael's new design system is a game-changer. Love the attention to detail!",
            "time": "2 days ago",
            "likes": 22
        }
    ]
    
    for kudos in kudos_list:
        with st.container():
            st.markdown(f"**{kudos['from']}** → **{kudos['to']}** • {kudos['type']}")
            st.write(f"_{kudos['message']}_")
            col1, col2 = st.columns([1, 5])
            with col1:
                st.caption(f"❤️ {kudos['likes']}")
            with col2:
                st.caption(f"🕒 {kudos['time']}")
            st.markdown("---")

def render_culture_resources():
    """Company culture resources and guides"""
    st.header("📚 Culture Resources")
    
    resources = [
        {
            "title": "📖 Employee Handbook",
            "description": "Everything you need to know about policies, benefits, and expectations",
            "link": "#"
        },
        {
            "title": "🎯 Company Mission & Vision",
            "description": "Learn about where we're going and how we plan to get there",
            "link": "#"
        },
        {
            "title": "💬 Communication Guidelines",
            "description": "Best practices for Slack, email, meetings, and collaboration",
            "link": "#"
        },
        {
            "title": "🌍 Remote Work Guide",
            "description": "Tips and tools for being effective in a hybrid environment",
            "link": "#"
        },
        {
            "title": "🎓 Learning & Development",
            "description": "Professional development opportunities and training catalog",
            "link": "#"
        },
        {
            "title": "🏥 Wellness Programs",
            "description": "Mental health resources, fitness benefits, and work-life balance",
            "link": "#"
        }
    ]
    
    for resource in resources:
        with st.expander(resource['title']):
            st.write(resource['description'])
            st.markdown(f"[📥 Access Resource]({resource['link']})")
    
    st.markdown("---")
    
    # Culture tips
    st.subheader("💡 Quick Culture Tips for New Hires")
    
    tips = [
        "Don't be afraid to ask questions - everyone is here to help!",
        "Join social channels on Slack to connect with colleagues",
        "Attend company all-hands meetings (usually monthly)",
        "Take advantage of coffee chat programs to meet people",
        "Share your wins in team meetings - we celebrate progress",
        "Work-life balance is important - use your PTO!",
        "Feedback is a gift - both giving and receiving",
        "Be yourself - we value diversity of thought and experience"
    ]
    
    for tip in tips:
        st.markdown(f"✓ {tip}")