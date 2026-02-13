#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────
# ytmp4 deploy script for Ubuntu Server
# Installs Docker if needed, pulls GHCR images & runs
# ──────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEPLOY_DIR="${YTMP4_DIR:-$SCRIPT_DIR}"

echo "==> ytmp4 deployment starting..."
echo "    Deploy directory: $DEPLOY_DIR"

# ── 1. Install Docker & Docker Compose if missing ──

if ! command -v docker &>/dev/null; then
    echo "==> Docker not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl gnupg

    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Let current user run docker without sudo
    sudo usermod -aG docker "$USER"
    echo "==> Docker installed. You may need to log out and back in for group changes."
else
    echo "==> Docker already installed."
fi

# ── 2. Create deploy directory and docker-compose.yml ──

mkdir -p "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

if [ ! -f "$DEPLOY_DIR/docker-compose.yml" ]; then
    echo "==> Creating docker-compose.yml with GHCR images..."
    cat > "$DEPLOY_DIR/docker-compose.yml" <<'COMPOSE'
services:
  backend:
    image: ghcr.io/eef-g/ytmp4-backend:latest
    environment:
      - YTMP4_DOWNLOAD_DIR=/app/downloads
      - YTMP4_CLEANUP_INTERVAL_MINUTES=${CLEANUP_INTERVAL_MINUTES:-60}
      - YTMP4_MAX_CONCURRENT_DOWNLOADS=${MAX_CONCURRENT_DOWNLOADS:-3}
    volumes:
      - downloads:/app/downloads
    restart: unless-stopped

  frontend:
    image: ghcr.io/eef-g/ytmp4-frontend:latest
    ports:
      - "${PORT:-8080}:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  downloads:
COMPOSE
else
    echo "==> docker-compose.yml already exists, keeping current config."
fi

# ── 3. Create .env if it doesn't exist ──

if [ ! -f "$DEPLOY_DIR/.env" ]; then
    echo "==> Creating default .env (edit to customize)..."
    cat > "$DEPLOY_DIR/.env" <<'ENV'
PORT=8080
CLEANUP_INTERVAL_MINUTES=60
MAX_CONCURRENT_DOWNLOADS=3
ENV
else
    echo "==> .env already exists, keeping current config."
fi

# ── 4. Pull and start containers ──

echo "==> Pulling latest images and starting containers..."

# Use sudo if user is not yet in the docker group this session
if groups | grep -q '\bdocker\b'; then
    docker compose pull
    docker compose up -d
else
    echo "    (using sudo — re-login after deploy to run docker without sudo)"
    sudo docker compose pull
    sudo docker compose up -d
fi

# ── 5. Show status ──

echo ""
echo "==> Deployment complete!"
echo ""

PORT=$(grep -E '^PORT=' "$DEPLOY_DIR/.env" 2>/dev/null | cut -d= -f2)
PORT=${PORT:-8080}

echo "    ytmp4 is running at: http://$(hostname -I | awk '{print $1}'):$PORT"
echo ""
echo "    Useful commands (from $DEPLOY_DIR):"
echo "      docker compose logs -f      # view logs"
echo "      docker compose down         # stop"
echo "      docker compose pull && docker compose up -d  # update & restart"
