"""Android versions API router."""
from fastapi import APIRouter, Query
from app.scrapers.android_versions import get_android_versions

router = APIRouter()


@router.get("", summary="Android version history")
async def list_android_versions(
    min_api: int | None = Query(None, description="Filter by minimum API level"),
    status:  str | None = Query(None, description="Filter by status: active | unsupported | preview"),
):
    """
    Full Android version history — every version from 1.0 to the latest
    including all subversions, API levels, codenames, and release dates.
    Data is hardcoded from official Android SDK documentation and
    verified against source.android.com build numbers.
    New versions are added as Google announces them.
    """
    versions = await get_android_versions()
    if min_api is not None:
        versions = [v for v in versions if (v.get("api_level") or 0) >= min_api]
    if status:
        versions = [v for v in versions if v.get("status") == status]
    return {"total": len(versions), "versions": versions}


@router.get("/{version_number}", summary="Single Android version")
async def get_android_version(version_number: str):
    """
    Look up a specific Android version by version number.
    Examples: 14, 13, 12L, 11, 10, 9, 4.4, 2.3.7
    """
    versions = await get_android_versions()
    match = next(
        (v for v in versions if v.get("version_number", "").lower() == version_number.lower()),
        None
    )
    if not match:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Android version {version_number!r} not found")
    return match
