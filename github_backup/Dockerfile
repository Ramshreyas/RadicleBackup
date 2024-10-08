# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install git and cron
RUN apt-get update && apt-get install -y git cron && apt-get clean

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add the crontab file in the cron directory
COPY crontab /etc/cron.d/github_backup_cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/github_backup_cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Apply cron job
RUN crontab /etc/cron.d/github_backup_cron

# Make sure the python script is executable
RUN chmod +x github_backup.py

# Start cron and then the main process (to keep the container running)
CMD cron && tail -f /var/log/cron.log
