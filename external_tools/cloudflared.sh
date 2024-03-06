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