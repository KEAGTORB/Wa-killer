import requests
import os
import re

class GitHubRepoInfo:
    def __init__(self, token=None):
        self.token = token
        self.headers = {}
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'

    def get_stargazers(self, repo_owner, repo_name):
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/stargazers'
        stargazers = []
        page = 1
        
        while True:
            response = requests.get(url, headers=self.headers, params={'page': page, 'per_page': 100})
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                stargazers.extend([user['login'] for user in data])
                page += 1
            else:
                break
        return stargazers

    def get_forkers(self, repo_owner, repo_name):
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/forks'
        forkers = []
        page = 1

        while True:
            response = requests.get(url, headers=self.headers, params={'page': page, 'per_page': 100})
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                forkers.extend([fork['owner']['login'] for fork in data])
                page += 1
            else:
                break
        return forkers

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def extract_repo_info(url):
    match = re.match(r'https://github.com/([^/]+)/([^/]+)', url)
    if match:
        return match.groups()
    return None, None

def main():
    clear_screen()
    print("""       
  ______ ____  _____  _  __ _____ _______       _____  
 |  ____/ __ \|  __ \| |/ // ____|__   __|/\   |  __ \ 
 | |__ | |  | | |__) | ' /| (___    | |  /  \  | |__) |
 |  __|| |  | |  _  /|  <  \___ \   | | / /\ \ |  _  / 
 | |   | |__| | | \ \| . \ ____) |  | |/ ____ \| | \ \ 
 |_|    \____/|_|  \_\_|\_\_____/   |_/_/    \_\_|  \_\                                                                                          

    """)
    print("=" * 50)
    print("Author: github.com/saltx5")
    print("=" * 50)

    repo_url = input("Enter the GitHub repository URL: ").strip()
    token = input("Enter your GitHub personal access token (leave empty if not required): ").strip()

    repo_owner, repo_name = extract_repo_info(repo_url)
    
    if not repo_owner or not repo_name:
        print("Invalid repository URL format.")
        return

    gh_info = GitHubRepoInfo(token)

    print("\nFetching data, please wait...\n")

    stargazers = gh_info.get_stargazers(repo_owner, repo_name)
    forkers = gh_info.get_forkers(repo_owner, repo_name)

    print(f"Repository: {repo_owner}/{repo_name}\n")
    
    max_len = max(len(stargazers), len(forkers))

    print(f"{'Stargazers':<40} {'Forkers'}")
    print("-" * 80)

    for i in range(max_len):
        star = stargazers[i] if i < len(stargazers) else ""
        fork = forkers[i] if i < len(forkers) else ""
        print(f"{star:<40} {fork}")

    print("=" * 50)

if __name__ == "__main__":
    main()
