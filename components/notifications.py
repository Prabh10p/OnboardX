import streamlit as st
from datetime import datetime, timedelta

def render_notifications(user, services):
    """Notification center"""
    st.title("🔔 Notifications")
    
    # Initialize notifications - check if empty and populate
    if not isinstance(st.session_state.notifications, list):
        st.session_state.notifications = []
    
    if len(st.session_state.notifications) == 0:
        # Populate with default notifications
        default_notifs = get_default_notifications(user)
        st.session_state.notifications.extend(default_notifs)
    
    notifications = st.session_state.notifications
    
    unread = len([n for n in notifications if not n['read']])
    
    # Header with stats
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"You have {unread} unread notification{'s' if unread != 1 else ''}")
    with col2:
        if st.button("✅ Mark all as read"):
            for n in notifications:
                n['read'] = True
            st.rerun()
    
    st.markdown("---")
    
    # Tabs for different notification types
    tab1, tab2, tab3, tab4 = st.tabs(["📬 All", "🆕 Unread", "👥 Meetings", "🎯 Tasks"])
    
    with tab1:
        display_notifications(notifications, filter_type=None)
    
    with tab2:
        unread_notifs = [n for n in notifications if not n['read']]
        display_notifications(unread_notifs, filter_type=None)
    
    with tab3:
        meeting_notifs = [n for n in notifications if n['type'] == 'meeting']
        display_notifications(meeting_notifs, filter_type='meeting')
    
    with tab4:
        task_notifs = [n for n in notifications if n['type'] == 'task']
        display_notifications(task_notifs, filter_type='task')

def display_notifications(notifications, filter_type=None):
    """Display list of notifications"""
    if not notifications:
        st.info("No notifications")
        return
    
    for notif in notifications:
        # Notification card
        bg_color = "#f0f2f6" if notif['read'] else "#e3f2fd"
        
        with st.container():
            col1, col2, col3 = st.columns([0.5, 4, 1])
            
            with col1:
                icon = get_notification_icon(notif['type'])
                st.markdown(f"### {icon}")
            
            with col2:
                if not notif['read']:
                    st.markdown(f"**{notif['title']}** 🔵")
                else:
                    st.markdown(f"{notif['title']}")
                
                st.caption(notif['message'])
                st.caption(f"🕒 {notif['timestamp']}")
            
            with col3:
                if not notif['read']:
                    if st.button("✓ Read", key=f"read_{notif['id']}"):
                        notif['read'] = True
                        st.rerun()
                
                if st.button("🗑️", key=f"delete_{notif['id']}"):
                    st.session_state.notifications.remove(notif)
                    st.rerun()
            
            st.markdown("---")

def get_notification_icon(notif_type):
    """Get icon for notification type"""
    icons = {
        "meeting": "📅",
        "task": "✅",
        "message": "💬",
        "system": "⚙️",
        "welcome": "👋",
        "reminder": "⏰",
        "achievement": "🏆"
    }
    return icons.get(notif_type, "🔔")

def get_default_notifications(user):
    """Generate default notifications"""
    return [
        {
            "id": "n1",
            "type": "welcome",
            "title": "Welcome to OnboardX!",
            "message": "We're excited to have you here. Check out your personalized onboarding checklist to get started.",
            "timestamp": "Today",
            "read": False
        },
        {
            "id": "n2",
            "type": "meeting",
            "title": "Upcoming: 1:1 with Manager",
            "message": "Your weekly check-in is scheduled for tomorrow at 2:00 PM",
            "timestamp": "2 hours ago",
            "read": False
        },
        {
            "id": "n3",
            "type": "task",
            "title": "Action Required: Complete Benefits Enrollment",
            "message": "Please complete your benefits enrollment by Friday. Due in 3 days.",
            "timestamp": "5 hours ago",
            "read": False
        },
        {
            "id": "n4",
            "type": "message",
            "title": "Message from Sarah Johnson",
            "message": "Hey! Welcome to the team. Let's grab coffee this week!",
            "timestamp": "Yesterday",
            "read": True
        },
        {
            "id": "n5",
            "type": "reminder",
            "title": "Reminder: Training Module Due Soon",
            "message": "Complete 'Security & Compliance Training' by end of week",
            "timestamp": "Yesterday",
            "read": True
        },
        {
            "id": "n6",
            "type": "achievement",
            "title": "Achievement Unlocked! 🎉",
            "message": "You've completed your first week! Keep up the great work.",
            "timestamp": "2 days ago",
            "read": False
        }
    ]

def add_notification(notif_type, title, message):
    """Add a new notification"""
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    
    new_notif = {
        "id": f"n_{datetime.now().timestamp()}",
        "type": notif_type,
        "title": title,
        "message": message,
        "timestamp": "Just now",
        "read": False
    }
    
    st.session_state.notifications.insert(0, new_notif)