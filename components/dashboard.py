import streamlit as st
from datetime import datetime, timedelta

def render_dashboard(user, services):
    """Render personalized dashboard"""
    st.title(f"👋 Welcome, {user['name']}!")
    
    # Welcome message
    st.markdown(f"""
    We're excited to have you on the team! You joined us on **{user['join_date']}**.
    Let's make your onboarding smooth and engaging.
    """)
    
    # Progress Overview
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    progress = user.get('onboarding_progress', 0)
    checklist_completed = len(user.get('checklist_completed', []))
    
    with col1:
        st.metric(
            label="📊 Overall Progress",
            value=f"{progress}%",
            delta=f"{progress - 0}% from start"
        )
    
    with col2:
        st.metric(
            label="✅ Tasks Completed",
            value=checklist_completed,
            delta=f"{checklist_completed} items"
        )
    
    with col3:
        mentor_status = "✓ Assigned" if user.get('mentor_assigned') else "⏳ Pending"
        st.metric(
            label="👥 Mentor Status",
            value=mentor_status
        )
    
    with col4:
        days_since_join = (datetime.now() - datetime.strptime(user['join_date'], "%Y-%m-%d")).days
        st.metric(
            label="📅 Days Active",
            value=days_since_join
        )
    
    # Progress Bar
    st.progress(progress / 100, text=f"Onboarding Progress: {progress}%")
    
    # Quick Actions
    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ View Checklist", use_container_width=True):
            st.session_state.current_page = "checklist"
            st.rerun()
    
    with col2:
        if st.button("📚 Browse Resources", use_container_width=True):
            st.session_state.current_page = "resources"
            st.rerun()
    
    with col3:
        if st.button("👥 Meet Your Team", use_container_width=True):
            st.session_state.current_page = "mentor_buddy"
            st.rerun()
    
    # Upcoming Tasks & Reminders
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Upcoming Tasks")
        
        tasks = [
            {"task": "Complete IT security training", "due": "Today", "priority": "High"},
            {"task": "Schedule 1:1 with manager", "due": "Tomorrow", "priority": "Medium"},
            {"task": "Review company handbook", "due": "In 3 days", "priority": "Medium"},
            {"task": "Set up development environment", "due": "This week", "priority": "High"},
        ]
        
        for task in tasks:
            priority_color = "red" if task['priority'] == "High" else "orange"
            st.markdown(f"""
            <div style="padding: 10px; border-left: 3px solid {priority_color}; margin-bottom: 10px; background: #f8f9fa;">
                <strong>{task['task']}</strong><br>
                <small>Due: {task['due']} | Priority: {task['priority']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("🎯 This Week's Goals")
        
        st.markdown("""
        - ✅ Complete profile setup
        - ⏳ Attend orientation session
        - ⏳ Meet your team members
        - ⏳ Review first project
        """)
        
        st.markdown("---")
        st.info("💡 **Tip of the Day**\n\nDon't hesitate to ask questions! Your mentor and buddy are here to help.")
    
    # Recent Activity
    st.markdown("---")
    st.subheader("📊 Recent Activity")
    
    activities = [
        {"icon": "✅", "text": "Completed 'Welcome Video'", "time": "2 hours ago"},
        {"icon": "📧", "text": "Welcome email sent", "time": "1 day ago"},
        {"icon": "👤", "text": "Account created", "time": f"{days_since_join} days ago"},
    ]
    
    for activity in activities:
        st.markdown(f"{activity['icon']} {activity['text']} • *{activity['time']}*")
    
    # AI Assistant
    st.markdown("---")
    st.subheader("🤖 Need Help? Ask Our AI Assistant")
    
    with st.form("ai_question_form"):
        question = st.text_input(
            "Ask a question about your onboarding...",
            placeholder="e.g., How do I access my benefits information?"
        )
        
        if st.form_submit_button("Ask"):
            if question:
                with st.spinner("Thinking..."):
                    context = {
                        "name": user['name'],
                        "role": user.get('role', ''),
                        "department": user.get('department', ''),
                        "plan": user['plan'],
                        "days_active": days_since_join
                    }
                    answer = services['llm'].answer_onboarding_question(question, context)
                    st.info(f"🤖 **Answer:** {answer}")