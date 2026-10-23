"""ROM Assistant API — Claude with real Droidify data via tool use."""
import httpx
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

SYSTEM_PROMPT = """You are the Droidify ROM Assistant — an Android modding expert with live access to Droidify's device database.

Droidify indexes custom ROMs, recoveries, root tools, and guides for 946+ Android devices in real time from 20+ sources including LineageOS, OrangeFox, TWRP, GrapheneOS, crDroid, MatrixxOS, /e/OS, CalyxOS, SourceForge and more.

You have tools to query Droidify's live data. Always use them when a user asks about a specific device, ROM, or recovery — never guess or make up data.

Rules:
- Use search_device first whenever a user mentions a device name or codename
- Use get_roms and get_recoveries to show what is actually available
- If search returns nothing, say so honestly — do not invent ROM names
- Always remind users to make a NANDroid backup before flashing
- For Samsung: warn about Knox (permanent trip on bootloader unlock) and Auto Blocker (One UI 6.1.1+ blocks sideloading by default)
- For GrapheneOS: only supports Pixel devices
- Keep responses concise and use bullet points for lists
- Format with simple HTML: <strong>, <br>, <ul><li>
- If you do not know something, say so and suggest XDA Developers"""

TOOLS = [
    {
        "name": "search_device",
        "description": "Search for Android devices by name, codename, or manufacturer. Use this first when a user mentions any device.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Device name, codename, or manufacturer e.g. 'Poco F1', 'beryllium', 'Samsung'"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_roms",
        "description": "Get available custom ROMs for a specific device codename.",
        "input_schema": {
            "type": "object",
            "properties": {
                "codename": {"type": "string", "description": "Exact device codename e.g. 'beryllium'"}
            },
            "required": ["codename"]
        }
    },
    {
        "name": "get_recoveries",
        "description": "Get available custom recoveries (TWRP, OrangeFox etc) for a specific device codename.",
        "input_schema": {
            "type": "object",
            "properties": {
                "codename": {"type": "string", "description": "Exact device codename e.g. 'beryllium'"}
            },
            "required": ["codename"]
        }
    },
    {
        "name": "get_guides",
        "description": "Get flashing guides for a specific device codename.",
        "input_schema": {
            "type": "object",
            "properties": {
                "codename": {"type": "string", "description": "Exact device codename e.g. 'beryllium'"}
            },
            "required": ["codename"]
        }
    },
    {
        "name": "get_android_versions",
        "description": "Get the full Android version history with API levels, codenames, and support status.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

BASE_URL = "http://localhost:7860"


async def call_tool(name: str, inputs: dict) -> str:
    try:
        async with httpx.AsyncClient(timeout=10, base_url=BASE_URL) as c:
            if name == "search_device":
                r = await c.get("/api/devices", params={"q": inputs["query"], "limit": 5})
                data = r.json()
                devices = data.get("devices", [])
                if not devices:
                    return f"No devices found for '{inputs['query']}'."
                lines = [
                    f"- {d.get('model_name','?')} (codename: {d.get('codename','?')}, OEM: {d.get('oem','?')})"
                    for d in devices
                ]
                return f"Found {data.get('total',0)} devices:\n" + "\n".join(lines)

            elif name == "get_roms":
                r = await c.get("/api/roms", params={"q": inputs["codename"], "limit": 10})
                data = r.json()
                roms = data.get("roms", data.get("results", []))
                if not roms:
                    return f"No ROMs found for '{inputs['codename']}' in the Droidify index."
                lines = [
                    f"- {rom.get('rom_name','?')} (Android {rom.get('android','?')}, {rom.get('type','?')}) — maintainer: {rom.get('maintainer','?')}"
                    for rom in roms[:8]
                ]
                return f"Found {data.get('total', len(roms))} ROM(s) for {inputs['codename']}:\n" + "\n".join(lines)

            elif name == "get_recoveries":
                r = await c.get("/api/recoveries", params={"q": inputs["codename"], "limit": 5})
                data = r.json()
                recs = data.get("recoveries", data.get("results", []))
                if not recs:
                    return f"No recoveries found for '{inputs['codename']}' in the Droidify index."
                lines = [f"- {rec.get('name','?')} {rec.get('version','')}" for rec in recs]
                return f"Found {len(recs)} recovery build(s) for {inputs['codename']}:\n" + "\n".join(lines)

            elif name == "get_guides":
                r = await c.get(f"/api/guides/{inputs['codename']}")
                data = r.json()
                guides = data.get("guides", [])
                if not guides:
                    return f"No device-specific guides for '{inputs['codename']}'."
                lines = [f"- {g.get('title','?')} ({g.get('guide_type','?')})" for g in guides]
                return "Available guides:\n" + "\n".join(lines)

            elif name == "get_android_versions":
                r = await c.get("/api/android-versions")
                data = r.json()
                versions = data if isinstance(data, list) else data.get("versions", [])
                active = [v for v in versions if v.get("status") == "active"]
                lines = [
                    f"- Android {v.get('version_number','?')} ({v.get('codename','?')}, API {v.get('api_level','?')}) — {v.get('status','?')}"
                    for v in active
                ]
                return f"Active Android versions ({len(active)}):\n" + "\n".join(lines)

    except Exception as e:
        return f"Error calling {name}: {str(e)}"
    return "Unknown tool."


class AssistantRequest(BaseModel):
    message: str
    history: list[dict] = []


@router.post("")
async def assistant(req: AssistantRequest):
    if not req.message or len(req.message) > 500:
        return JSONResponse({"reply": "Please keep your message under 500 characters."})

    messages = []
    for h in req.history[-8:]:
        role = h.get("role", "")
        content = h.get("content", "")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})

    if not messages or messages[-1]["role"] != "user":
        messages.append({"role": "user", "content": req.message})
    elif messages[-1]["content"] != req.message:
        messages.append({"role": "user", "content": req.message})

    for _ in range(5):
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"Content-Type": "application/json"},
                    json={
                        "model": "claude-sonnet-4-6",
                        "max_tokens": 1000,
                        "system": SYSTEM_PROMPT,
                        "tools": TOOLS,
                        "messages": messages,
                    },
                )
                data = r.json()
        except Exception:
            return JSONResponse({"reply": "Connection error. Please try again."})

        stop_reason = data.get("stop_reason")
        content_blocks = data.get("content", [])

        if stop_reason == "end_turn":
            text = next((b.get("text", "") for b in content_blocks if b.get("type") == "text"), "")
            return JSONResponse({"reply": text or "I could not generate a response."})

        elif stop_reason == "tool_use":
            tool_results = []
            for block in content_blocks:
                if block.get("type") == "tool_use":
                    result = await call_tool(block.get("name", ""), block.get("input", {}))
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.get("id", ""),
                        "content": result
                    })
            messages.append({"role": "assistant", "content": content_blocks})
            messages.append({"role": "user", "content": tool_results})
        else:
            break

    return JSONResponse({"reply": "Something went wrong. Please try again."})
