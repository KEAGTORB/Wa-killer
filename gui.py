import requests
import re
import tkinter as tk
from tkinter import messagebox, ttk

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

def extract_repo_info(url):
    match = re.match(r'https://github.com/([^/]+)/([^/]+)', url)
    if match:
        return match.groups()
    return None, None

class GitHubApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Repo Info - Author: saltx5")
        self.root.geometry("700x500")
        self.root.config(bg="#f4f4f4")

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="GitHub Stargazers and Forkers", font=("Arial", 16, "bold"), bg="#f4f4f4")
        title_label.pack(pady=10)

        # URL Input
        self.repo_url_label = tk.Label(self.root, text="Enter GitHub Repo URL:", font=("Arial", 12), bg="#f4f4f4")
        self.repo_url_label.pack(pady=5)
        self.repo_url_entry = tk.Entry(self.root, font=("Arial", 12), width=50)
        self.repo_url_entry.pack(pady=5)

        # Token Input
        self.token_label = tk.Label(self.root, text="Enter GitHub Token (optional):", font=("Arial", 12), bg="#f4f4f4")
        self.token_label.pack(pady=5)
        self.token_entry = tk.Entry(self.root, font=("Arial", 12), width=50)
        self.token_entry.pack(pady=5)

        # Fetch Button
        self.fetch_button = tk.Button(self.root, text="Fetch Stargazers and Forkers", font=("Arial", 12, "bold"), bg="#9CFF1E", command=self.fetch_data)
        self.fetch_button.pack(pady=20)

        # Table Frame
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack()

    def fetch_data(self):
        repo_url = self.repo_url_entry.get().strip()
        token = self.token_entry.get().strip()

        repo_owner, repo_name = extract_repo_info(repo_url)
        
        if not repo_owner or not repo_name:
            messagebox.showerror("Error", "Invalid repository URL format.")
            return

        gh_info = GitHubRepoInfo(token)
        stargazers = gh_info.get_stargazers(repo_owner, repo_name)
        forkers = gh_info.get_forkers(repo_owner, repo_name)

        self.display_table(stargazers, forkers)

    def display_table(self, stargazers, forkers):
        for widget in self.table_frame.winfo_children():
            widget.destroy()  # Clear any previous table content

        # Create Table Header
        headers = ["Stargazers", "Forkers"]
        table = ttk.Treeview(self.table_frame, columns=headers, show="headings", height=15)
        table.pack()

        for header in headers:
            table.heading(header, text=header)

        max_len = max(len(stargazers), len(forkers))

        # Populate Table with data
        for i in range(max_len):
            star = stargazers[i] if i < len(stargazers) else ""
            fork = forkers[i] if i < len(forkers) else ""
            table.insert("", "end", values=(star, fork))

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubApp(root)
    root.mainloop()
