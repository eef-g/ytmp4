from enum import Enum
from pydantic import BaseModel, field_validator
import re


ALLOWED_HOSTS = re.compile(
    r"^https?://(www\.)?"
    r"(youtube\.com|youtu\.be|instagram\.com|tiktok\.com|vm\.tiktok\.com)"
)


class JobStatus(str, Enum):
    pending = "pending"
    downloading = "downloading"
    processing = "processing"
    done = "done"
    error = "error"


class SubmitRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        v = v.strip()
        if not ALLOWED_HOSTS.match(v):
            raise ValueError(
                "URL must be from youtube.com, youtu.be, instagram.com, "
                "tiktok.com, or vm.tiktok.com"
            )
        return v


class JobInfo(BaseModel):
    job_id: str
    url: str
    status: JobStatus
    progress: float = 0.0
    title: str | None = None
    filename: str | None = None
    error: str | None = None
