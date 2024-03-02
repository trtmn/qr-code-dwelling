if [ ! -f /etc/init.d/cloudflared ]; then cloudflared service install $tunnel_key; fi
rm ./supervisord.log
rm ./supervisord.pid
/usr/bin/supervisord