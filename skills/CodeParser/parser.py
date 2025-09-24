import os
import re

class CodeParser:
    def __init__(self):
        pass

    def parse_code(self, repo_path):
        parsed_output = []

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    classes = re.findall(r'class\s+(\w+)', content)
                    methods = re.findall(r'(public|private|protected)\s+[\w<>\[\]]+\s+(\w+)\s*\(.*?\)', content)
                    annotations = re.findall(r'@(\w+)', content)
                    imports = re.findall(r'import\s+([\w\.]+);', content)

                    parsed_output.append({
                        "file": file_path,
                        "classes": classes,
                        "methods": [m[1] for m in methods],
                        "annotations": annotations,
                        "imports": imports
                    })

        return parsed_output

# Example usage
if __name__ == "__main__":
    parser = CodeParser()
    repo_path = "input"
    result = parser.parse_code(repo_path)
    print(result)