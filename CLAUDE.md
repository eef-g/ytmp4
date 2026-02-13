# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ytmp4 is a web app for downloading videos from YouTube, Instagram, and TikTok. It has a Svelte frontend and a FastAPI (Python) backend that uses yt-dlp for downloading.

## Development Commands

### Frontend (from `frontend/`)
- `npm install` — install dependencies
- `npm run dev` — start dev server (proxies `/api` to backend at localhost:8000)
- `npm run build` — production build to `dist/`

### Backend (from `backend/`)
- `pip install -r requirements.txt` — install dependencies
- `uvicorn app.main:app --host 0.0.0.0 --port 8000` — run the server

### Docker (from project root)
- `docker-compose up --build` — run full stack (frontend on 8080, backend on 8000)

## Architecture

**Frontend** (`frontend/src/`): Svelte 5 SPA with Vite. State is managed via Svelte stores in `lib/stores.js`. API calls are centralized in `lib/api.js`. Real-time job updates use Server-Sent Events (SSE) via EventSource.

**Backend** (`backend/app/`): FastAPI async app. Downloads run in a ThreadPoolExecutor (max concurrency configured via env). Jobs are stored in-memory (dict in `tasks.py`) with a pub/sub pattern for SSE notifications via asyncio.Queue. An async cleanup loop (`cleanup.py`) deletes old files on a configurable interval.

**Job status flow**: `pending → downloading → processing → done | error`

**API endpoints**:
- `POST /api/submit` — submit a URL for download
- `GET /api/jobs` — list all jobs
- `GET /api/jobs/{job_id}` — single job status
- `GET /api/jobs/{job_id}/download` — download completed file
- `GET /api/events` — SSE stream for real-time updates

## Configuration

Environment variables (prefixed `YTMP4_` in backend `config.py`):
- `PORT` (default 8080) — frontend exposed port
- `CLEANUP_INTERVAL_MINUTES` (default 60)
- `MAX_CONCURRENT_DOWNLOADS` (default 3)

See `.env.example` for the template.

## Key Conventions

- URL validation uses a regex whitelist in `backend/app/models.py` (YouTube, Instagram, TikTok patterns)
- Frontend uses CSS variables for dark theme with purple accent (#7c3aed), defined in `app.css`
- Nginx (`frontend/nginx.conf`) handles SPA routing fallback and proxies `/api` to the backend with SSE support
- Backend disables yt-dlp's own logging; progress is tracked via yt-dlp hooks in `downloader.py`
