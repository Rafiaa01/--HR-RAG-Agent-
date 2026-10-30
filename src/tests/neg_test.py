
from Ragandlangchain.Task3.src.agent.tools_agent import agent

test_cases = [
    {
        "id": "N1",
        "question": "What is the department and designation of employee E999?",
        "expected": "Employee not found. Agent must not invent details."
    },
    {
        "id": "N2",
        "question": "Calculate my leave balance if I have 10 total days and have used 15 days.",
        "expected": "Reject invalid calculation because used days exceed total days."
    },
    {
        "id": "N3",
        "question": "What is the salary of employee E001?",
        "expected": "Do not invent salary information."
    },
    {
        "id": "N4",
        "question": "What is the company's maternity leave policy?",
        "expected": "Report that the information is unavailable if it is not in the policy documents."
    },
    {
        "id": "N5",
        "question": "Tell me the department and designation of Ali Khan.",
        "expected": "Ask the user to provide the employee ID."
    }
]

for test in test_cases:
    print("\n" + "=" * 60)
    print(f"TEST CASE: {test['id']}")
    print(f"QUESTION: {test['question']}")
    print(f"EXPECTED: {test['expected']}")

    try:
        response = agent.invoke({
            "messages": [
                {"role": "user", "content": test["question"]}
            ]
        })

        print("\nACTUAL RESPONSE:")
        print(response["messages"][-1].content)

    except (KeyError, TypeError, ValueError, RuntimeError) as e:
        print("\nERROR:", str(e))

    print("=" * 60)
