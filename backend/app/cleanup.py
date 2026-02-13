from __future__ import annotations

import asyncio
import logging
import time

from app.config import settings
from app.tasks import get_all_jobs, remove_job

logger = logging.getLogger(__name__)


async def cleanup_loop() -> None:
    interval = settings.cleanup_interval_minutes * 60
    while True:
        await asyncio.sleep(interval)
        try:
            _cleanup_old_files()
        except Exception:
            logger.exception("Cleanup error")


def _cleanup_old_files() -> None:
    download_dir = settings.download_dir
    if not download_dir.exists():
        return

    max_age = settings.cleanup_interval_minutes * 60
    now = time.time()
    removed = 0

    for f in download_dir.iterdir():
        if f.is_file() and (now - f.stat().st_mtime) > max_age:
            job_id = f.stem
            f.unlink(missing_ok=True)
            remove_job(job_id)
            removed += 1

    if removed:
        logger.info("Cleaned up %d old file(s)", removed)
