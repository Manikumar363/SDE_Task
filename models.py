from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Employee(BaseModel):
    employee_id: str = Field(..., description="Unique employee ID")
    name: str
    department: str
    salary: float
    joining_date: date
    skills: List[str]

class UpdateEmployee(BaseModel):
    name: Optional[str]
    department: Optional[str]
    salary: Optional[float]
    joining_date: Optional[date]
    skills: Optional[List[str]]
