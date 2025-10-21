import json
import os
from datetime import datetime
from typing import Optional, Dict

class AuthManager:
    def __init__(self, user_file: str = "data/users.json"):
        self.user_file = user_file
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.user_file), exist_ok=True)
        if not os.path.exists(self.user_file):
            with open(self.user_file, 'w') as f:
                json.dump({}, f)
    
    def load_users(self) -> Dict:
        """Load all users from file"""
        try:
            with open(self.user_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_users(self, users: Dict):
        """Save users to file"""
        with open(self.user_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def create_user(self, name: str, email: str, password: str, plan: str) -> Dict:
        """Create a new user account"""
        users = self.load_users()
        
        if email in users:
            raise ValueError("User already exists")
        
        user_data = {
            "name": name,
            "email": email,
            "password": password,  # In production, hash this!
            "plan": plan,
            "join_date": datetime.now().strftime("%Y-%m-%d"),
            "onboarding_progress": 0,
            "department": "",
            "role": "",
            "mentor_assigned": False,
            "buddy_assigned": False,
            "checklist_completed": []
        }
        
        users[email] = user_data
        self.save_users(users)
        return user_data
    
    def authenticate(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user credentials"""
        users = self.load_users()
        
        if email in users and users[email]['password'] == password:
            return users[email]
        return None
    
    def update_user(self, email: str, user_data: Dict):
        """Update user information"""
        users = self.load_users()
        if email in users:
            users[email].update(user_data)
            self.save_users(users)
            return True
        return False
    
    def get_user(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        users = self.load_users()
        return users.get(email)
    
    def update_progress(self, email: str, progress: int):
        """Update onboarding progress"""
        users = self.load_users()
        if email in users:
            users[email]['onboarding_progress'] = progress
            self.save_users(users)