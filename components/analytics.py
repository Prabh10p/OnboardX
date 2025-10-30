import streamlit as st
from datetime import datetime, timedelta
import json

def render_analytics(user, services):
    """Analytics and progress tracking dashboard"""
    st.title("📊 Analytics & Insights")
    
    st.markdown("Track your onboarding progress and engagement metrics")
    
    # Time-based metrics
    join_date = datetime.fromisoformat(user.get('join_date_full', datetime.now().isoformat()))
    days_since_join = (datetime.now() - join_date).days
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Days at Company", days_since_join)
    
    with col2:
        meetings = st.session_state.get('meetings', [])
        st.metric("Meetings Scheduled", len(meetings))
    
    with col3:
        goals = st.session_state.get('goals', [])
        completed_goals = len([g for g in goals if isinstance(g, dict) and g.get('status') == 'completed'])
        st.metric("Goals Completed", completed_goals)
    
    with col4:
        # Calculate completion percentage
        total_items = len(goals) + 10  # 10 checklist items (approximate)
        completed_items = completed_goals + 5  # approximate checklist completion
        completion_pct = min(100, int((completed_items / total_items) * 100))
        st.metric("Overall Progress", f"{completion_pct}%")
    
    st.markdown("---")
    
    # Progress by category
    st.subheader("📈 Progress by Category")
    
    tab1, tab2, tab3 = st.tabs(["Goals Progress", "Meeting Activity", "Engagement Score"])
    
    with tab1:
        render_goals_progress(goals)
    
    with tab2:
        render_meeting_activity(meetings)
    
    with tab3:
        render_engagement_score(user, days_since_join, meetings, goals)

def render_goals_progress(goals):
    """Display goals progress visualization"""
    if not isinstance(goals, list) or not goals:
        st.info("No goals data available yet")
        return
    
    # Count by period
    period_stats = {
        "30_days": {"total": 0, "completed": 0},
        "60_days": {"total": 0, "completed": 0},
        "90_days": {"total": 0, "completed": 0}
    }
    
    for goal in goals:
        if isinstance(goal, dict):
            period = goal.get('period', 'custom')
            if period in period_stats:
                period_stats[period]["total"] += 1
                if goal.get('status') == 'completed':
                    period_stats[period]["completed"] += 1
    
    # Display progress bars
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**30-Day Goals**")
        if period_stats["30_days"]["total"] > 0:
            progress = period_stats["30_days"]["completed"] / period_stats["30_days"]["total"]
            st.progress(progress)
            st.caption(f"{period_stats['30_days']['completed']}/{period_stats['30_days']['total']} completed")
        else:
            st.caption("No goals set")
    
    with col2:
        st.markdown("**60-Day Goals**")
        if period_stats["60_days"]["total"] > 0:
            progress = period_stats["60_days"]["completed"] / period_stats["60_days"]["total"]
            st.progress(progress)
            st.caption(f"{period_stats['60_days']['completed']}/{period_stats['60_days']['total']} completed")
        else:
            st.caption("No goals set")
    
    with col3:
        st.markdown("**90-Day Goals**")
        if period_stats["90_days"]["total"] > 0:
            progress = period_stats["90_days"]["completed"] / period_stats["90_days"]["total"]
            st.progress(progress)
            st.caption(f"{period_stats['90_days']['completed']}/{period_stats['90_days']['total']} completed")
        else:
            st.caption("No goals set")
    
    # Upcoming deadlines
    st.markdown("---")
    st.subheader("⏰ Upcoming Deadlines")
    
    upcoming = [g for g in goals if isinstance(g, dict) and g.get('status') != 'completed']
    
    if upcoming:
        for goal in upcoming[:5]:  # Show top 5
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{goal.get('title', 'Untitled')}**")
            with col2:
                st.caption(f"Due: {goal.get('due_date', 'TBD')}")
    else:
        st.success("🎉 All goals completed!")

def render_meeting_activity(meetings):
    """Display meeting activity metrics"""
    if not isinstance(meetings, list):
        meetings = []
    
    st.markdown("### Meeting Statistics")
    
    total_meetings = len(meetings)
    
    if total_meetings == 0:
        st.info("No meetings scheduled yet. Visit Team Directory to schedule your first meeting!")
        return
    
    # Count by status
    pending = len([m for m in meetings if isinstance(m, dict) and m.get('status') == 'pending'])
    completed = len([m for m in meetings if isinstance(m, dict) and m.get('status') == 'completed'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Meetings", total_meetings)
    with col2:
        st.metric("Upcoming", pending)
    with col3:
        st.metric("Completed", completed)
    
    # Recent meetings
    st.markdown("---")
    st.markdown("**Recent Meetings**")
    
    for meeting in meetings[:5]:
        if isinstance(meeting, dict):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"• {meeting.get('title', 'Untitled')}")
                if 'with' in meeting:
                    st.caption(f"with {meeting['with']}")
            with col2:
                status = meeting.get('status', 'scheduled')
                if status == 'completed':
                    st.success("✅")
                else:
                    st.info("📅")

def render_engagement_score(user, days_since_join, meetings, goals):
    """Calculate and display engagement score"""
    st.markdown("### Your Engagement Score")
    
    # Calculate score (0-100)
    score = 0
    
    # Days active (max 20 points)
    score += min(20, days_since_join * 2)
    
    # Meetings scheduled (max 30 points)
    if isinstance(meetings, list):
        score += min(30, len(meetings) * 5)
    
    # Goals progress (max 30 points)
    if isinstance(goals, list) and goals:
        completed = len([g for g in goals if isinstance(g, dict) and g.get('status') == 'completed'])
        total = len(goals)
        score += int((completed / total) * 30) if total > 0 else 0
    
    # Profile completion (max 20 points)
    profile_fields = ['name', 'email', 'department', 'role', 'bio']
    filled_fields = sum(1 for field in profile_fields if user.get(field))
    score += int((filled_fields / len(profile_fields)) * 20)
    
    # Display score
    score = min(100, score)
    
    # Color based on score
    if score >= 80:
        color = "🟢"
        message = "Excellent! You're highly engaged."
    elif score >= 60:
        color = "🟡"
        message = "Good progress! Keep it up."
    elif score >= 40:
        color = "🟠"
        message = "Getting started. Explore more features!"
    else:
        color = "🔴"
        message = "Let's get you more engaged!"
    
    st.markdown(f"## {color} {score}/100")
    st.progress(score / 100)
    st.caption(message)
    
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Recommendations")
    
    recommendations = []
    
    if not isinstance(meetings, list) or len(meetings) < 3:
        recommendations.append("Schedule more 1:1 meetings with your team members")
    
    if not isinstance(goals, list) or not goals:
        recommendations.append("Set some custom goals to track your progress")
    
    if not user.get('bio'):
        recommendations.append("Complete your profile by adding a bio in Settings")
    
    if isinstance(goals, list):
        completed = len([g for g in goals if isinstance(g, dict) and g.get('status') == 'completed'])
        if completed == 0 and goals:
            recommendations.append("Mark your first goal as completed!")
    
    if not recommendations:
        recommendations.append("You're doing great! Keep engaging with the platform.")
    
    for rec in recommendations:
        st.markdown(f"• {rec}")