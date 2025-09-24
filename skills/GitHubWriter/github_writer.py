import os
from git import Repo
from dotenv import load_dotenv

class GitHubWriter:
    def __init__(self, local_folder, github_url, branch="main", commit_message="Add generated microservices"):
        load_dotenv()  # Load environment variables from .env file
        self.local_folder = local_folder
        self.github_url = github_url
        self.branch = branch
        self.commit_message = commit_message

    def write_to_github(self):
        # Clone the repo to a temp directory if not already present
        repo_dir = "./temp_github_repo"
        if not os.path.exists(repo_dir):
            Repo.clone_from(self.github_url, repo_dir, branch=self.branch)
        repo = Repo(repo_dir)
        # Copy generated files into the repo
        self._copy_files(self.local_folder, repo_dir)

        # Stage, commit, and push
        repo.git.add(A=True)
        repo.index.commit(self.commit_message)
        origin = repo.remote(name='origin')
        origin.push(self.branch)
        print(f"Committed and pushed generated microservices to {self.github_url} on branch {self.branch}")

    def _copy_files(self, src, dst):
        import shutil
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

# Example usage:
if __name__ == "__main__":
    writer = GitHubWriter(
        local_folder="generated_microservices",
        github_url=os.getenv("TARGET_REPO_URL"),
        branch="main",
        commit_message="Add generated microservices"
    )
    writer.write_to_github()