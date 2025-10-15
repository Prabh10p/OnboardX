# app/ai/parsers.py

from pydantic import BaseModel, Field, constr, EmailStr
from typing import Optional

# ✅ Schema 1: For login input
class UserLogin(BaseModel):
    username: constr(min_length=3, max_length=20) = Field(
        ..., description="Validated username of the individual"
    )
    password: constr(min_length=6) = Field(
        ..., description="Validated password; must be at least 6 characters"
    )


# ✅ Schema 2: For new employee onboarding info
class EmployeeOnboarding(BaseModel):
    full_name: str = Field(..., description="Employee's full legal name")
    email: EmailStr = Field(..., description="Official onboarding email address")
    department: str = Field(..., description="Department where employee will work")
    start_date: Optional[str] = Field(None, description="Tentative start date (YYYY-MM-DD)")


# ✅ Schema 3: For task progress updates
class TaskProgress(BaseModel):
    task_name: str = Field(..., description="The name of the assigned task")
    status: str = Field(..., description="Task status e.g. pending, in_progress, completed")
    remarks: Optional[str] = Field(None, description="Additional comments from the user")
