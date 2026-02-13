#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────
# ytmp4 deploy script for Ubuntu Server
# Installs Docker if needed, then builds & runs
# ──────────────────────────────────────────────

APP_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> ytmp4 deployment starting..."
echo "    App directory: $APP_DIR"

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

# ── 2. Create .env from example if it doesn't exist ──

if [ ! -f "$APP_DIR/.env" ]; then
    echo "==> Creating .env from .env.example (edit to customize)..."
    cp "$APP_DIR/.env.example" "$APP_DIR/.env"
else
    echo "==> .env already exists, keeping current config."
fi

# ── 3. Build and start containers ──

echo "==> Building and starting containers..."
cd "$APP_DIR"

# Use sudo if user is not yet in the docker group this session
if groups | grep -q '\bdocker\b'; then
    docker compose up --build -d
else
    echo "    (using sudo — re-login after deploy to run docker without sudo)"
    sudo docker compose up --build -d
fi

# ── 4. Show status ──

echo ""
echo "==> Deployment complete!"
echo ""

PORT=$(grep -E '^PORT=' "$APP_DIR/.env" 2>/dev/null | cut -d= -f2)
PORT=${PORT:-8080}

echo "    ytmp4 is running at: http://$(hostname -I | awk '{print $1}'):$PORT"
echo ""
echo "    Useful commands:"
echo "      docker compose logs -f        # view logs"
echo "      docker compose down            # stop"
echo "      docker compose up --build -d   # rebuild & restart"
