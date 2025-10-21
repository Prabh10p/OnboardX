import streamlit as st
from datetime import datetime

def render_feedback(user, services):
    """Render feedback collection interface"""
    st.title("💬 Share Your Feedback")
    
    st.markdown("""
    We’d love to hear your thoughts about your onboarding experience!
    Your feedback helps us improve and make OnboardX even better.
    """)
    
    st.markdown("---")
    
    # Rating section
    st.subheader("⭐ Overall Experience")
    rating = st.slider("Rate your onboarding experience (1 = poor, 5 = excellent)", 1, 5, 4)
    
    # Text feedback section
    st.subheader("🗒️ Additional Comments")
    feedback_text = st.text_area("Share your suggestions or experiences here...")
    
    # Improvement options
    st.subheader("⚙️ What could we improve?")
    improvements = st.multiselect(
        "Select any areas you'd like to see improved:",
        ["Onboarding Speed", "Communication", "Resources Provided", "Mentorship", "User Interface", "Other"]
    )
    
    # Submit button
    if st.button("📨 Submit Feedback"):
        if feedback_text.strip() == "":
            st.warning("Please write some feedback before submitting.")
        else:
            feedback_entry = {
                "user": user["email"],
                "name": user["name"],
                "rating": rating,
                "feedback": feedback_text,
                "improvements": improvements,
                "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Save feedback (local JSON storage)
            try:
                with open("data/feedback.json", "a") as f:
                    f.write(f"{feedback_entry}\n")
            except FileNotFoundError:
                st.error("Feedback storage not found — please ensure 'data/' folder exists.")
            
            # Optional: send email notification to admin
            try:
                services["email"].send_email(
                    to="admin@onboardx.com",
                    subject=f"New Feedback from {user['name']}",
                    body=f"""
                    ⭐ Rating: {rating}/5
                    🧑 User: {user['name']} ({user['email']})
                    📝 Feedback: {feedback_text}
                    ⚙️ Suggested Improvements: {', '.join(improvements) if improvements else 'None'}
                    """
                )
            except Exception as e:
                st.warning(f"Email service not available: {e}")
            
            st.success("✅ Thank you for your feedback! It’s been successfully submitted.")
