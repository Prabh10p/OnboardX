import streamlit as st
import json
import os

def load_checklist_template(plan):
    """Load checklist based on plan"""
    basic_tasks = [
        {"id": "welcome_video", "title": "Watch Welcome Video", "description": "Introduction to company culture and values", "category": "Orientation", "duration": "15 min"},
        {"id": "profile_setup", "title": "Complete Profile Setup", "description": "Add your photo, bio, and contact info", "category": "Account", "duration": "10 min"},
        {"id": "it_access", "title": "Set Up IT Access", "description": "Configure email, Slack, and essential tools", "category": "IT", "duration": "30 min"},
        {"id": "security_training", "title": "Complete Security Training", "description": "Learn about data protection and security policies", "category": "Compliance", "duration": "45 min"},
        {"id": "handbook_review", "title": "Review Employee Handbook", "description": "Understand company policies and procedures", "category": "HR", "duration": "1 hour"},
        {"id": "team_intro", "title": "Team Introduction Meeting", "description": "Meet your immediate team members", "category": "Team", "duration": "30 min"},
        {"id": "workspace_setup", "title": "Set Up Workspace", "description": "Arrange your desk and equipment", "category": "Facilities", "duration": "20 min"},
    ]
    
    pro_tasks = basic_tasks + [
        {"id": "mentor_meeting", "title": "First Meeting with Mentor", "description": "Discuss goals and expectations", "category": "Mentorship", "duration": "1 hour"},
        {"id": "goal_setting", "title": "Set 30-60-90 Day Goals", "description": "Define your short-term objectives", "category": "Goals", "duration": "45 min"},
        {"id": "department_overview", "title": "Department Overview Session", "description": "Learn about department structure and processes", "category": "Orientation", "duration": "1 hour"},
        {"id": "tools_training", "title": "Role-Specific Tools Training", "description": "Get trained on the tools you'll use daily", "category": "Training", "duration": "2 hours"},
    ]
    
    enterprise_tasks = pro_tasks + [
        {"id": "buddy_intro", "title": "Meet Your Onboarding Buddy", "description": "Connect with your peer buddy", "category": "Buddy System", "duration": "30 min"},
        {"id": "exec_welcome", "title": "Executive Welcome Session", "description": "Meet leadership and learn company vision", "category": "Leadership", "duration": "1 hour"},
        {"id": "custom_training", "title": "Custom Role Training", "description": "Specialized training for your position", "category": "Training", "duration": "4 hours"},
        {"id": "cross_team_intro", "title": "Cross-Team Introductions", "description": "Meet key stakeholders from other departments", "category": "Networking", "duration": "1 hour"},
    ]
    
    if plan == "Basic":
        return basic_tasks
    elif plan == "Pro":
        return pro_tasks
    else:
        return enterprise_tasks

def render_checklist(user, services):
    """Render interactive onboarding checklist"""
    st.title("✅ Your Onboarding Checklist")
    
    st.markdown(f"""
    Complete these tasks to ensure a smooth onboarding experience.
    Your plan: **{user['plan']}**
    """)
    
    # Load checklist
    checklist = load_checklist_template(user['plan'])
    completed = user.get('checklist_completed', [])
    
    # Progress metrics
    total_tasks = len(checklist)
    completed_tasks = len(completed)
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tasks", total_tasks)
    with col2:
        st.metric("Completed", completed_tasks, delta=f"{progress}%")
    with col3:
        st.metric("Remaining", total_tasks - completed_tasks)
    
    st.progress(progress / 100, text=f"{progress}% Complete")
    
    # Filter options
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        categories = ["All"] + sorted(list(set(task['category'] for task in checklist)))
        selected_category = st.selectbox("Filter by Category", categories)
    
    with col2:
        show_completed = st.checkbox("Show Completed", value=True)
    
    # Group tasks by category
    st.markdown("---")
    
    filtered_checklist = checklist
    if selected_category != "All":
        filtered_checklist = [t for t in checklist if t['category'] == selected_category]
    
    if not show_completed:
        filtered_checklist = [t for t in filtered_checklist if t['id'] not in completed]
    
    # Display tasks
    for task in filtered_checklist:
        is_completed = task['id'] in completed
        
        with st.container():
            col1, col2 = st.columns([0.1, 0.9])
            
            with col1:
                checkbox = st.checkbox(
                    "",
                    value=is_completed,
                    key=f"task_{task['id']}",
                    label_visibility="collapsed"
                )
                
                # Update completion status
                if checkbox and not is_completed:
                    completed.append(task['id'])
                    user['checklist_completed'] = completed
                    user['onboarding_progress'] = int((len(completed) / total_tasks) * 100)
                    services['auth'].update_user(user['email'], user)
                    st.rerun()
                elif not checkbox and is_completed:
                    completed.remove(task['id'])
                    user['checklist_completed'] = completed
                    user['onboarding_progress'] = int((len(completed) / total_tasks) * 100)
                    services['auth'].update_user(user['email'], user)
                    st.rerun()
            
            with col2:
                style = "text-decoration: line-through; opacity: 0.6;" if is_completed else ""
                st.markdown(f"""
                <div style="{style}">
                    <h4>{task['title']} 
                    <span style="background: #e7f3ff; padding: 2px 8px; border-radius: 4px; font-size: 12px;">
                        {task['category']}
                    </span>
                    </h4>
                    <p style="color: #666;">{task['description']}</p>
                    <small>⏱️ Estimated time: {task['duration']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                if not is_completed:
                    if st.button(f"📖 View Details", key=f"details_{task['id']}"):
                        st.info(f"**{task['title']}**\n\n{task['description']}\n\nEstimated duration: {task['duration']}")
        
        st.markdown("---")
    
    # Send reminder button
    if completed_tasks < total_tasks:
        st.markdown("### 📧 Need a Reminder?")
        if st.button("Send Checklist Reminder Email"):
            pending_tasks = [t['title'] for t in checklist if t['id'] not in completed]
            success = services['email'].send_checklist_reminder(
                user['email'],
                user['name'],
                pending_tasks[:5]  # Send top 5 pending tasks
            )
            if success:
                st.success("✅ Reminder email sent!")
            else:
                st.warning("Could not send email at this time.")
    else:
        st.success("🎉 Congratulations! You've completed all your onboarding tasks!")
        st.balloons()