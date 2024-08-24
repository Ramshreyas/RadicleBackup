import os
import subprocess
import json
import logging

# Configure logging to output to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the rad binary
RAD_BINARY = "/root/.radicle/bin/rad"  # Adjust this path based on the actual location inside the .radicle folder

URN_FILE = "/root/backup/radicle_urns.json"  # File to store URNs

def load_urns():
    """Load the URNs from the JSON file."""
    if os.path.exists(URN_FILE):
        with open(URN_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_urns(urns):
    """Save the URNs to the JSON file."""
    with open(URN_FILE, 'w') as file:
        json.dump(urns, file, indent=4)

def is_radicle_repo(repo_path):
    """Check if the repository is already initialized as a Radicle project."""
    rad_path = os.path.join(repo_path, '.rad')
    return os.path.exists(rad_path)

def get_radicle_urn(repo_path):
    """Retrieve the Radicle URN by running 'rad .'."""
    try:
        result = subprocess.run([RAD_BINARY, '.'], cwd=repo_path, check=True, stdout=subprocess.PIPE, text=True)
        urn = result.stdout.strip()
        logging.info(f"Retrieved Radicle URN for {repo_path}: {urn}")
        return urn
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to retrieve Radicle URN for {repo_path}: {e}")
        raise

def initialize_radicle_repo(repo_path):
    """Initialize the repository as a Radicle project."""
    logging.info(f"Initializing Radicle project in {repo_path}...")
    try:
        subprocess.run([RAD_BINARY, 'init'], cwd=repo_path, check=True)
        logging.info(f"Successfully initialized Radicle project: {repo_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to initialize Radicle project in {repo_path}: {e}")
        raise

def push_to_radicle(repo_path):
    """Push the repository to the Radicle network."""
    logging.info(f"Pushing {repo_path} to Radicle network...")
    try:
        subprocess.run(['git', 'push', 'rad', '--all'], cwd=repo_path, check=True)
        subprocess.run(['git', 'push', 'rad', '--tags'], cwd=repo_path, check=True)
        logging.info(f"Successfully pushed {repo_path} to Radicle network")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to push {repo_path} to Radicle network: {e}")
        raise

def process_repositories(backup_dir):
    """Process each repository in the backup directory."""
    urns = load_urns()

    for repo_name in os.listdir(backup_dir):
        repo_path = os.path.join(backup_dir, repo_name)
        if os.path.isdir(repo_path):
            logging.info(f"Processing repository: {repo_name}")
            if not is_radicle_repo(repo_path):
                initialize_radicle_repo(repo_path)

            # Retrieve the URN and store it
            urn = get_radicle_urn(repo_path)
            urns[repo_name] = urn

            # Push the repository to Radicle network
            push_to_radicle(repo_path)

    save_urns(urns)

def main():
    backup_dir = "/root/backup"  # This should match the directory where the repos are backed up
    logging.info("Starting Radicle push process...")
    process_repositories(backup_dir)
    logging.info("Radicle push process completed.")

if __name__ == "__main__":
    main()
