from __future__ import annotations

import logging
from pathlib import Path

import yt_dlp

from app.config import settings
from app.models import JobStatus
from app.tasks import update_job, broadcast

logger = logging.getLogger(__name__)


def _progress_hook(job_id: str):
    def hook(d: dict) -> None:
        status = d.get("status")
        if status == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes", 0)
            pct = (downloaded / total * 100) if total else 0.0
            update_job(job_id, status=JobStatus.downloading, progress=round(pct, 1))
            broadcast(job_id)
        elif status == "finished":
            update_job(job_id, status=JobStatus.processing, progress=100.0)
            broadcast(job_id)
    return hook


def run_download(job_id: str, url: str) -> None:
    download_dir: Path = settings.download_dir
    download_dir.mkdir(parents=True, exist_ok=True)

    output_template = str(download_dir / f"{job_id}.%(ext)s")

    ydl_opts: dict = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": output_template,
        "progress_hooks": [_progress_hook(job_id)],
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "video")
            # Find the actual output file
            filename = None
            for ext in ("mp4", "mkv", "webm"):
                candidate = download_dir / f"{job_id}.{ext}"
                if candidate.exists():
                    filename = candidate.name
                    break

            if filename is None:
                raise FileNotFoundError("Download completed but output file not found")

            update_job(
                job_id,
                status=JobStatus.done,
                progress=100.0,
                title=title,
                filename=filename,
            )
            broadcast(job_id)

    except Exception as e:
        logger.exception("Download failed for job %s", job_id)
        update_job(job_id, status=JobStatus.error, error=str(e))
        broadcast(job_id)
