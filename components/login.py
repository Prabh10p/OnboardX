import streamlit as st

def render_login(services):
    """Render login form"""
    st.subheader("🔐 Welcome Back!")
    st.markdown("Log in to continue your onboarding journey")
    
    with st.form("login_form"):
        email = st.text_input(
            "📧 Email",
            placeholder="your.email@company.com"
        )
        
        password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter your password"
        )
        
        remember_me = st.checkbox("Remember me")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            submit = st.form_submit_button("🚀 Log In", use_container_width=True, type="primary")
        
        if submit:
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                user = services['auth'].authenticate(email.strip(), password)
                
                if user:
                    st.session_state["user"] = user
                    st.success(f"Welcome back, {user['name']}! 👋")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
    
    st.markdown("---")
    st.caption("Forgot your password? Contact your HR administrator.")