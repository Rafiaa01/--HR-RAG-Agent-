from Ragandlangchain.Task3.src.agent.tools_agent import agent

test_cases = [
    {"id": "P1", "question": "What is the annual leave policy?"},
    {
        "id": "P2",
        "question": "What is the department and designation of employee E001?",
    },
    {
        "id": "P3",
        "question": "Calculate the remaining leave for an employee with 20 total days and 7 used days.",
    },
    {
        "id": "P4",
        "question": "What is the department, designation, and remaining leave balance of employee E001?",
    },
    {"id": "P5", "question": "What is the company's remote work policy?"},
]


for test in test_cases:
    print("\n" + "=" * 60)
    print(f"TEST CASE: {test['id']}")
    print(f"QUESTION: {test['question']}")

    response = agent.invoke(
        {"messages": [{"role": "user", "content": test["question"]}]}
    )

    print("\nAGENT RESPONSE:")
    print(response["messages"][-1].content)
    print("=" * 60)
