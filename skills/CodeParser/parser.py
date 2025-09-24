import os
import re

class CodeParser:
    def __init__(self):
        pass

    def parse_code(self, repo_path):
        parsed_output = []

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".cs"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    namespaces = re.findall(r'namespace\s+([\w\.]+)', content)
                    classes = re.findall(r'class\s+(\w+)(?:\s*:\s*([\w, ]+))?', content)
                    methods = re.findall(r'(public|private|protected|internal)\s+[\w<>\[\]]+\s+(\w+)\s*\(.*?\)', content)
                    properties = re.findall(r'(public|private|protected|internal)\s+[\w<>\[\]]+\s+(\w+)\s*\{\s*get;.*?set;.*?\}', content)
                    annotations = re.findall(r'\[(\w+)\]', content)
                    imports = re.findall(r'using\s+([\w\.]+);', content)

                    parsed_output.append({
                        "file": file_path,
                        "namespaces": namespaces,
                        "classes": [{"name": c[0], "inherits": c[1].split(", ") if c[1] else []} for c in classes],
                        "methods": [{"name": m[1], "access": m[0]} for m in methods],
                        "properties": [{"name": p[1], "access": p[0]} for p in properties],
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
