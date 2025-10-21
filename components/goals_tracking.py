import streamlit as st
from datetime import datetime, timedelta
import json

def render_goals_tracking(user, services):
    """30-60-90 day goals tracking system"""
    st.title("🎯 Goals & Milestones")
    
    # Initialize goals in session state
    if 'goals' not in st.session_state:
        st.session_state.goals = get_default_goals(user)
    
    # Progress overview
    goals = st.session_state.goals
    completed = len([g for g in goals if g['status'] == 'completed'])
    total = len(goals)
    progress = (completed / total * 100) if total > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Goals", total)
    with col2:
        st.metric("Completed", completed, delta=f"{progress:.0f}%")
    with col3:
        in_progress = len([g for g in goals if g['status'] == 'in_progress'])
        st.metric("In Progress", in_progress)
    with col4:
        not_started = len([g for g in goals if g['status'] == 'not_started'])
        st.metric("Not Started", not_started)
    
    st.progress(progress / 100)
    
    st.markdown("---")
    
    # Tabs for 30-60-90 day goals
    tab1, tab2, tab3, tab4 = st.tabs(["📅 30 Days", "📅 60 Days", "📅 90 Days", "➕ Custom Goals"])
    
    with tab1:
        render_goal_period(goals, "30_days", "First 30 Days", user, services)
    
    with tab2:
        render_goal_period(goals, "60_days", "First 60 Days", user, services)
    
    with tab3:
        render_goal_period(goals, "90_days", "First 90 Days", user, services)
    
    with tab4:
        render_custom_goals(goals, user)

def render_goal_period(goals, period, title, user, services):
    """Render goals for a specific period"""
    st.subheader(title)
    
    period_goals = [g for g in goals if g['period'] == period]
    
    if not period_goals:
        st.info(f"No goals set for {title.lower()}")
        return
    
    for goal in period_goals:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                status_emoji = get_status_emoji(goal['status'])
                st.markdown(f"### {status_emoji} {goal['title']}")
                st.write(goal['description'])
                
                if goal.get('subtasks'):
                    completed_subtasks = len([t for t in goal['subtasks'] if t['completed']])
                    total_subtasks = len(goal['subtasks'])
                    st.progress(completed_subtasks / total_subtasks if total_subtasks > 0 else 0)
                    st.caption(f"Subtasks: {completed_subtasks}/{total_subtasks}")
            
            with col2:
                st.write(f"**Due:** {goal['due_date']}")
                st.write(f"**Priority:** {goal['priority']}")
            
            with col3:
                new_status = st.selectbox(
                    "Status",
                    ["not_started", "in_progress", "completed"],
                    index=["not_started", "in_progress", "completed"].index(goal['status']),
                    key=f"status_{goal['id']}"
                )
                
                if new_status != goal['status']:
                    goal['status'] = new_status
                    if new_status == 'completed':
                        st.success("🎉 Goal completed!")
                        st.balloons()
                    st.rerun()
            
            # Subtasks
            if goal.get('subtasks'):
                with st.expander("View Subtasks"):
                    for i, subtask in enumerate(goal['subtasks']):
                        completed = st.checkbox(
                            subtask['title'],
                            value=subtask['completed'],
                            key=f"subtask_{goal['id']}_{i}"
                        )
                        if completed != subtask['completed']:
                            subtask['completed'] = completed
                            st.rerun()
            
            # Notes
            with st.expander("📝 Add Notes"):
                notes = st.text_area(
                    "Progress notes",
                    value=goal.get('notes', ''),
                    key=f"notes_{goal['id']}"
                )
                if st.button("Save Notes", key=f"save_notes_{goal['id']}"):
                    goal['notes'] = notes
                    st.success("Notes saved!")
            
            st.markdown("---")

