from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agent.agent import agent


router = APIRouter()


class AskRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_agent(request: AskRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question,
                    }
                ]
            }
        )

        messages = result.get("messages", [])

        if not messages:
            raise RuntimeError("Agent returned no messages.")

        final_message = messages[-1]

        answer = final_message.content

        tools_used = []

        for message in messages:
            tool_calls = getattr(message, "tool_calls", [])

            for tool_call in tool_calls:
                tool_name = tool_call.get("name")

                if tool_name and tool_name not in tools_used:
                    tools_used.append(tool_name)

        return {
            "question": question,
            "answer": answer,
            "tools_used": tools_used,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {exc}",
        ) from exc