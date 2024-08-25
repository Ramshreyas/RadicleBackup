# GitHub and Radicle Backup Automation

This repository provides a solution for automating the backup of public GitHub repositories and pushing those backups to a Radicle node. The setup involves a Docker container for backing up GitHub repositories and a direct server process for pushing the backups to Radicle.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Repository Structure](#repository-structure)
- [GitHub Backup Process](#github-backup-process)
- [Radicle Setup and Push Process](#radicle-setup-and-push-process)
- [Running the GitHub Backup Container](#running-the-github-backup-container)
- [Setting Up Radicle Push on the Server](#setting-up-radicle-push-on-the-server)
- [Testing the Setup](#testing-the-setup)
- [Scheduling](#scheduling)
- [Troubleshooting](#troubleshooting)

## Overview

This project consists of two main processes:

1. **GitHub Backup**: Clones all public repositories from a specified GitHub organization into a local directory using Docker.
2. **Radicle Push**: Pushes the backed-up repositories to a Radicle node for decentralized storage directly on the server.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker**: Used to create and manage containers for the GitHub backup process.
- **Radicle CLI**: Installed directly on the server for managing the Radicle push process.
- **GitHub Personal Access Token (PAT)**: Required for accessing the GitHub API.

## Repository Structure

```
/path/to/project/
├── github_backup/
│   ├── Dockerfile
│   ├── github_backup.py
│   ├── config.json
│   ├── crontab
├── radicle_push/
│   ├── radicle_push.py
│   ├── crontab
```

### `config.json` Example

```json
{
    "github_org": "your-github-org-name",
    "api_key": "your-github-api-key",
    "backup_dir": "/app/backup"
}
```

- **`github_org`**: The name of the GitHub organization you want to back up.
- **`api_key`**: Your GitHub PAT.
- **`backup_dir`**: Directory inside the container where repositories will be backed up.

## GitHub Backup Process

### 1. Setup

Navigate to the `github_backup/` directory and build the Docker image:

```bash
cd github_backup
docker build -t github-backup .
```

### 2. Running the Container

Run the container, mounting the backup directory on your host machine:

```bash
docker run -d -v /root/backup:/app/backup --name github-backup github-backup
```

### 3. Scheduled Backups

The GitHub backup process is configured to run daily at midnight via a cron job specified in the `crontab` file. You can view and modify this schedule as needed.

## Radicle Setup and Push Process

### 1. Install Radicle

Install Radicle on your server using the following command:

```bash
curl -sSf https://radicle.xyz/install | sh
```

### 2. Verify Installation

Check that Radicle has been installed correctly:

```bash
rad --version
```

### 3. Create a Radicle Identity

Create a Radicle identity on the server:

```bash
rad auth
```

Follow the prompts to create your identity.

### 4. Start the Radicle Node

Start the Radicle node and check its status:

```bash
rad node status
rad node start
```

### 5. Setting Up the Radicle Push Script

Place the `radicle_push.py` script in the appropriate directory on your server, and ensure it is executable:

```bash
chmod +x /path/to/radicle_push/radicle_push.py
```

### 6. Configure Crontab for Radicle Push

Set up a cron job to run the Radicle push script daily at 1 AM:

1. Edit the crontab:

```bash
crontab -e
```

2. Add the following entry to schedule the script:

```bash
0 1 * * * /usr/bin/python3 /path/to/radicle_push/radicle_push.py >> /var/log/radicle_push.log 2>&1
```

This will run the `radicle_push.py` script at 1 AM every day, and log the output to `/var/log/radicle_push.log`.

## Running the GitHub Backup Container

To run the GitHub backup process, execute the following command:

```bash
docker run -d -v /root/backup:/app/backup --name github-backup github-backup
```

This command mounts the backup directory on your host machine to `/app/backup` inside the container.

## Setting Up Radicle Push on the Server

1. Ensure the Radicle node is running:

```bash
rad node start
```

2. The Radicle push process is handled directly on the server via the cron job set up earlier. Ensure that the `radicle_push.py` script is correctly configured and scheduled.

## Testing the Setup

You can manually test each process by running the associated commands:

1. **Test GitHub Backup**:

```bash
docker exec -it github-backup python /app/github_backup.py
```

2. **Test Radicle Push**:

```bash
/usr/bin/python3 /path/to/radicle_push/radicle_push.py
```

## Scheduling

Both processes are set up to run automatically via cron jobs:

- **GitHub Backup**: Runs daily at midnight using Docker.
- **Radicle Push**: Runs daily at 1 AM directly on the server.

You can modify the schedules by editing the `crontab` files.

## Troubleshooting

If you encounter issues, consider the following steps:

1. **Check Logs**:

   For GitHub backup:

   ```bash
   docker logs github-backup
   ```

   For Radicle push:

   Check the log file specified in the crontab entry, e.g., `/var/log/radicle_push.log`.

2. **Inspect Containers**:

   Enter the container for manual inspection:

   ```bash
   docker exec -it github-backup /bin/bash
   ```

3. **Verify Radicle Node**:

   Ensure the Radicle node is running:

   ```bash
   rad node status
   ```

4. **Permissions**:

   Verify that the directories on your host machine have appropriate permissions for Docker and the Radicle push script to access.

---

This setup ensures that your GitHub repositories are backed up locally and pushed to Radicle for decentralized storage, with both processes automated and easily manageable.
