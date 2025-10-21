import streamlit as st

def render_resources(user, services):
    """Render training resources and materials"""
    st.title("📚 Resources & Training")
    
    st.markdown("""
    Access all the resources you need to succeed in your new role.
    Everything is organized and contextualized for your position.
    """)
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 Search resources...", placeholder="e.g., security training")
    with col2:
        resource_type = st.selectbox("Type", ["All", "Video", "Document", "Course", "Tool"])
    
    st.markdown("---")
    
    # Tabs for different resource categories
    tab1, tab2, tab3, tab4 = st.tabs(["🎓 Training", "📖 Documentation", "🛠️ Tools", "🎯 Role-Specific"])
    
    with tab1:
        st.subheader("Training Courses")
        st.markdown("Complete these courses to build your skills and knowledge")
        
        courses = [
            {
                "title": "Company Culture & Values",
                "description": "Learn about our mission, vision, and core values",
                "duration": "30 min",
                "type": "Video",
                "progress": 100,
                "required": True
            },
            {
                "title": "Information Security Fundamentals",
                "description": "Essential security practices and data protection",
                "duration": "1 hour",
                "type": "Course",
                "progress": 0,
                "required": True
            },
            {
                "title": "Effective Communication",
                "description": "Best practices for team communication and collaboration",
                "duration": "45 min",
                "type": "Video",
                "progress": 0,
                "required": False
            },
            {
                "title": "Time Management Techniques",
                "description": "Strategies for productivity and work-life balance",
                "duration": "40 min",
                "type": "Course",
                "progress": 0,
                "required": False
            },
        ]
        
        for course in courses:
            with st.expander(f"{'🔴' if course['required'] else '🟢'} {course['title']} - {course['duration']}"):
                st.markdown(f"**{course['description']}**")
                st.markdown(f"*Type: {course['type']}* | *{'Required' if course['required'] else 'Optional'}*")
                
                if course['progress'] > 0:
                    st.progress(course['progress'] / 100, text=f"{course['progress']}% complete")
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button("▶️ Start", key=f"start_{course['title']}"):
                        st.info("Opening course...")
                with col2:
                    if course['progress'] == 100:
                        st.success("✅ Completed!")
    
    with tab2:
        st.subheader("Documentation & Policies")
        st.markdown("Important documents and company policies")
        
        docs = [
            {
                "title": "Employee Handbook",
                "description": "Complete guide to company policies and procedures",
                "category": "Policy",
                "pages": 45
            },
            {
                "title": "Benefits Guide",
                "description": "Overview of health, retirement, and other benefits",
                "category": "HR",
                "pages": 20
            },
            {
                "title": "Code of Conduct",
                "description": "Expected behavior and ethical guidelines",
                "category": "Policy",
                "pages": 12
            },
            {
                "title": "IT Usage Policy",
                "description": "Guidelines for using company technology",
                "category": "IT",
                "pages": 8
            },
            {
                "title": "Emergency Procedures",
                "description": "What to do in case of emergencies",
                "category": "Safety",
                "pages": 6
            },
        ]
        
        for doc in docs:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**📄 {doc['title']}**")
                st.caption(doc['description'])
            with col2:
                st.caption(f"📑 {doc['pages']} pages")
            with col3:
                if st.button("View", key=f"view_{doc['title']}"):
                    st.info(f"Opening {doc['title']}...")
    
    with tab3:
        st.subheader("Essential Tools")
        st.markdown("Tools and applications you'll use daily")
        
        tools = [
            {
                "name": "Email & Calendar",
                "description": "Company email and calendar system",
                "status": "Active",
                "icon": "📧"
            },
            {
                "name": "Slack",
                "description": "Team communication platform",
                "status": "Active",
                "icon": "💬"
            },
            {
                "name": "Project Management",
                "description": "Track tasks and project progress",
                "status": "Pending Setup",
                "icon": "📊"
            },
            {
                "name": "HR Portal",
                "description": "Manage payroll, time off, and benefits",
                "status": "Active",
                "icon": "👥"
            },
            {
                "name": "Document Storage",
                "description": "Cloud storage for files and documents",
                "status": "Active",
                "icon": "📁"
            },
        ]
        
        cols = st.columns(2)
        for idx, tool in enumerate(tools):
            with cols[idx % 2]:
                with st.container():
                    st.markdown(f"""
                    <div style="padding: 20px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px;">
                        <h3>{tool['icon']} {tool['name']}</h3>
                        <p>{tool['description']}</p>
                        <span style="background: {'#d4edda' if tool['status'] == 'Active' else '#fff3cd'}; 
                              padding: 4px 12px; border-radius: 4px; font-size: 12px;">
                            {tool['status']}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if tool['status'] == "Active":
                        if st.button(f"Open {tool['name']}", key=f"open_{tool['name']}"):
                            st.info(f"Launching {tool['name']}...")
                    else:
                        if st.button(f"Set Up {tool['name']}", key=f"setup_{tool['name']}"):
                            st.info(f"Setting up {tool['name']}...")
    
    with tab4:
        st.subheader(f"Resources for {user.get('role', 'Your Role')}")
        st.markdown(f"Customized resources for your role in {user.get('department', 'your department')}")
        
        # AI-generated personalized learning path
        if st.button("🤖 Generate Personalized Learning Path"):
            with st.spinner("Creating your custom learning path..."):
                learning_path = services['llm'].suggest_learning_path(
                    user.get('role', 'Employee'),
                    user['plan']
                )
                
                if learning_path:
                    st.success("✨ Here's your personalized learning path!")
                    for idx, resource in enumerate(learning_path, 1):
                        st.markdown(f"""
                        **{idx}. {resource.get('title', 'Resource')}**  
                        {resource.get('description', '')}  
                        *Duration: {resource.get('duration', 'N/A')}*
                        """)
                        st.markdown("---")
                else:
                    st.info("Check back soon for personalized recommendations!")
        
        st.markdown("---")
        st.markdown("### 📌 Quick Links")
        
        quick_links = [
            "🔗 Department Wiki",
            "🔗 Team Drive",
            "🔗 Project Templates",
            "🔗 Best Practices Guide",
            "🔗 FAQ & Troubleshooting"
        ]
        
        for link in quick_links:
            st.markdown(f"- {link}")
    
    # Download section
    st.markdown("---")
    st.subheader("📥 Downloads")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            label="📄 Employee Handbook (PDF)",
            data="Sample handbook content",
            file_name="employee_handbook.pdf",
            mime="application/pdf"
        )
    with col2:
        st.download_button(
            label="📋 Onboarding Checklist",
            data="Sample checklist",
            file_name="onboarding_checklist.txt",
            mime="text/plain"
        )
    with col3:
        st.download_button(
            label="🎯 Goal Setting Template",
            data="Sample goals template",
            file_name="goals_template.txt",
            mime="text/plain"
        )