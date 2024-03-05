# This script is used to set up a cloudflared service and clean up supervisord logs and pid files.

# Check if the cloudflared service is already installed.
# If not, install it using the provided tunnel key.
if [ ! -f /etc/init.d/cloudflared ]; then cloudflared service install $tunnel_key; fi

# Remove the supervisord log file if it exists.
rm ./supervisord.log

# Remove the supervisord pid file if it exists.
rm ./supervisord.pid

# Remove the app.log file if it exists
rm ./app.log

# Apply the nginx configuration.
envsubst '$SERVER_NAME' < ./nginx.conf.template > /etc/nginx/conf.d/nginx.conf

# Start the supervisord service.
/usr/bin/supervisord