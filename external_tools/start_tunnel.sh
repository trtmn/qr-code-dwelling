if [ ! -f /etc/init.d/cloudflared ]; then cloudflared service install {{ op://Automation Secrets/QR_Maker/tunnel_key }}; fi
