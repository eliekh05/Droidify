import re
from fastapi import APIRouter, Query
from app.scrapers.tools import get_tools

router = APIRouter()


@router.get("")
async def list_tools(
    category: str | None = Query(None, description="root | xposed | flashing | recovery"),
    status:   str | None = Query(None, description="active | discontinued"),
):
    """
    Root tools, recoveries, and flashing utilities with live version data.

    GitHub-backed tools (Magisk, KernelSU, APatch, LSPosed, Heimdall, Fastboot Enhance)
    fetch their latest release from the GitHub API (unauthenticated, no key needed).
    Other tools link to their official pages.
    """
    tools = await get_tools(category=category)
    if status:
        tools = [t for t in tools if t.get("status") == status]
    categories = list(dict.fromkeys(t["category"] for t in tools))
    return {"total": len(tools), "categories": categories, "tools": tools}
