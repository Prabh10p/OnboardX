import streamlit as st
from datetime import datetime, timedelta

def render_notifications(user, services):
    """Notification center"""
    st.title("🔔 Notifications")
    
    # Initialize notifications
    if 'notifications' not in st.session_state:
        st.session_state.notifications = get_default_notifications(user)
    
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
        st.info("No notifications available.")
        return
    
    for notif in notifications:
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
    today = datetime.now().strftime("%b %d, %Y %I:%M %p")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%b %d, %Y %I:%M %p")
    
    return [
        {
            "id": "n1",
            "type": "welcome",
            "title": f"Welcome to OnboardX, {user['name']}!",
            "message": "We're excited to have you here. Check your onboarding checklist to get started.",
            "timestamp": today,
            "read": False
        },
        {
            "id": "n2",
            "type": "meeting",
            "title": "Orientation Meeting Scheduled",
            "message": "Your onboarding orientation is tomorrow at 10:00 AM with HR.",
            "timestamp": tomorrow,
            "read": False
        },
        {
            "id": "n3",
            "type": "task",
            "title": "Complete Your Profile Setup",
            "message": "Add your department and role in the Settings page to personalize your dashboard.",
            "timestamp": today,
            "read": False
        },
        {
            "id": "n4",
            "type": "achievement",
            "title": "First Task Completed 🎉",
            "message": "You’ve completed your first onboarding step — great job!",
            "timestamp": today,
            "read": True
        }
    ]
