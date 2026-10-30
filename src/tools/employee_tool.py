import json
from pathlib import Path

from langchain.tools import tool
from pydantic import BaseModel, Field

EMPLOYEE_FILE = Path(__file__).resolve().parents[1] / "data" / "employees.json"


class EmployeeInput(BaseModel):
    employee_id: str = Field(description="The employee's unique ID, such as E001")


@tool(args_schema=EmployeeInput)
def get_employee_details(employee_id: str) -> str:
    
    """Retrieve fictional employee details using their employee ID.
    Use this tool when the user asks about an employee's name,
    department, designation, manager, or employment information.
    Never guess missing employee information.
    """
    if not EMPLOYEE_FILE.exists():
        return "Error: Employee data file was not found."

    with open(EMPLOYEE_FILE, "r", encoding="utf-8") as file:
        employees = json.load(file)

    employee = employees.get(employee_id.upper())

    if employee is None:
        return f"Employee ID {employee_id} was not found."

    return json.dumps(employee, indent=2)
