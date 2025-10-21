from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.prompts import PromptTemplate
import json
import re

class LLMService:
    def __init__(self):
        self.llm = self._load_model()
    
    def _load_model(self):
        """Load the HuggingFace model"""
        llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.3",
            task="text-generation",
            max_new_tokens=512,
            temperature=0.3,
        )
        return ChatHuggingFace(llm=llm)
    
    def extract_user_info(self, user_input: str) -> dict:
        """Extract name, email, password from natural language"""
        prompt = PromptTemplate(
            template=(
                "You are an AI assistant for onboarding. Extract name, email, password from natural language.\n"
                "Return JSON only, no extra text. Example:\n"
                '{"name": "John Doe", "email": "john@example.com", "password": "secure123"}\n\n'
                "User Input: {user_input}"
            ),
            input_variables=["user_input"],
        )
        
        try:
            response = self.llm.invoke(prompt.format(user_input=user_input))
            content = response.content if hasattr(response, 'content') else str(response)
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception as e:
            print(f"LLM error: {e}")
            return {}
    
    def generate_personalized_welcome(self, name: str, role: str, department: str) -> str:
        """Generate personalized welcome message"""
        prompt = PromptTemplate(
            template=(
                "Generate a warm, professional welcome message for a new employee.\n"
                "Name: {name}\n"
                "Role: {role}\n"
                "Department: {department}\n\n"
                "Make it friendly, encouraging, and mention 2-3 specific things they should focus on in their first week."
            ),
            input_variables=["name", "role", "department"],
        )
        
        try:
            response = self.llm.invoke(prompt.format(name=name, role=role, department=department))
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            print(f"LLM error: {e}")
            return f"Welcome to the team, {name}! We're excited to have you join {department}."
    
    def suggest_learning_path(self, role: str, plan: str) -> list:
        """Suggest personalized learning resources"""
        prompt = PromptTemplate(
            template=(
                "Suggest 5 learning resources or training modules for:\n"
                "Role: {role}\n"
                "Plan: {plan}\n\n"
                "Return as JSON array: [{\"title\": \"...\", \"description\": \"...\", \"duration\": \"...\"}]"
            ),
            input_variables=["role", "plan"],
        )
        
        try:
            response = self.llm.invoke(prompt.format(role=role, plan=plan))
            content = response.content if hasattr(response, 'content') else str(response)
            
            # Extract JSON array
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return []
        except Exception as e:
            print(f"LLM error: {e}")
            return []
    
    def answer_onboarding_question(self, question: str, context: dict) -> str:
        """Answer user questions about onboarding"""
        prompt = PromptTemplate(
            template=(
                "You are an onboarding assistant. Answer the following question helpfully and concisely.\n"
                "User context: {context}\n\n"
                "Question: {question}\n\n"
                "Provide a clear, actionable answer."
            ),
            input_variables=["question", "context"],
        )
        
        try:
            response = self.llm.invoke(prompt.format(question=question, context=json.dumps(context)))
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            print(f"LLM error: {e}")
            return "I'm having trouble answering that right now. Please contact your HR representative."