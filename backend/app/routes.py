from __future__ import annotations

import asyncio
import json
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from sse_starlette.sse import EventSourceResponse

from app.config import settings
from app.downloader import run_download
from app.models import JobInfo, SubmitRequest
from app.tasks import (
    broadcast,
    create_job,
    get_all_jobs,
    job_info,
    subscribe,
    unsubscribe,
)

router = APIRouter(prefix="/api")

_executor = ThreadPoolExecutor(max_workers=settings.max_concurrent_downloads)


@router.post("/submit")
async def submit_url(req: SubmitRequest) -> dict:
    job_id = create_job(req.url)
    broadcast(job_id)
    loop = asyncio.get_event_loop()
    loop.run_in_executor(_executor, run_download, job_id, req.url)
    return {"job_id": job_id}


@router.get("/jobs")
async def list_jobs() -> list[JobInfo]:
    return [JobInfo(**j) for j in get_all_jobs()]


@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str) -> JobInfo:
    info = job_info(job_id)
    if info is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return info


@router.get("/jobs/{job_id}/download")
async def download_file(job_id: str) -> FileResponse:
    info = job_info(job_id)
    if info is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if info.filename is None:
        raise HTTPException(status_code=400, detail="File not ready")

    path = settings.download_dir / info.filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    download_name = f"{info.title or 'video'}.mp4"
    return FileResponse(
        path=str(path),
        filename=download_name,
        media_type="video/mp4",
    )


@router.get("/events")
async def sse_events():
    queue = subscribe()

    async def event_generator():
        try:
            while True:
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=30)
                    yield {
                        "event": "job_update",
                        "data": json.dumps(data, default=str),
                    }
                except asyncio.TimeoutError:
                    yield {"event": "ping", "data": ""}
        except asyncio.CancelledError:
            pass
        finally:
            unsubscribe(queue)

    return EventSourceResponse(event_generator())
