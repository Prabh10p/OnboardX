# app/ai/llm_agent.py

import re
import pandas as pd
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from parsers import UserLogin
from vector_stoe import VectorStore

# Load environment variables
load_dotenv()

# Initialize FAISS memory for storing user inputs
memory = VectorStore(dim=384)


def Conversational_agent(user_input: str):
    """
    Conversational AI agent that:
    1. Stores user input in FAISS memory
    2. Extracts structured login info using LLM + Pydantic parser
    """

    # 1️⃣ Store input in FAISS memory
    memory.add_text(user_input)

    # 2️⃣ Initialize LLM endpoint
    llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    task="conversational"
)


    # 3️⃣ Wrap LLM with Chat interface (optional for unified prompt handling)
    model = ChatHuggingFace(llm=llm)

    # 4️⃣ Create prompt
    prompt = PromptTemplate(
        template=(
            "You are an intelligent assistant that extracts structured login data.\n"
            "The user will provide some text, and you must clearly identify their username and password.\n"
            "Input: {user_input}\n\n"
            "Return only structured data following this schema:\n"
            "username: <string>\n"
            "password: <string>"
        ),
        input_variables=["user_input"]
    )

    # 5️⃣ Format prompt with user input
    formatted_prompt = prompt.format(user_input=user_input)

    # 6️⃣ Invoke LLM and normalize raw response
    raw_response = model.invoke(formatted_prompt)

    # HuggingFaceEndpoint with task="text-generation" may return dict, str, or message
    if hasattr(raw_response, "content"):
        raw_response = raw_response.content
    elif isinstance(raw_response, dict) and "generated_text" in raw_response:
        raw_response = raw_response["generated_text"]
    else:
        raw_response = str(raw_response)

    # 7️⃣ Try parsing with Pydantic, else fallback to regex
    try:
        structured_response = UserLogin.model_validate_json(raw_response)
    except Exception:
        username_match = re.search(r"username[:\s]+(\S+)", raw_response, re.IGNORECASE)
        password_match = re.search(r"password[:\s]+(\S+)", raw_response, re.IGNORECASE)

        structured_response = UserLogin(
            username=username_match.group(1) if username_match else None,
            password=password_match.group(1) if password_match else None
        )

    # 8️⃣ Retrieve top 3 similar past inputs from memory
    recent_history = memory.search(user_input, top_k=3)

    return {
        "structured_response": structured_response,
        "recent_history": recent_history,
        "raw_output": raw_response
    }


# ✅ Example usage
if __name__ == "__main__":
    test_input = "Hey, my username is akhil and my password is secure123 and it is good"
    output = Conversational_agent(test_input)
    print("\n🎯 Structured Response:")
    print(output["structured_response"])
    print("\n📚 Recent Similar Inputs from Memory:")
    print(output["recent_history"])
    print("\n🧠 Raw Model Output:")
    print(output["raw_output"])
