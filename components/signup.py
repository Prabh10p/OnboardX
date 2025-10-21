import streamlit as st
from datetime import datetime

def render_signup(services):
    """Render step-by-step signup process"""
    st.subheader("🚀 Create Your Account")
    st.markdown("Let's get you started with a personalized onboarding experience!")
    
    # Progress indicator
    progress = st.session_state.signup_step / 4
    st.progress(progress)
    st.caption(f"Step {st.session_state.signup_step + 1} of 5")
    
    # Step 0: Name
    if st.session_state.signup_step == 0:
        st.markdown("### 👋 What's your name?")
        st.caption("Let us know how to address you")
        
        name = st.text_input(
            "Full Name",
            value=st.session_state.signup_data.get("name", ""),
            placeholder="e.g., Sarah Johnson",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Next →", use_container_width=True):
                if name.strip():
                    st.session_state.signup_data["name"] = name.strip()
                    st.session_state.signup_step = 1
                    st.rerun()
                else:
                    st.warning("Please enter your name to continue.")
    
    # Step 1: Email
    elif st.session_state.signup_step == 1:
        st.markdown(f"### 📧 Hi {st.session_state.signup_data['name']}! What's your email?")
        st.caption("We'll use this for your login and important updates")
        
        email = st.text_input(
            "Email Address",
            value=st.session_state.signup_data.get("email", ""),
            placeholder="e.g., sarah.johnson@company.com",
            label_visibility="collapsed"
        )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            if st.button("← Back"):
                st.session_state.signup_step = 0
                st.rerun()
        with col3:
            if st.button("Next →", use_container_width=True):
                email = email.strip()
                if not email:
                    st.warning("Please enter your email to continue.")
                elif not services['email'].is_valid_email(email):
                    st.warning("⚠️ Please enter a valid email address.")
                else:
                    # Check if user already exists
                    existing = services['auth'].get_user(email)
                    if existing:
                        st.error("This email is already registered. Please use the login tab.")
                    else:
                        st.session_state.signup_data["email"] = email
                        st.session_state.signup_step = 2
                        st.rerun()
    
    # Step 2: Password
    elif st.session_state.signup_step == 2:
        st.markdown("### 🔑 Create a secure password")
        st.caption("Make it strong! Use at least 8 characters")
        
        password = st.text_input(
            "Password",
            type="password",
            value=st.session_state.signup_data.get("password", ""),
            placeholder="Enter a secure password",
            label_visibility="collapsed"
        )
        
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password"
        )
        
        # Password strength indicator
        if password:
            strength = 0
            if len(password) >= 8:
                strength += 25
            if any(c.isupper() for c in password):
                strength += 25
            if any(c.isdigit() for c in password):
                strength += 25
            if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
                strength += 25
            
            color = "red" if strength < 50 else "orange" if strength < 75 else "green"
            st.markdown(f"Password Strength: :{color}[{'▮' * (strength // 25)}{'▯' * (4 - strength // 25)}]")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            if st.button("← Back"):
                st.session_state.signup_step = 1
                st.rerun()
        with col3:
            if st.button("Next →", use_container_width=True):
                if not password.strip():
                    st.warning("Please enter a password to continue.")
                elif len(password) < 8:
                    st.warning("Password must be at least 8 characters long.")
                elif password != confirm_password:
                    st.error("Passwords don't match!")
                else:
                    st.session_state.signup_data["password"] = password.strip()
                    st.session_state.signup_step = 3
                    st.rerun()
    
    # Step 3: Role & Department
    elif st.session_state.signup_step == 3:
        st.markdown("### 💼 Tell us about your role")
        st.caption("This helps us customize your onboarding experience")
        
        col1, col2 = st.columns(2)
        with col1:
            role = st.text_input(
                "Job Role",
                value=st.session_state.signup_data.get("role", ""),
                placeholder="e.g., Software Engineer"
            )
        with col2:
            department = st.selectbox(
                "Department",
                ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations", "Design", "Other"],
                index=0
            )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            if st.button("← Back"):
                st.session_state.signup_step = 2
                st.rerun()
        with col3:
            if st.button("Next →", use_container_width=True):
                if role.strip():
                    st.session_state.signup_data["role"] = role.strip()
                    st.session_state.signup_data["department"] = department
                    st.session_state.signup_step = 4
                    st.rerun()
                else:
                    st.warning("Please enter your role to continue.")
    
    # Step 4: Plan Selection
    elif st.session_state.signup_step == 4:
        st.markdown("### 📦 Choose your onboarding plan")
        st.caption("Select the plan that best fits your needs")
        
        plan_col1, plan_col2, plan_col3 = st.columns(3)
        
        with plan_col1:
            with st.container():
                st.markdown("#### 🌟 Basic")
                st.markdown("**Free**")
                st.markdown("---")
                st.markdown("""
                - ✅ Essential checklist
                - 📚 Basic resources
                - 📧 Email support
                - 📊 Progress tracking
                """)
                if st.button("Select Basic", key="basic", use_container_width=True):
                    st.session_state.signup_data["plan"] = "Basic"
        
        with plan_col2:
            with st.container():
                st.markdown("#### 🚀 Pro")
                st.markdown("**$29/month**")
                st.markdown("---")
                st.markdown("""
                - ✅ All Basic features
                - 👥 Mentor assignment
                - 🎯 Goal setting
                - 📹 Video tutorials
                - 💬 Priority support
                """)
                if st.button("Select Pro", key="pro", use_container_width=True):
                    st.session_state.signup_data["plan"] = "Pro"
        
        with plan_col3:
            with st.container():
                st.markdown("#### 💎 Enterprise")
                st.markdown("**Custom**")
                st.markdown("---")
                st.markdown("""
                - ✅ All Pro features
                - 🤝 Buddy system
                - 📊 Analytics dashboard
                - 🎓 Custom training
                - 👨‍💼 Dedicated support
                """)
                if st.button("Select Enterprise", key="enterprise", use_container_width=True):
                    st.session_state.signup_data["plan"] = "Enterprise"
        
        # Create account if plan is selected
        if "plan" in st.session_state.signup_data:
            st.markdown("---")
            st.success(f"✅ {st.session_state.signup_data['plan']} plan selected!")
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                if st.button("← Back"):
                    st.session_state.signup_data.pop("plan", None)
                    st.rerun()
            with col3:
                if st.button("🎉 Create Account", use_container_width=True, type="primary"):
                    try:
                        # Create user account
                        user_data = services['auth'].create_user(
                            name=st.session_state.signup_data["name"],
                            email=st.session_state.signup_data["email"],
                            password=st.session_state.signup_data["password"],
                            plan=st.session_state.signup_data["plan"]
                        )
                        
                        # Update with additional info
                        user_data['role'] = st.session_state.signup_data.get("role", "")
                        user_data['department'] = st.session_state.signup_data.get("department", "")
                        services['auth'].update_user(user_data['email'], user_data)
                        
                        # Send welcome email
                        services['email'].send_welcome_email(
                            user_data['email'],
                            user_data['name'],
                            user_data['plan']
                        )
                        
                        # Set session and reset
                        st.session_state["user"] = user_data
                        st.session_state.signup_step = 0
                        st.session_state.signup_data = {}
                        
                        st.success(f"🎉 Welcome aboard, {user_data['name']}!")
                        st.balloons()
                        st.rerun()
                        
                    except ValueError as e:
                        st.error(f"Error creating account: {str(e)}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {str(e)}")