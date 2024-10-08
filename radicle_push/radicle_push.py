import os
import subprocess
import json
import logging

# Configure logging to output to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the rad binary
RAD_BINARY = "/root/.radicle/bin/rad"  # Adjust this path based on the actual location inside the .radicle folder

# Load configuration from config.json
def load_config(config_file='config.json'):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as file:
        return json.load(file)

# Load config values
config = load_config()

# Paths from configuration file
BACKUP_DIR = config.get('backup_dir', '/root/backup')
URN_FILE = config.get('urn_file', f'{BACKUP_DIR}/radicle_urns.json')

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
    try:
        # Run the 'rad .' command to check if the repository is initialized
        result = subprocess.run([RAD_BINARY, '.'], cwd=repo_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True  # Success indicates the repository is initialized
    except subprocess.CalledProcessError:
        return False  # Failure indicates the repository is not initialized

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
        # Use yes "" to send multiple newlines to rad init, effectively selecting defaults for all prompts
        subprocess.run(['sh', '-c', f'yes "" | {RAD_BINARY} init'], cwd=repo_path, check=True)
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
        # raise

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
    logging.info(f"Starting Radicle push process for backup directory: {BACKUP_DIR}...")
    process_repositories(BACKUP_DIR)
    logging.info("Radicle push process completed.")

if __name__ == "__main__":
    main()
