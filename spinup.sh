# This script is used to set up a cloudflared service and clean up supervisord logs and pid files.


op inject --force -i ./external_tools/start_tunnel.sh -o ./external_tools/start_tunnel.sh
#if [ ! -f /etc/init.d/cloudflared ]; then cloudflared service install $tunnel_key; fi

# Make the shell scripts executable.
chmod u+x ./external_tools/*.sh

# Remove the supervisord log file if it exists.
rm ./supervisord.log

# Remove the supervisord pid file if it exists.
rm ./supervisord.pid

# Remove the app.log file if it exists
rm ./app.log

#generate the nginx configuration file from the template using 1password CLI
op inject -i ./nginx.conf.template -o /etc/nginx/conf.d/nginx.conf

# Start the supervisord service.
supervisord -c /etc/supervisor/conf.d/supervisord.conf