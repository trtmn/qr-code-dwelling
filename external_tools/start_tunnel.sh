# Check if the cloudflared service is already installed.
# If not, install it using the provided tunnel key.
if [ ! -f /etc/init.d/cloudflared ]; then cloudflared service install {{ op://Automation Secrets/QR_Maker/tunnel_key }}; fi
