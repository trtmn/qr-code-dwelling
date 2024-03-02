# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install curl, nginx, git, and supervisord
RUN apt-get update && apt-get install -y curl nginx git supervisor

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install the Cloudflare Tunnel
RUN curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
RUN dpkg -i cloudflared.deb
#RUN cloudflared service install $(shell tunnel_key)

# Copy the default nginx.conf and supervisord configuration
COPY nginx.conf /etc/nginx/conf.d/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Make port 80 available to the world outside this container
EXPOSE 80

# Run spinup script
CMD ./spinup.sh

