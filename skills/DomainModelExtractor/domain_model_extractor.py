import os
import re

class DomainModelExtractor:
    def __init__(self):
        pass

    def extract_domain_models(self, repo_path):
        domain_models = {}
        excluded_suffixes = ("Controller", "Repository", "Service", "Tests")

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".cs"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # Only consider files with [Table] attribute or those in Models folder
                    if "[Table]" in content or "Models" in root:
                        class_match = re.search(r'class\s+(\w+)', content)
                        if class_match:
                            class_name = class_match.group(1)

                            # Skip classes with unwanted suffixes
                            if class_name.endswith(excluded_suffixes):
                                continue

                            # Extract public properties with getters and setters
                            properties = re.findall(
                                r'public\s+([\w<>\?]+)\s+(\w+)\s*\{\s*get;\s*set;\s*\}', content)

                            # Extract fields (private, protected, public)
                            fields = re.findall(
                                r'(private|protected|public)\s+([\w<>\?]+)\s+(\w+);', content)

                            # Combine properties and fields
                            members = [{"type": p[0], "name": p[1]} for p in properties] + \
                                      [{"type": f[1], "name": f[2]} for f in fields]

                            domain_models[class_name] = members

        return domain_models

# Example usage
if __name__ == "__main__":
    tool = DomainModelExtractor()
    repo_path = "/path/to/cloned/repo"
    models = tool.extract_domain_models(repo_path)
    print(models)
