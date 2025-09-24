import git
import tempfile
import os

def clone_repo(repo_url, branch="main"):
    # Create a temporary directory to clone the repo
    input_dir = "input"
    print(f"Cloning into temporary directory: {input_dir}")
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    # Clone the repo
        git.Repo.clone_from(repo_url, input_dir, branch=branch)
    # Optionally list files
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            print(os.path.join(root, file))

    return input_dir

# Example usage
if __name__ == "__main__":
    repo_url = "https://github.com/Jonahida/java-spring-monolithic-ecommerce-application"
    clone_repo(repo_url)