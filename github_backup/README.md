# GitHub Organization Backup Script

This repository provides a Dockerized solution to back up all public repositories from a GitHub organization to your local machine. The backup process is automated to run daily at midnight using a cron job inside a Docker container.

## Features

- Automatically clones and updates all public repositories from a specified GitHub organization.
- Stores the repositories in a mounted local directory for easy access and additional backup security.
- Runs daily at midnight server time via a cron job.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- [Docker](https://www.docker.com/get-started)
- A GitHub [Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with at least `repo` scope.

### Repository Setup

1. **Clone this repository:**

    ```bash
    git clone https://github.com/yourusername/github-org-backup.git
    cd github-org-backup
    ```

2. **Configure the backup settings:**

    - Rename the `config.example.json` to `config.json`:

      ```bash
      mv config.example.json config.json
      ```

    - Open `config.json` and fill in the required details:
    
      ```json
      {
          "github_org": "your-github-org-name",
          "api_key": "your-github-api-key",
          "backup_dir": "/app/backup"
      }
      ```

    - Replace `"your-github-org-name"` with the name of the GitHub organization.
    - Replace `"your-github-api-key"` with your GitHub Personal Access Token.
    - The `backup_dir` should remain `/app/backup` to correctly map with the Docker volume.

3. **Build the Docker image:**

    ```bash
    docker build -t github-backup-cron .
    ```

### Running the Backup

1. **Run the Docker container:**

    ```bash
    docker run -d -v /path/to/local/backup:/app/backup --name github-backup github-backup-cron
    ```

    - Replace `/path/to/local/backup` with the directory on your local machine where you want to store the backups.
    - The container will run in the background, automatically performing backups daily at midnight.

### Checking Logs and Manual Execution

- **View Logs:**

    To check the output of the cron job, you can view the container logs:

    ```bash
    docker logs github-backup
    ```

- **Manual Backup:**

    If you want to manually trigger the backup, you can execute the script inside the running container:

    ```bash
    docker exec -it github-backup python /app/github_backup.py
    ```

### Updating the Configuration

If you need to update the `config.json` file or make other changes, follow these steps:

1. Stop the running container:

    ```bash
    docker stop github-backup
    ```

2. Make the necessary changes to `config.json`.

3. Rebuild the Docker image:

    ```bash
    docker build -t github-backup-cron .
    ```

4. Start the container again:

    ```bash
    docker run -d -v /path/to/local/backup:/app/backup --name github-backup github-backup-cron
    ```

### Troubleshooting

- **Common Issues:**
  - Ensure the GitHub API key has the necessary permissions.
  - Check that the local backup directory has sufficient space and correct permissions.

- **Cron Job Debugging:**
  - If the cron job does not run as expected, check the cron log inside the container:

    ```bash
    docker exec -it github-backup cat /var/log/cron.log
    ```

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for any bugs or feature requests.

### Author

- **Your Name** - [GitHub Profile](https://github.com/yourusername)

---

**Note:** This repository and script are designed to handle public repositories. If your organization has private repositories, additional considerations regarding API key permissions and security will be required.
