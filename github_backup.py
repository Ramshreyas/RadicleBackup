import os
import json
import subprocess
import requests

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
    return [repo['name'] for repo in response.json()]

def clone_repo(repo_name, org_name, backup_dir):
    repo_url = f'https://github.com/{org_name}/{repo_name}.git'
    repo_path = os.path.join(backup_dir, repo_name)
    if not os.path.exists(repo_path):
        print(f'Cloning {repo_name}...')
        subprocess.run(['git', 'clone', repo_url], cwd=backup_dir)
    else:
        print(f'{repo_name} already cloned.')

def update_repo(repo_name, backup_dir):
    repo_path = os.path.join(backup_dir, repo_name)
    print(f'Updating {repo_name}...')
    subprocess.run(['git', 'fetch', '--all'], cwd=repo_path)
    subprocess.run(['git', 'pull'], cwd=repo_path)

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
    backup_repos(config)

if __name__ == "__main__":
    main()
