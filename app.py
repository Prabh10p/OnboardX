import streamlit as st
import json
import os
import re
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()

# ===========================
# 🧠 User Schema
# ===========================
class UserOnboarding(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    plan: str | None = None

# ===========================
# ⚙️ Load LLM
# ===========================
@st.cache_resource
def load_model():
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.3",
        task="text-generation",
        max_new_tokens=256,
        temperature=0.3,
    )
    return ChatHuggingFace(llm=llm)

model = load_model()

# ===========================
# 💡 Prompt Template
# ===========================
prompt_template = PromptTemplate(
    template=(
        "You are an AI assistant for onboarding. Extract name, email, password from natural language.\n"
        "Return JSON only, no extra text. Example:\n"
        "{{\"name\": \"Akhil\", \"email\": \"akhil@gmail.com\", \"password\": \"secure123\"}}\n\n"
        "User Input: {user_input}"
    ),
    input_variables=["user_input"],
)

# ===========================
# 📁 User storage
# ===========================
USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

users = load_users()

# ===========================
# ✉️ Email helper
# ===========================
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")

def is_valid_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def send_confirmation_email(to_email: str, name: str, plan: str):
    if not is_valid_email(to_email):
        st.warning("❌ Invalid email address.")
        return

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        message = Mail(
            from_email=EMAIL_FROM,
            to_emails=to_email,
            subject="🎉 OnboardX Account Created!",
            html_content=f"""
                <p>Hi {name},</p>
                <p>Your OnboardX account has been successfully created!</p>
                <p>Your selected plan: <b>{plan}</b></p>
                <p>Welcome aboard!</p>
                <p>— OnboardX Team</p>
            """
        )
        sg.send(message)
        st.success(f"✅ Confirmation email sent to {to_email}!")
    except Exception as e:
        st.warning(f"Could not send email: {e}")

# ===========================
# 🏗️ Streamlit UI
# ===========================
st.set_page_config(page_title="OnboardX Personalized Assistant", page_icon="🤖", layout="centered")
st.title("🤖 Personalized Onboarding Assistant")
st.markdown(
    "Step-by-step AI-guided onboarding. Users are welcomed personally and guided progressively."
)

# ===========================
# Step-by-step signup session
# ===========================
if "signup_step" not in st.session_state:
    st.session_state.signup_step = 0
    st.session_state.signup_data = {}

tab1, tab2 = st.tabs(["🆕 Sign Up", "🔑 Log In"])

# ===========================
# SIGN UP
# ===========================
with tab1:
    st.subheader("Step-by-step Signup")

    if st.session_state.signup_step == 0:
        name = st.text_input("👋 What's your name?", value=st.session_state.signup_data.get("name", ""))
        if st.button("Next →"):
            if name.strip():
                st.session_state.signup_data["name"] = name.strip()
                st.session_state.signup_step = 1
            else:
                st.warning("Please enter your name to continue.")

    elif st.session_state.signup_step == 1:
        email_input = st.text_input("📧 Email", value=st.session_state.signup_data.get("email", ""))
        if st.button("Next →"):
            email_input = email_input.strip()
            if not email_input:
                st.warning("Please enter your email to continue.")
            elif not is_valid_email(email_input):
                st.warning("⚠️ Please enter a valid email address.")
            else:
                st.session_state.signup_data["email"] = email_input
                st.session_state.signup_step = 2

    elif st.session_state.signup_step == 2:
        password = st.text_input("🔑 Password", type="password", value=st.session_state.signup_data.get("password", ""))
        if st.button("Next →"):
            if password.strip():
                st.session_state.signup_data["password"] = password.strip()
                st.session_state.signup_step = 3
            else:
                st.warning("Please enter a password to continue.")

    elif st.session_state.signup_step == 3:
        plan = st.radio("📦 Choose your onboarding plan", ["Basic", "Pro", "Enterprise"], index=0)
        if st.button("Create Account"):
            st.session_state.signup_data["plan"] = plan
            data = UserOnboarding(**st.session_state.signup_data)

            if not data.name or not data.password or not data.email:
                st.error("⚠️ Name, email, and password are required!")
            else:
                # Save user
                users[data.email] = {
                    "name": data.name,
                    "password": data.password,
                    "plan": data.plan
                }
                save_users(users)

                # Send confirmation email
                send_confirmation_email(data.email, data.name, data.plan)

                st.success(f"🎉 Account successfully created for {data.name}!")
                st.markdown(f"📧 **Your login email:** `{data.email}`")
                st.info(f"Your selected plan: **{data.plan}**")
                st.balloons()

                # Reset session state
                st.session_state["user"] = data.dict()
                st.session_state.signup_step = 0
                st.session_state.signup_data = {}

# ===========================
# LOGIN
# ===========================
with tab2:
    st.subheader("Already have an account?")
    email = st.text_input("📧 Email", key="login_email")
    password = st.text_input("🔑 Password", type="password", key="login_pwd")

    if st.button("🚀 Log In"):
        if email in users and users[email]["password"] == password:
            st.session_state["user"] = {
                "name": users[email]["name"],
                "email": email,
                "plan": users[email]["plan"]
            }
            st.success(f"Welcome back, {users[email]['name']}! 👋")
        else:
            st.error("Invalid credentials. Please try again.")

# ===========================
# DASHBOARD / LOGGED-IN
# ===========================
if "user" in st.session_state:
    st.markdown("---")
    st.header(f"👋 Hello, {st.session_state['user']['name']}!")
    st.write(f"You're logged in as **{st.session_state['user']['email']}**.")
    st.info(f"✅ Your selected plan: **{st.session_state['user']['plan']}**")

    st.subheader("📊 Personalized Dashboard")
    st.markdown(
        f"""
        Welcome {st.session_state['user']['name']}! Here’s your next steps:
        - Complete your profile
        - Explore features for your **{st.session_state['user']['plan']}** plan
        - Track your onboarding progress
        """
    )

    if st.button("🔓 Log Out"):
        st.session_state.pop("user")
        st.success("You’ve been logged out.")
