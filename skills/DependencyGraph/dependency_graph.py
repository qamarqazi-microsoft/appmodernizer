import os
import re

class DependencyGraph:
    def __init__(self):
        pass

    def build_dependency_graph(self, repo_path):
        graph = {}

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    class_match = re.search(r'class\s+(\w+)', content)
                    imports = re.findall(r'import\s+([\w\.]+);', content)

                    if class_match:
                        class_name = class_match.group(1)
                        graph[class_name] = imports

        return graph

# Example usage
if __name__ == "__main__":
    tool = DependencyGraph()
    repo_path = "/path/to/cloned/repo"
    graph = tool.build_dependency_graph(repo_path)
    print(graph)