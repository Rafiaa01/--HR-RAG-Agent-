from fastapi import HTTPException
from src.agent.tools_agent import agent
from src.config import ChatRequest, ChatResponse


def chat(request: ChatRequest):
    try:
        response = agent.invoke(
            {"messages": [{"role": "user", "content": request.message}]}
        )

        answer = response["messages"][-1].content

        return ChatResponse(answer=answer)

    except Exception:  # noqa: BLE001
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request."
        )