def render_custom_goals(goals, user):
    """Add and manage custom goals"""
    st.subheader("Create Custom Goal")
    
    with st.form("add_custom_goal"):
        goal_title = st.text_input("Goal Title")
        goal_desc = st.text_area("Description")
        
        col1, col2 = st.columns(2)
        with col1:
            period = st.selectbox("Time Period", ["30_days", "60_days", "90_days", "custom"])
        with col2:
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        due_date = st.date_input("Due Date", min_value=datetime.now().date())
        
        submitted = st.form_submit_button("➕ Add Goal")
        
        if submitted and goal_title:
            new_goal = {
                "id": f"goal_{datetime.now().timestamp()}",
                "title": goal_title,
                "description": goal_desc,
                "period": period,
                "priority": priority,
                "due_date": due_date.strftime("%b %d, %Y"),
                "status": "not_started",
                "subtasks": [],
                "notes": ""
            }
            st.session_state.goals.append(new_goal)
            st.success("Goal added!")
            st.rerun()
    
    # Display custom goals
    st.markdown("---")
    st.subheader("Your Custom Goals")
    
    custom_goals = [g for g in goals if g.get('custom', False) or g['period'] == 'custom']
    
    if custom_goals:
        for goal in custom_goals:
            col1, col2 = st.columns([4, 1])
            with col1:
                status_emoji = get_status_emoji(goal['status'])
                st.markdown(f"**{status_emoji} {goal['title']}** - {goal['description']}")
            with col2:
                if st.button("🗑️", key=f"delete_{goal['id']}"):
                    st.session_state.goals.remove(goal)
                    st.rerun()
    else:
        st.info("No custom goals yet. Add one above!")

def get_default_goals(user):
    """Generate default onboarding goals"""
    return [
        {
            "id": "g1",
            "title": "Complete all HR paperwork",
            "description": "Submit all required documents including tax forms, benefits enrollment, and emergency contacts",
            "period": "30_days",
            "priority": "High",
            "due_date": "Week 1",
            "status": "not_started",
            "subtasks": [
                {"title": "I-9 verification", "completed": False},
                {"title": "W-4 tax form", "completed": False},
                {"title": "Benefits enrollment", "completed": False},
                {"title": "Direct deposit setup", "completed": False}
            ],
            "notes": ""
        },
        {
            "id": "g2",
            "title": "Meet with your team",
            "description": "Schedule 1:1 meetings with all immediate team members",
            "period": "30_days",
            "priority": "High",
            "due_date": "Week 2",
            "status": "not_started",
            "subtasks": [
                {"title": "Manager 1:1", "completed": False},
                {"title": "Team standup", "completed": False},
                {"title": "Buddy session", "completed": False}
            ],
            "notes": ""
        },
        {
            "id": "g3",
            "title": "Complete training modules",
            "description": "Finish all required onboarding training courses",
            "period": "30_days",
            "priority": "Medium",
            "due_date": "Week 3",
            "status": "not_started",
            "subtasks": [
                {"title": "Company culture training", "completed": False},
                {"title": "Security & compliance", "completed": False},
                {"title": "Tools & systems overview", "completed": False}
            ],
            "notes": ""
        },
        {
            "id": "g4",
            "title": "Deliver first project",
            "description": "Complete and present your first project or major task",
            "period": "60_days",
            "priority": "High",
            "due_date": "Day 45",
            "status": "not_started",
            "subtasks": [],
            "notes": ""
        },
        {
            "id": "g5",
            "title": "Build cross-functional relationships",
            "description": "Connect with key stakeholders in other departments",
            "period": "60_days",
            "priority": "Medium",
            "due_date": "Day 60",
            "status": "not_started",
            "subtasks": [],
            "notes": ""
        },
        {
            "id": "g6",
            "title": "Master core responsibilities",
            "description": "Demonstrate proficiency in all primary job functions",
            "period": "90_days",
            "priority": "High",
            "due_date": "Day 90",
            "status": "not_started",
            "subtasks": [],
            "notes": ""
        }
    ]

def get_status_emoji(status):
    """Get emoji for goal status"""
    if status == "completed":
        return "✅"
    elif status == "in_progress":
        return "🔄"
    else:
        return "⭕"