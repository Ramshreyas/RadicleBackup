# GitHub and Radicle Backup Automation

This repository provides a Dockerized solution for automating the backup of public GitHub repositories and pushing those backups to a Radicle node. The setup involves two separate Docker containers—one for backing up GitHub repositories and another for pushing the backups to Radicle.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Repository Structure](#repository-structure)
- [GitHub Backup Process](#github-backup-process)
- [Radicle Push Process](#radicle-push-process)
- [Running the Containers](#running-the-containers)
- [Testing the Setup](#testing-the-setup)
- [Scheduling](#scheduling)
- [Troubleshooting](#troubleshooting)

## Overview

This project consists of two main processes:

1. **GitHub Backup**: Clones all public repositories from a specified GitHub organization into a local directory.
2. **Radicle Push**: Pushes the backed-up repositories to a Radicle node for decentralized storage.

Each process runs in its own Docker container and can be scheduled to run automatically using cron jobs.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker**: Used to create and manage containers.
- **Radicle Node**: Ensure you have a Radicle node running either on your host machine or accessible via the network.
- **GitHub Personal Access Token (PAT)**: Required for accessing the GitHub API.

## Repository Structure

\```
/path/to/project/
├── github_backup/
│   ├── Dockerfile
│   ├── github_backup.py
│   ├── config.json
│   ├── crontab
├── radicle_push/
│   ├── Dockerfile
│   ├── radicle_push.py
│   ├── crontab
\```

### `config.json` Example

\```json
{
    "github_org": "your-github-org-name",
    "api_key": "your-github-api-key",
    "backup_dir": "/app/backup"
}
\```

- **`github_org`**: The name of the GitHub organization you want to back up.
- **`api_key`**: Your GitHub PAT.
- **`backup_dir`**: Directory inside the container where repositories will be backed up.

## GitHub Backup Process

### 1. Setup

Navigate to the `github_backup/` directory and build the Docker image:

\```bash
cd github_backup
docker build -t github-backup .
\```

### 2. Running the Container

Run the container, mounting the backup directory on your host machine:

\```bash
docker run -d -v /root/backup:/app/backup --name github-backup github-backup
\```

### 3. Scheduled Backups

The GitHub backup process is configured to run daily at midnight via a cron job specified in the `crontab` file. You can view and modify this schedule as needed.

## Radicle Push Process

### 1. Setup

Navigate to the `radicle_push/` directory and build the Docker image:

\```bash
cd radicle_push
docker build -t radicle-push .
\```

### 2. Running the Container

Run the container, ensuring you mount both the GitHub backup directory and the Radicle data directory:

\```bash
docker run -d \
  -v /root/backup:/app/backup \
  -v /root/.radicle:/root/.radicle \
  --name radicle-push radicle-push
\```

- **Note**: If the Radicle binary is located inside the `.radicle` directory, the `radicle_push.py` script will need to reference the correct path (e.g., `/root/.radicle/bin/rad`).

### 3. Scheduled Radicle Push

The Radicle push process is configured to run daily at 1 AM via a cron job specified in the `crontab` file. You can view and modify this schedule as needed.

## Running the Containers

To run both the GitHub backup and Radicle push processes, execute the following commands:

1. **Run GitHub Backup**:

\```bash
docker run -d -v /root/backup:/app/backup --name github-backup github-backup
\```

2. **Run Radicle Push**:

\```bash
docker run -d \
  -v /root/backup:/app/backup \
  -v /root/.radicle:/root/.radicle \
  --name radicle-push radicle-push
\```

## Testing the Setup

You can manually test each process by running the associated scripts inside their respective containers:

1. **Test GitHub Backup**:

\```bash
docker exec -it github-backup python /app/github_backup.py
\```

2. **Test Radicle Push**:

\```bash
docker exec -it radicle-push python /app/radicle_push.py
\```

## Scheduling

Both processes are set up to run automatically via cron jobs:

- **GitHub Backup**: Runs daily at midnight.
- **Radicle Push**: Runs daily at 1 AM.

You can modify the schedules by editing the `crontab` files in each respective directory.

## Troubleshooting

If you encounter issues, consider the following steps:

1. **Check Logs**:

   View logs for either container using:

   \```bash
   docker logs github-backup
   docker logs radicle-push
   \```

2. **Inspect Containers**:

   Enter the container for manual inspection:

   \```bash
   docker exec -it github-backup /bin/bash
   docker exec -it radicle-push /bin/bash
   \```

3. **Verify Volume Mounts**:

   Ensure that volumes are mounted correctly, and data is accessible inside the containers.

4. **Permissions**:

   Verify that the directories on your host machine have appropriate permissions for Docker to access.

---

This setup ensures that your GitHub repositories are backed up locally and pushed to Radicle for decentralized storage, with both processes automated and easily manageable.
