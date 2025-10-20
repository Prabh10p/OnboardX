import streamlit as st
from pydantic import BaseModel
from langchain_huggingface import ChatHuggingFace
from langchain.prompts import ChatPromptTemplate
import json
import time

# ==============================================
# 1️⃣ Define the structured schema
# ==============================================
class UserOnboarding(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None

# ==============================================
# 2️⃣ Initialize Hugging Face LLM
# ==============================================
@st.cache_resource
def load_model():
    return ChatHuggingFace.from_model_id(
        model_id="mistralai/Mistral-7B-Instruct-v0.3",  # robust and lightweight
        task="text-generation",
        model_kwargs={"temperature": 0.3, "max_new_tokens": 256}
    )

model = load_model()

# ==============================================
# 3️⃣ Prompt Template
# ==============================================
prompt = ChatPromptTemplate.from_template("""
You are an intelligent onboarding assistant.
Extract the user's name, email, and password from their message.
Return only valid JSON matching this schema:
{name: string, email: string, password: string}

User input: {input}
""")

# ==============================================
# 4️⃣ Streamlit UI
# ==============================================
st.set_page_config(page_title="Conversational Onboarding Assistant", page_icon="🤖")
st.title("🤖 Conversational Onboarding Assistant")

st.markdown("""
Welcome! This AI assistant extracts structured onboarding information  
from natural language input — no forms needed.
""")

user_input = st.text_area(
    "Enter your onboarding message:",
    placeholder="e.g. Hey, my name is Akhil, email akhil@gmail.com, and password is secure123",
)

if "structured_data" not in st.session_state:
    st.session_state.structured_data = None

# ==============================================
# 5️⃣ Process Input
# ==============================================
if st.button("Extract Information"):
    if user_input.strip():
        st.info("🔍 Analyzing input with LLM...")
        formatted_prompt = prompt.format(input=user_input)

        try:
            response = model.invoke(formatted_prompt)
            raw_output = response.content.strip()
            st.subheader("🧠 Raw Model Output")
            st.code(raw_output, language="json")

            try:
                structured = UserOnboarding.model_validate_json(raw_output)
                st.session_state.structured_data = structured
                st.success("✅ Structured Onboarding Data Extracted")
                st.json(structured.dict())
            except Exception:
                st.warning("⚠️ Could not parse valid JSON. Please check output formatting.")

        except Exception as e:
            st.error(f"Error while calling model: {e}")
    else:
        st.warning("Please enter some onboarding text.")

# ==============================================
# 6️⃣ Simulated Account Creation
# ==============================================
if st.session_state.structured_data:
    st.markdown("---")
    st.subheader("🚀 Simulate Account Creation")

    if st.button("Create Account"):
        with st.spinner("Creating account..."):
            time.sleep(2)
            st.success(f"🎉 Account successfully created for {st.session_state.structured_data.name or 'User'}!")
            st.balloons()

# ==============================================
# Footer
# ==============================================
st.markdown("---")
st.caption("Prototype by Prabhjot Singh — Conversational Onboarding Assistant Demo (2025)")
