"""ROM Assistant API — uses Claude via Anthropic API to answer modding questions."""
import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

SYSTEM_PROMPT = """You are the Droidify ROM Assistant — a helpful Android modding expert built into Droidify (https://eliekh05-droidify-hf.hf.space), a free web app that indexes custom ROMs, recoveries, and tools for 946+ Android devices.

Your job:
1. Help users find custom ROMs, recoveries, root tools, and flashing guides for their device
2. Answer questions about Android modding — bootloaders, TWRP, Magisk, KernelSU, Play Integrity, etc.
3. When a user mentions a device, suggest they search for it on Droidify using the device's codename
4. Explain concepts clearly — assume the user may be a beginner

Rules:
- Be concise. Use short paragraphs or bullet points.
- Never recommend anything illegal or potentially harmful
- Always remind users to make a NANDroid backup before flashing
- For Samsung devices, always warn about Knox and Auto Blocker (One UI 6.1.1+)
- If you don't know something specific, say so and suggest checking XDA Developers
- Don't make up ROM names or download links — direct users to search on Droidify
- Format responses in simple HTML: use <strong>, <br>, <ul><li> where helpful
- Keep responses under 200 words unless the question genuinely requires more"""


class AssistantRequest(BaseModel):
    message: str
    history: list[dict] = []


@router.post("")
async def assistant(req: AssistantRequest):
    if not req.message or len(req.message) > 500:
        return JSONResponse({"reply": "Please keep your message under 500 characters."})

    # Build messages for Claude API
    messages = []
    for h in req.history[-8:]:  # last 8 turns for context
        role = h.get("role", "")
        content = h.get("content", "")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})

    # Ensure last message is the current one
    if not messages or messages[-1]["role"] != "user":
        messages.append({"role": "user", "content": req.message})

    try:
        import httpx
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "claude-sonnet-4-6",
                    "max_tokens": 1000,
                    "system": SYSTEM_PROMPT,
                    "messages": messages,
                },
            )
            data = r.json()
            reply = data.get("content", [{}])[0].get("text", "")
            if not reply:
                return JSONResponse({"reply": "I couldn't generate a response. Please try again."})
            return JSONResponse({"reply": reply})
    except Exception as e:
        return JSONResponse({"reply": "Something went wrong on my end. Please try again in a moment."})
