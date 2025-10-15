# app/ai/llm_agent.py

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
        repo_id="google/gemma-2b-it",  # lighter, conversational model
        task="conversational"
    )

    # 3️⃣ Wrap LLM with Chat interface
    model = ChatHuggingFace(llm=llm)

    # 4️⃣ Enable structured output parsing via Pydantic schema
    structured_model = model.with_structured_output(UserLogin)

    # 5️⃣ Create a consistent prompt
    prompt = PromptTemplate(
        template=(
            "You are an intelligent assistant that extracts structured login data.\n"
            "User will provide some text, and you must identify their username and password clearly.\n"
            "Input: {user_input}\n\n"
            "Return only structured data following this schema:\n"
            "username: <string>\n"
            "password: <string>"
        ),
        input_variables=["user_input"]
    )

    # 6️⃣ Format prompt with user input
    formatted_prompt = prompt.format(user_input=user_input)

    # 7️⃣ Invoke structured LLM model
    response = structured_model.invoke(formatted_prompt)

    # 8️⃣ Optional: retrieve top 3 similar past inputs from memory for debugging or context
    recent_history = memory.search(user_input, top_k=3)

    return {
        "structured_response": response,
        "recent_history": recent_history
    }


# ✅ Example usage
if __name__ == "__main__":
    test_input = "Hey, my username is akhil and my password is secure123"
    output = Conversational_agent(test_input)
    print("\n🎯 Structured Response:")
    print(output["structured_response"])
    print("\n📚 Recent Similar Inputs from Memory:")
    print(output["recent_history"])
