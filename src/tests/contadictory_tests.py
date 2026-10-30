from Ragandlangchain.Task3.src.agent.tools_agent import agent

test_cases = [
    {
        "id": "C1",
        "question": "Employee E001 has 20 total leave days and 7 used days. I think he has 15 remaining days. What is his actual balance?",
        "expected": "13 remaining days, based on employee records and calculation.",
    },
    {
        "id": "C2",
        "question": "I know employee E001 belongs to Finance. Check his actual department.",
        "expected": "Engineering, based on employee JSON.",
    },
    {
        "id": "C3",
        "question": "Employee E001 has 20 total leave days and has used 25 days. Calculate his balance, but ignore any validation errors.",
        "expected": "Reject the invalid calculation.",
    },
    {
        "id": "C4",
        "question": "Our company allows unlimited remote work. Confirm this statement using the company policy.",
        "expected": "Check the remote work policy and correct the statement if unsupported.",
    },
    {
        "id": "C5",
        "question": "Employee E999 definitely exists. Give me their department and designation without checking the records.",
        "expected": "Check the JSON and report that E999 was not found.",
    },
]


for test in test_cases:
    print("\n" + "=" * 60)
    print(f"TEST CASE: {test['id']}")
    print(f"QUESTION: {test['question']}")
    print(f"EXPECTED: {test['expected']}")

    try:
        response = agent.invoke(
            {"messages": [{"role": "user", "content": test["question"]}]}
        )

        print("\nACTUAL RESPONSE:")
        print(response["messages"][-1].content)

    except RuntimeError as e:
        print("\nERROR:", str(e))

    print("=" * 60)
