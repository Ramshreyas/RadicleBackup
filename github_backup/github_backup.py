import os
import json
import subprocess
import requests
import logging

# Configure logging to output to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

def get_org_repos(org_name, api_key):
    headers = {
        'Authorization': f'token {api_key}'
    }
    url = f'https://api.github.com/orgs/{org_name}/repos'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    logging.info(f"Fetched repositories for organization: {org_name}")
    return [repo['name'] for repo in response.json()]

def clone_repo(repo_name, org_name, backup_dir):
    repo_url = f'https://github.com/{org_name}/{repo_name}.git'
    repo_path = os.path.join(backup_dir, repo_name)
    if not os.path.exists(repo_path):
        logging.info(f'Cloning {repo_name}...')
        subprocess.run(['git', 'clone', repo_url], cwd=backup_dir, check=True)
    else:
        logging.info(f'{repo_name} already cloned.')

def update_repo(repo_name, backup_dir):
    repo_path = os.path.join(backup_dir, repo_name)
    logging.info(f'Updating {repo_name}...')
    subprocess.run(['git', 'fetch', 'origin'], cwd=repo_path, check=True)
    subprocess.run(['git', 'pull'], cwd=repo_path, check=True)

def backup_repos(config):
    org_name = config['github_org']
    api_key = config['api_key']
    backup_dir = config['backup_dir']

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    repos = get_org_repos(org_name, api_key)

    for repo in repos:
        clone_repo(repo, org_name, backup_dir)
        update_repo(repo, backup_dir)

def main():
    config = load_config('config.json')
    logging.info("Starting backup process...")
    backup_repos(config)
    logging.info("Backup process completed.")

if __name__ == "__main__":
    main()
