import streamlit as st
import json
import os
from datetime import datetime, timedelta
from utils.auth import AuthManager
from utils.email_service import EmailService
from utils.llm_service import LLMService
from components.signup import render_signup
from components.login import render_login
from components.dashboard import render_dashboard
from components.checklist import render_checklist
from components.resources import render_resources
from components.mentor_buddy import render_mentor_buddy
from components.feedback import render_feedback
from components.team_directory import render_team_directory
from components.calendar_view import render_calendar
from components.goals_tracking import render_goals_tracking
from components.notifications import render_notifications
from components.company_culture import render_company_culture
from dotenv import load_dotenv

load_dotenv()

# ===========================
# 🎨 Page Configuration
# ===========================
st.set_page_config(
    page_title="OnboardX - Smart Onboarding Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================
# 🎯 Initialize Services
# ===========================
@st.cache_resource
def init_services():
    return {
        'auth': AuthManager(),
        'email': EmailService(),
        'llm': LLMService()
    }

services = init_services()

# ===========================
# 🔧 Session State Initialization
# ===========================
if "signup_step" not in st.session_state:
    st.session_state.signup_step = 0
    st.session_state.signup_data = {}
    
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Initialize notifications and goals BEFORE any rendering
if "notifications" not in st.session_state:
    st.session_state.notifications = []

if "goals" not in st.session_state:
    st.session_state.goals = []

if "meetings" not in st.session_state:
    st.session_state.meetings = []

# Initialize user join date for calendar/goals
if "user" in st.session_state and "join_date_full" not in st.session_state.user:
    st.session_state.user["join_date_full"] = datetime.now().isoformat()

# ===========================
# 🏠 Landing Page
# ===========================
if "user" not in st.session_state:
    st.markdown("""
    <style>
    .hero-title {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="hero-title">🚀 OnboardX</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Transform Your Employee Onboarding Experience</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📋 Organized Process")
        st.write("Clear checklists, schedules, and assigned mentors from day one")
    
    with col2:
        st.markdown("### 🤝 Human Connection")
        st.write("Built-in buddy system and team introductions")
    
    with col3:
        st.markdown("### 🎯 Clear Goals")
        st.write("Defined success metrics and expectations")
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🆕 Sign Up", "🔑 Log In"])
    
    with tab1:
        render_signup(services)
    
    with tab2:
        render_login(services)

# ===========================
# 📊 Main Dashboard (Logged In)
# ===========================
else:
    user = st.session_state.user
    
    # Notification badge count with safety checks
    notifications = st.session_state.get('notifications', [])
    
    # Ensure notifications is a list
    if not isinstance(notifications, list):
        notifications = []
    
    # Count unread notifications (only valid dict items)
    unread_count = len([
        n for n in notifications 
        if isinstance(n, dict) and not n.get('read', False)
    ])
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"### 👋 Welcome, {user['name']}!")
        st.markdown(f"**Plan:** {user['plan']}")
        st.markdown(f"**Join Date:** {user.get('join_date', 'Today')}")
        
        st.markdown("---")
        st.markdown("### 🧭 Navigation")
        
        pages = {
            "🏠 Dashboard": "dashboard",
            "✅ Onboarding Checklist": "checklist",
            "🎯 Goals & Milestones": "goals_page",
            "📅 My Calendar": "calendar",
            "👥 Team Directory": "team_directory",
            "📚 Resources & Training": "resources",
            "🤝 Mentor & Buddy": "mentor_buddy",
            f"🔔 Notifications ({unread_count})": "notifications_page",
            "🌟 Company Culture": "culture",
            "💬 Feedback": "feedback",
            "⚙️ Settings": "settings"
        }
        
        for label, page_id in pages.items():
            if st.button(label, key=f"nav_{page_id}", use_container_width=True):
                st.session_state.current_page = page_id
        
        st.markdown("---")
        if st.button("🔓 Log Out", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    # Main Content Area
    current_page = st.session_state.current_page
    
    if current_page == "dashboard":
        render_dashboard(user, services)
    elif current_page == "checklist":
        render_checklist(user, services)
    elif current_page == "goals":
        render_goals_tracking(user, services)
    elif current_page == "calendar":
        render_calendar(user, services)
    elif current_page == "team_directory":
        render_team_directory(user, services)
    elif current_page == "resources":
        render_resources(user, services)
    elif current_page == "mentor_buddy":
        render_mentor_buddy(user, services)
    elif current_page == "notifications":
        render_notifications(user, services)
    elif current_page == "culture":
        render_company_culture(user, services)
    elif current_page == "feedback":
        render_feedback(user, services)
    elif current_page == "settings":
        st.title("⚙️ Settings")
        st.info("Settings page - Update your profile, preferences, and notifications")
        
        tab1, tab2, tab3 = st.tabs(["👤 Profile", "🔔 Notifications", "🎨 Preferences"])
        
        with tab1:
            with st.form("profile_update"):
                st.subheader("Update Profile")
                new_name = st.text_input("Name", value=user['name'])
                new_email = st.text_input("Email", value=user['email'], disabled=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    department = st.text_input("Department", value=user.get('department', ''))
                with col2:
                    role = st.text_input("Role", value=user.get('role', ''))
                
                bio = st.text_area("Bio", value=user.get('bio', ''), 
                                  placeholder="Tell us about yourself...")
                
                if st.form_submit_button("💾 Save Changes"):
                    user['name'] = new_name
                    user['department'] = department
                    user['role'] = role
                    user['bio'] = bio
                    services['auth'].update_user(user['email'], user)
                    st.success("Profile updated successfully!")
                    st.rerun()
        
        with tab2:
            st.subheader("Notification Preferences")
            
            email_notifs = st.checkbox("📧 Email Notifications", value=True)
            meeting_reminders = st.checkbox("📅 Meeting Reminders", value=True)
            task_reminders = st.checkbox("✅ Task Due Date Reminders", value=True)
            weekly_digest = st.checkbox("📊 Weekly Progress Digest", value=True)
            
            if st.button("Save Notification Settings"):
                st.success("Notification preferences saved!")
        
        with tab3:
            st.subheader("Display Preferences")
            
            theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
            language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
            timezone = st.selectbox("Timezone", ["PST", "EST", "CST", "MST", "UTC"])
            
            if st.button("Save Preferences"):
                st.success("Preferences saved!")