"""
app/services/alerts.py — ROM alert checker.
Runs every 2 hours as a background task.
Compares current ROM counts against stored snapshots.
Creates alerts when new ROMs are found for watchlisted devices.
"""
import asyncio
import logging

_log = logging.getLogger("droidify.alerts")


async def check_all_alerts() -> None:
    """Check every watchlisted device for new ROMs. Run as background task."""
    try:
        from app.db import (
            get_all_watchlisted_users, get_rom_snapshot,
            update_rom_snapshot, create_alert,
        )
        from app.scrapers.roms import get_roms_for_device

        pairs = await get_all_watchlisted_users()
        if not pairs:
            return

        _log.info("Checking ROM alerts for %d watchlist entries", len(pairs))
        checked = 0
        alerted = 0

        for entry in pairs:
            user_id  = entry["user_id"]
            codename = entry["codename"]
            try:
                roms      = await get_roms_for_device(codename)
                new_count = len(roms) if roms else 0
                old_count = await get_rom_snapshot(user_id, codename)

                if old_count == -1:
                    # First check — just store baseline, no alert
                    await update_rom_snapshot(user_id, codename, new_count)
                elif new_count > old_count:
                    diff = new_count - old_count
                    msg  = (
                        f"{diff} new ROM build{'s' if diff > 1 else ''} "
                        f"available for {codename}"
                    )
                    await create_alert(user_id, codename, msg, old_count, new_count)
                    await update_rom_snapshot(user_id, codename, new_count)
                    alerted += 1
                else:
                    await update_rom_snapshot(user_id, codename, new_count)

                checked += 1
                # Small delay to avoid hammering scrapers
                await asyncio.sleep(0.1)

            except Exception as e:
                _log.debug("Alert check failed for %s: %s", codename, e)

        _log.info("Alert check done: %d checked, %d alerted", checked, alerted)

    except Exception as e:
        _log.warning("Alert check error: %s", e)


async def run_alert_loop() -> None:
    """Background loop — check every 2 hours."""
    # Wait 5 minutes after startup before first check
    # so cache has time to warm up
    await asyncio.sleep(300)
    while True:
        await check_all_alerts()
        await asyncio.sleep(2 * 60 * 60)  # 2 hours
