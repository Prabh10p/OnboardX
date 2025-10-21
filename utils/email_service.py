import os
import re
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.api_key = os.getenv("SENDGRID_API_KEY")
        self.from_email = os.getenv("EMAIL_FROM")
        self.sg = SendGridAPIClient(self.api_key) if self.api_key else None
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
    
    def send_welcome_email(self, to_email: str, name: str, plan: str) -> bool:
        """Send welcome email to new user"""
        if not self.is_valid_email(to_email) or not self.sg:
            return False
        
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject="🎉 Welcome to OnboardX!",
                html_content=f"""
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2 style="color: #667eea;">Welcome to OnboardX, {name}! 🚀</h2>
                        <p>We're thrilled to have you join our platform!</p>
                        
                        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <h3 style="color: #333; margin-top: 0;">Your Account Details:</h3>
                            <p><strong>Plan:</strong> {plan}</p>
                            <p><strong>Email:</strong> {to_email}</p>
                        </div>
                        
                        <h3>What's Next?</h3>
                        <ul style="line-height: 1.8;">
                            <li>✅ Complete your onboarding checklist</li>
                            <li>👥 Meet your mentor and buddy</li>
                            <li>📚 Access training resources</li>
                            <li>🎯 Set your first 30-day goals</li>
                        </ul>
                        
                        <p style="margin-top: 30px;">
                            <a href="#" style="background: #667eea; color: white; padding: 12px 24px; 
                                text-decoration: none; border-radius: 5px; display: inline-block;">
                                Get Started
                            </a>
                        </p>
                        
                        <p style="color: #666; font-size: 14px; margin-top: 30px;">
                            Best regards,<br>
                            The OnboardX Team
                        </p>
                    </div>
                """
            )
            self.sg.send(message)
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    def send_checklist_reminder(self, to_email: str, name: str, pending_tasks: list) -> bool:
        """Send reminder for pending checklist items"""
        if not self.is_valid_email(to_email) or not self.sg:
            return False
        
        try:
            tasks_html = "".join([f"<li>{task}</li>" for task in pending_tasks])
            
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject="📋 Onboarding Checklist Reminder",
                html_content=f"""
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2 style="color: #667eea;">Hi {name}! 👋</h2>
                        <p>You have pending items on your onboarding checklist:</p>
                        
                        <div style="background: #fff3cd; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <h3 style="color: #856404; margin-top: 0;">Pending Tasks:</h3>
                            <ul style="color: #856404;">
                                {tasks_html}
                            </ul>
                        </div>
                        
                        <p>Complete these tasks to make the most of your onboarding experience!</p>
                        
                        <p style="color: #666; font-size: 14px; margin-top: 30px;">
                            Best regards,<br>
                            The OnboardX Team
                        </p>
                    </div>
                """
            )
            self.sg.send(message)
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    def send_mentor_introduction(self, to_email: str, mentee_name: str, mentor_name: str, mentor_email: str) -> bool:
        """Send mentor introduction email"""
        if not self.is_valid_email(to_email) or not self.sg:
            return False
        
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject="👥 Meet Your Onboarding Mentor!",
                html_content=f"""
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2 style="color: #667eea;">Hi {mentee_name}! 🤝</h2>
                        <p>We've assigned you a mentor to help with your onboarding journey!</p>
                        
                        <div style="background: #e7f3ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <h3 style="color: #004085; margin-top: 0;">Your Mentor:</h3>
                            <p><strong>Name:</strong> {mentor_name}</p>
                            <p><strong>Email:</strong> {mentor_email}</p>
                        </div>
                        
                        <p>Feel free to reach out to your mentor with any questions or concerns!</p>
                        
                        <p style="color: #666; font-size: 14px; margin-top: 30px;">
                            Best regards,<br>
                            The OnboardX Team
                        </p>
                    </div>
                """
            )
            self.sg.send(message)
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False