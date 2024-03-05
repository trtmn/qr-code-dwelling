# This script is used to set up a server environment with necessary dependencies and tools.

# Update the APT package list and install necessary dependencies.
# curl, nginx, git, supervisor, gpg, and sudo are installed.
apt-get update && apt-get install -y curl nginx git supervisor gpg cron nano

./1password_cli.sh

# Install Python dependencies.
# The Python dependencies are installed from the requirements.txt file.
pip install --no-cache-dir -r requirements.txt

# Install the cloudflared tunnel.
# The cloudflared package is downloaded from the GitHub releases page.
# Check the current architecture and download the appropriate package
if [ $(uname -m) = "x86_64" ]; then
  curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
fi
if [ $(uname -m) = "aarch64" ]; then
  curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
fi
if [ -f cloudflared.deb ]; then
  dpkg -i cloudflared.deb
else
  echo "cloudflared.deb file not found. Please check the download URL or network connection."
fi