from fastapi import APIRouter, Query
from app.scrapers.android_versions import get_android_versions

router = APIRouter()

@router.get("")
async def list_android_versions(
    min_api: int | None = Query(None, description="Minimum API level"),
    status:  str | None = Query(None, description="active | partial | unsupported"),
):
    """
    Full Android version history fetched live from Wikipedia.
    Covers Android 1.0 (2008) through Android 16 / Baklava (2025, May 2026 SPL).
    Source: https://en.wikipedia.org/wiki/Android_version_history
    """
    versions = await get_android_versions()
    if min_api is not None:
        versions = [v for v in versions if v["api_level"] >= min_api]
    if status:
        versions = [v for v in versions if v.get("status") == status]
    return {"total": len(versions), "versions": versions}
