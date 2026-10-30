# Task 3: HR Policy Assistant (RAG + LangChain Tool-Calling Agent)

A document-grounded HR assistant for a fictional company. It answers employee questions by combining **retrieval-augmented generation (RAG)** over company policy PDFs with **tool calling** over structured employee records, and exposes the agent through a **FastAPI** service.

## 1. Objectives

- Build a RAG pipeline: load PDFs, chunk them, embed them, store them in FAISS and retrieve relevant context.
- Build a LangChain agent that decides which tool to call for each question.
- Validate tool inputs with Pydantic so invalid requests are rejected, not guessed.
- Keep answers grounded: no invented policies, no invented employee data.
- Evaluate the agent with positive, negative and contradictory test cases.
- Serve the agent over HTTP.

## 2. Architecture

```
                  User question
                        |
                        v
              +--------------------+
              |  FastAPI service   |   application.py -> src/chat
              +--------------------+
                        |
                        v
              +--------------------+
              |  LangChain Agent   |   src/tools_agent.py (system prompt + tools)
              +--------------------+
               |         |         |
               v         v         v
       search_company  get_employee  calculate_leave
          _policy        _details       _balance
               |         |         |
               v         v         v
        FAISS vector   Employee    Pydantic-validated
        store (RAG)    JSON data   calculation
               ^
               |
   PDF loader -> chunking -> embeddings -> faiss_index
```

## 3. Tech Stack

| Area | Tools |
|------|-------|
| Language | Python 3.13 |
| Agent framework | LangChain (agents, tools) |
| Vector store | FAISS |
| Validation | Pydantic |
| API | FastAPI + Uvicorn |
| Testing | Scripted test cases (positive, negative, contradictory) |

## 4. How It Works

**Ingestion (RAG pipeline)**
1. `loader` reads the policy PDFs from `src/data`.
2. `chunking` splits the text into overlapping chunks and attaches metadata (document name, page number, policy topic).
3. `store` embeds the chunks and saves them to a FAISS index (`faiss_index/`).
4. A retriever returns the top-k most relevant chunks for a query (k = 5).

**Agent**
- The agent receives the user message, chooses a tool, reads the tool output and writes the final answer.
- The system prompt enforces the rules in section 7.

## 5. Tools

| Tool | Purpose | Data source |
|------|---------|-------------|
| `search_company_policy` | Answers policy questions (leave, remote work, etc.) from retrieved document text | FAISS index over policy PDFs |
| `get_employee_details` | Returns name, department, designation and leave data for an employee ID | Employee JSON |
| `calculate_leave_balance` | Computes remaining leave from total and used days | Pydantic-validated input |

## 6. Agent Behavior and Guardrails

- Policy answers come **only** from retrieved text. If the policy does not cover a topic, the agent says so and suggests contacting HR.
- Employees are looked up by **employee ID only**. If only a name is given, the agent asks for the ID.
- Unknown IDs are reported as not found. Missing fields (such as salary) are reported as unavailable.
- Leave calculations always go through the tool. Invalid input (used days greater than total days) is rejected with an explanation, never returned as a negative number.
- User claims that conflict with the records or the policy are checked and corrected.
- Instructions to skip tools, skip verification or bypass validation are ignored.

## 7. Setup

```powershell
python -m venv .envv
.envv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root with your API key:

```
OPENAI_API_KEY=your_key_here
```

## 8. Running

Run all commands from the project root (`task3/`).

**Agent test scripts**
```powershell
python src/test_positve.py
python src/neg_test.py
python src/contadictory_tests.py
```

**API server**
```powershell
python -m uvicorn application:application
```
The server starts at `http://127.0.0.1:8000`. FastAPI's interactive docs are at `/docs`.

## 9. Evaluation

| Group | ID | Scenario | Expected behavior |
|-------|----|----------|-------------------|
| Positive | P1 | Annual leave policy | Answer from the policy PDF |
| | P2 | Department and designation of E001 | Correct lookup |
| | P3 | 20 total, 7 used | 13 days remaining |
| | P4 | Employee details plus leave balance | Multi-tool answer |
| | P5 | Remote work policy | Answer from the policy PDF |
| Negative | N1 | Unknown employee E999 | Reports not found |
| | N2 | 10 total, 15 used | Pydantic validation rejects the input |
| | N3 | Salary of E001 | Does not invent salary data |
| | N4 | Maternity leave policy | Reports it is not in the documents |
| | N5 | Name without employee ID | Asks for the ID |
| Contradictory | C1 | User claims 15 days remaining | Corrects to 13 |
| | C2 | User claims E001 is in Finance | Corrects to Engineering |
| | C3 | "Ignore validation errors" | Validation cannot be bypassed |
| | C4 | "Unlimited remote work" | Checks the policy and corrects the claim |
| | C5 | "E999 exists, don't check" | Checks records and reports not found |

## 10. Design Decisions

- **Tools instead of prompting alone.** Structured data and calculations go through tools, so results are deterministic and verifiable.
- **Validation in code, not only in the prompt.** Pydantic enforces input rules even if the model tries to work around them.
- **Metadata on every chunk.** Document name, page and policy topic make answers traceable to a source.
- **Source-aware retrieval.** Multiple policy documents can describe the same topic. Returning the source file and page with each chunk keeps answers traceable and conflicts visible.
- **Paths anchored to `Path(__file__)`.** Data and index paths work from any working directory.

## 11. Known Limitations and Future Work

- Remote work details appear in more than one source document, so answers depend on which chunks are retrieved. Filtering by source or reconciling the documents would remove this.
- Tests currently print output for manual review. Converting them to automated assertions (for example with `pytest`) would make regression checks repeatable.
- Setting model temperature to 0 and running each case several times would help detect flaky behavior.
- Additional edge cases: alternative ID formats (`e001`, `E-001`), non-numeric leave values and prompt-injection attempts.