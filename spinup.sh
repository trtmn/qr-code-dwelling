# This script is used to set up a cloudflared service and clean up supervisord logs and pid files.

# Check if the cloudflared service is already installed.
# If not, install it using the provided tunnel key.
if [ ! -f /etc/init.d/cloudflared ]; then cloudflared service install $tunnel_key; fi

# Remove the supervisord log file if it exists.
rm ./supervisord.log

# Remove the supervisord pid file if it exists.
rm ./supervisord.pid

# Start the supervisord service.
/usr/bin/supervisord