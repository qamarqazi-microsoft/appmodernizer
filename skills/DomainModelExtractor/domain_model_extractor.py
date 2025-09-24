import os
import re

class DomainModelExtractor:
    def __init__(self):
        pass

    def extract_domain_models(self, repo_path):
        domain_models = {}

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    if "@Entity" in content:
                        class_match = re.search(r'class\s+(\w+)', content)
                        if class_match:
                            class_name = class_match.group(1)
                            fields = re.findall(r'(private|protected|public)\s+(\w+)\s+(\w+);', content)
                            domain_models[class_name] = [{"type": f[1], "name": f[2]} for f in fields]

        return domain_models

# Example usage
if __name__ == "__main__":
    tool = DomainModelExtractor()
    repo_path = "/path/to/cloned/repo"
    models = tool.extract_domain_models(repo_path)
    print(models)