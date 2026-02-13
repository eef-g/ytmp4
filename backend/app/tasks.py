from __future__ import annotations

import uuid
from typing import Any

from app.models import JobInfo, JobStatus

_jobs: dict[str, dict[str, Any]] = {}

# SSE subscribers: list of asyncio.Queue
_subscribers: list[Any] = []


def create_job(url: str) -> str:
    job_id = uuid.uuid4().hex[:12]
    _jobs[job_id] = {
        "job_id": job_id,
        "url": url,
        "status": JobStatus.pending,
        "progress": 0.0,
        "title": None,
        "filename": None,
        "error": None,
    }
    return job_id


def get_job(job_id: str) -> dict[str, Any] | None:
    return _jobs.get(job_id)


def get_all_jobs() -> list[dict[str, Any]]:
    return list(_jobs.values())


def update_job(job_id: str, **kwargs: Any) -> None:
    if job_id in _jobs:
        _jobs[job_id].update(kwargs)


def remove_job(job_id: str) -> None:
    _jobs.pop(job_id, None)


def job_info(job_id: str) -> JobInfo | None:
    data = get_job(job_id)
    if data is None:
        return None
    return JobInfo(**data)


def subscribe() -> Any:
    import asyncio
    q: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
    _subscribers.append(q)
    return q


def unsubscribe(q: Any) -> None:
    try:
        _subscribers.remove(q)
    except ValueError:
        pass


def broadcast(job_id: str) -> None:
    data = get_job(job_id)
    if data is None:
        return
    for q in list(_subscribers):
        try:
            q.put_nowait(data)
        except Exception:
            pass
