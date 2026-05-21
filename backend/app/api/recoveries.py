import re
from fastapi import APIRouter, HTTPException, Query
from app.scrapers.recoveries import get_recoveries

router = APIRouter()


@router.get("")
async def list_recoveries(
    q:            str | None = Query(None, description="Search by codename or model"),
    recovery:     str | None = Query(None, description="TWRP | OrangeFox"),
    manufacturer: str | None = Query(None, description="Filter by manufacturer"),
    limit:        int = Query(50, ge=1, le=500),
    offset:       int = Query(0, ge=0),
):
    """
    Recovery-supported devices from TWRP (896 devices) and OrangeFox (159 devices).
    Both sources are free and require no authentication.
    """
    return await get_recoveries(
        q=q,
        recovery=recovery,
        manufacturer=manufacturer,
        limit=limit,
        offset=offset,
    )
