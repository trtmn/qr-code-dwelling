# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install APT packages and Other Dependencies
RUN ./install_tools.sh


# Copy the default nginx.conf and supervisord configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Make port 80 available to the world outside this container
EXPOSE 80


# Run spinup script
CMD ./spinup.sh

