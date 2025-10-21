import streamlit as st
from datetime import datetime, timedelta

def render_mentor_buddy(user, services):
    """Render mentor and buddy system interface"""
    st.title("👥 Mentor & Buddy System")
    
    st.markdown("""
    Connect with experienced team members who will guide you through your onboarding journey.
    Your mentor provides professional guidance, while your buddy helps with day-to-day questions.
    """)
    
    # Check plan access
    has_mentor = user['plan'] in ["Pro", "Enterprise"]
    has_buddy = user['plan'] == "Enterprise"
    
    if not has_mentor and not has_buddy:
        st.warning("⚠️ Mentor and Buddy features are available in Pro and Enterprise plans.")
        st.info("Upgrade your plan to get personalized mentorship and peer support!")
        return
    
    st.markdown("---")
    
    # Tabs for Mentor and Buddy
    tabs = []
    if has_mentor:
        tabs.append("🎓 Your Mentor")
    if has_buddy:
        tabs.append("🤝 Your Buddy")
    tabs.extend(["📅 Schedule Meeting", "💬 Messages"])
    
    tab_objects = st.tabs(tabs)
    current_tab = 0
    
    # Mentor Tab
    if has_mentor:
        with tab_objects[current_tab]:
            st.subheader("🎓 Your Mentor")
            
            mentor_assigned = user.get('mentor_assigned', False)
            
            if not mentor_assigned:
                st.info("🔍 We're matching you with the perfect mentor...")
                
                if st.button("🎯 Find My Mentor"):
                    with st.spinner("Analyzing your profile and finding the best match..."):
                        # Simulated mentor matching logic
                        import time
                        time.sleep(2)  # simulate processing time
                        
                        user['mentor_assigned'] = True
                        user['mentor_name'] = "Alex Johnson"
                        user['mentor_role'] = "Senior Software Engineer"
                    
                    st.success(f"✅ Mentor assigned: **{user['mentor_name']}**, {user['mentor_role']}")
            else:
                st.success(f"🎉 Your mentor is **{user['mentor_name']}**, {user['mentor_role']}")
