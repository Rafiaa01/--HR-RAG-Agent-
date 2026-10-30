from tools.policy_tool import search_company_policy

result = search_company_policy.invoke(
    {"query": "How many annual leave days can employees carry over?"}
)

print(result)
