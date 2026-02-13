# ytmp4

![Version](https://img.shields.io/badge/version-1.0.0-blue?style=flat-square)
![Build](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)
![Docker](https://img.shields.io/badge/docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)
![Vibe Coded](https://img.shields.io/badge/vibe%20coded-%F0%9F%A4%99-ff69b4?style=flat-square)
![License](https://img.shields.io/badge/license-personal-lightgrey?style=flat-square)

![Svelte](https://img.shields.io/badge/Svelte_5-FF3E00?style=flat-square&logo=svelte&logoColor=white)
![Vite](https://img.shields.io/badge/Vite_6-646CFF?style=flat-square&logo=vite&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![yt--dlp](https://img.shields.io/badge/yt--dlp-FF0000?style=flat-square&logo=youtube&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white)

A simple, ad-free, self-hosted short-form video downloader for YouTube, Instagram, and TikTok.

> This app was vibe coded with manual tweaks and prompt engineering to get the desired result — no bloat, no ads, just paste a link and download.

## Quick Start

### Deploy on any machine (no source code needed)

```bash
curl -O https://raw.githubusercontent.com/eef-g/ytmp4/master/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

The script installs Docker if missing, pulls the pre-built images from GHCR, and starts the app.

### Build from source

```bash
git clone https://github.com/eef-g/ytmp4.git
cd ytmp4
docker compose up --build
```

Open [http://localhost:8080](http://localhost:8080), paste a link, and download.

## Supported Platforms

| Platform | Example URLs |
|----------|-------------|
| YouTube | `youtube.com/watch?v=...`, `youtu.be/...`, `youtube.com/shorts/...` |
| Instagram | `instagram.com/reel/...`, `instagram.com/p/...` |
| TikTok | `tiktok.com/@user/video/...` |

## Configuration

Copy `.env.example` and adjust as needed:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Frontend port |
| `CLEANUP_INTERVAL_MINUTES` | `60` | Auto-delete downloaded files after this interval |
| `MAX_CONCURRENT_DOWNLOADS` | `3` | Max parallel downloads |

## How It Works

1. Paste a video URL into the web UI
2. Backend queues a download job using yt-dlp
3. Real-time progress streams to the browser via SSE
4. Download the MP4 when it's ready

Files are automatically cleaned up on a configurable interval so the server doesn't fill up.
