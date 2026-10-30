from tools.leave_tool import calculate_leave_balance

result = calculate_leave_balance.invoke({"total_days": 20, "used_days": 7})

print(result)
