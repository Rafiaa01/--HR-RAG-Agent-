from langchain.tools import tool
from pydantic import BaseModel, Field, model_validator


class LeaveInput(BaseModel):
    total_days: int = Field(
        ge=0, description="Total annual leave days allocated to the employee"
    )

    used_days: int = Field(ge=0, description="Number of annual leave days already used")

    @model_validator(mode="after")
    def validate_leave(self):
        if self.used_days > self.total_days:
            raise ValueError("Used leave days cannot exceed total leave days.")
        return self


@tool(args_schema=LeaveInput)
def calculate_leave_balance(total_days: int, used_days: int) -> str:
    """Calculate the remaining annual leave balance.
    Use this tool when the user asks how many leave days remain.
    Requires total allocated leave days and used leave days.
    """
    remaining_days = total_days - used_days

    return (
        f"Total leave days: {total_days}\n"
        f"Used leave days: {used_days}\n"
        f"Remaining leave days: {remaining_days}"
    )
