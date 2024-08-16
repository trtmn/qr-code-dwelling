# This script is used to set up a cloudflared service and clean up supervisord logs and pid files.

#if DEBUG
if [ "$DEBUG" != "true" ]; then
  op inject --force -i ./external_tools/start_tunnel.sh -o /tmp/start_tunnel_injected.sh
  chmod u+x /tmp/start_tunnel_injected.sh
  echo "Starting cloudflared tunnel"
  /tmp/start_tunnel_injected.sh
fi

#generate the nginx configuration file from the template using 1password CLI
op inject -i ./nginx.conf.template -o /etc/nginx/conf.d/nginx.conf
# Export the shorten environment variable to the app.
export shorten="$(op read "op://Automation Secrets/QR_Maker/shorten")"
export yourls_key="$(op read "op://Automation Secrets/QR_Maker/yourls_key")"
# Remove the supervisord log file if it exists.
rm ./supervisord.log
# Remove the supervisord pid file if it exists.
rm ./supervisord.pid
# Remove the app.log file if it exists
rm ./app.log
# Wait 10 seconds for the cloudflared tunnel to start.
#echo "Waiting for the cloudflared tunnel to start..."
#sleep 10
# Start the supervisord service.
pwd
supervisord -c ./supervisord.conf